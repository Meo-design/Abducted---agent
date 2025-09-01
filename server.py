
from flask import Flask, request, jsonify, render_template_string
import os, json, datetime, threading, requests, smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# --- Config ---
PLAYBOOK = {}
PLAYBOOK_PATH = os.environ.get("PLAYBOOK_PATH", "./playbook/Abducted_Memories_Campaign_Playbook.json")
PLAYBOOK_URL  = os.environ.get("PLAYBOOK_URL")  # optional http(s) source
CRON_TOKEN    = os.environ.get("CRON_TOKEN", "")  # protect cron endpoints
DAILY_HOUR    = os.environ.get("DAILY_HOUR", "09:00")
DRY_RUN       = os.environ.get("DRY_RUN", "true").lower() == "true"

# Email digest (SMTP)
SMTP_HOST = os.environ.get("SMTP_HOST","")
SMTP_PORT = int(os.environ.get("SMTP_PORT","587"))
SMTP_USER = os.environ.get("SMTP_USER","")
SMTP_PASS = os.environ.get("SMTP_PASS","")
DIGEST_TO = os.environ.get("DIGEST_TO","")
DIGEST_FROM = os.environ.get("DIGEST_FROM", SMTP_USER or "no-reply@example.com")
DIGEST_DAY = os.environ.get("DIGEST_DAY","mon").lower()  # mon,tue,wed,thu,fri,sat,sun

# --- State ---
last_quick = None
last_daily = None
last_weekly = None
lock = threading.Lock()

# Lightweight KPI and decision memory (use DB later if needed)
KPI = {
    "ads": {"ctr": 0.0, "roas": 0.0, "orders": 0, "revenue": 0.0, "spend": 0.0},
    "social": {"posts_last_7d": 0, "engagement_rate": 0.0},
    "email": {"subs": 0, "open_rate": 0.0, "click_rate": 0.0},
    "reviews": {"count": 0, "avg": 0.0}
}
DECISIONS = []  # append dicts; keep last 100
MAX_DECISIONS = 100

DASHBOARD_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Defenders Agent Dashboard</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;color:#111}
    h1{margin:0 0 8px 0} .muted{color:#666}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:16px 0}
    .card{border:1px solid #e5e7eb;border-radius:12px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
    .title{font-weight:600;margin-bottom:8px}
    pre{background:#0b1020;color:#e5e7eb;padding:12px;border-radius:8px;overflow:auto}
    table{width:100%;border-collapse:collapse}
    th,td{border-bottom:1px solid #eee;padding:8px;text-align:left;font-size:14px;vertical-align:top}
    th{font-weight:600;background:#fafafa}
    .pill{display:inline-block;padding:2px 8px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:12px}
    .ok{color:#059669} .warn{color:#b45309} .err{color:#b91c1c}
  </style>
</head>
<body>
  <h1>Defenders Agent <span class="muted">— Dashboard</span></h1>
  <div class="muted">Playbook: {{ meta.title or 'Unknown' }} • Dry-Run: {{ 'ON' if dry_run else 'OFF' }}</div>

  <div class="grid">
    <div class="card">
      <div class="title">Ads</div>
      <div>CTR: {{ kpi.ads.ctr }}%</div>
      <div>ROAS: {{ kpi.ads.roas }}x</div>
      <div>Orders: {{ kpi.ads.orders }}</div>
      <div>Revenue: ${{ '{:,.2f}'.format(kpi.ads.revenue) }}</div>
      <div>Spend: ${{ '{:,.2f}'.format(kpi.ads.spend) }}</div>
    </div>
    <div class="card">
      <div class="title">Social</div>
      <div>Posts (7d): {{ kpi.social.posts_last_7d }}</div>
      <div>Engagement Rate: {{ kpi.social.engagement_rate }}%</div>
    </div>
    <div class="card">
      <div class="title">Email</div>
      <div>Subscribers: {{ kpi.email.subs }}</div>
      <div>Open Rate: {{ kpi.email.open_rate }}%</div>
      <div>Click Rate: {{ kpi.email.click_rate }}%</div>
    </div>
    <div class="card">
      <div class="title">Reviews</div>
      <div>Count: {{ kpi.reviews.count }}</div>
      <div>Avg Rating: {{ kpi.reviews.avg }}</div>
    </div>
  </div>

  <div class="card">
    <div class="title">Recent Decisions <span class="pill">{{ decisions|length }}</span></div>
    <table>
      <tr><th>Time (UTC)</th><th>Action</th><th>Details</th></tr>
      {% for d in decisions %}
      <tr>
        <td>{{ d.time }}</td>
        <td>{{ d.action }}</td>
        <td><pre>{{ d.payload }}</pre></td>
      </tr>
      {% endfor %}
    </table>
  </div>

  <div class="muted" style="margin-top:12px;">
    Last quick: {{ last_quick or '—' }} • Last daily: {{ last_daily or '—' }} • Last weekly: {{ last_weekly or '—' }}
  </div>
</body>
</html>
"""

def load_playbook():
    global PLAYBOOK
    try:
        if PLAYBOOK_URL and PLAYBOOK_URL.startswith("http"):
            resp = requests.get(PLAYBOOK_URL, timeout=10)
            resp.raise_for_status()
            PLAYBOOK = resp.json()
        else:
            with open(PLAYBOOK_PATH, "r", encoding="utf-8") as f:
                PLAYBOOK = json.load(f)
        return {"ok": True, "source": PLAYBOOK_URL or PLAYBOOK_PATH}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def auth_ok(req):
    tok = req.headers.get("X-CRON-TOKEN") or req.args.get("token","")
    return (CRON_TOKEN == "" and os.environ.get("ALLOW_PUBLIC_CRON","false").lower()=="true") or (tok and tok == CRON_TOKEN)

def record_decision(action, payload):
    from datetime import datetime as dt
    DECISIONS.append({"time": dt.utcnow().isoformat()+'Z', "action": action, "payload": json.dumps(payload, ensure_ascii=False, indent=2)})
    # Trim
    if len(DECISIONS) > MAX_DECISIONS:
        del DECISIONS[:len(DECISIONS)-MAX_DECISIONS]

def evaluate_and_act(kind="quick"):
    meta = PLAYBOOK.get("meta", {})
    social_posts = PLAYBOOK.get("social_calendar", {}).get("posts", [])

    if kind == "quick":
        # Queue next 3 posts (DRY-RUN)
        queued = []
        for p in social_posts[:3]:
            payload = {"platform":"generic","copy":p.get("copy",""),"day":p.get("day")}
            record_decision("queue_post", payload)
            queued.append(payload)
        # Example: ads adjust
        ads_payload = {"note":"paused low CTR keywords; scaled ROAS≥2.0 ad sets", "dry_run":DRY_RUN}
        record_decision("ads_adjust", ads_payload)
        return {"queued_posts": queued, "ads": ads_payload}

    else:  # daily
        scheduled = []
        for p in social_posts[:14]:
            payload = {"platform":"generic","copy":p.get("copy",""),"day":p.get("day")}
            record_decision("schedule_post", payload)
            scheduled.append(payload)
        email_payload = {"subject":"Welcome to the Veil","dry_run":DRY_RUN}
        record_decision("stage_newsletter", email_payload)
        return {"scheduled_posts": scheduled, "email": email_payload}

def weekday_str(dt):
    return ["mon","tue","wed","thu","fri","sat","sun"][dt.weekday()]

def send_weekly_digest():
    # Compose a simple text report from KPI & DECISIONS
    lines = []
    lines.append("Abducted Memories — Weekly Performance Digest\n")
    lines.append(f"Ads: CTR {KPI['ads']['ctr']}% | ROAS {KPI['ads']['roas']}x | Orders {KPI['ads']['orders']} | Revenue ${KPI['ads']['revenue']:.2f} | Spend ${KPI['ads']['spend']:.2f}")
    lines.append(f"Social: Posts(7d) {KPI['social']['posts_last_7d']} | ER {KPI['social']['engagement_rate']}%")
    lines.append(f"Email: Subs {KPI['email']['subs']} | Open {KPI['email']['open_rate']}% | Click {KPI['email']['click_rate']}%")
    lines.append(f"Reviews: Count {KPI['reviews']['count']} | Avg {KPI['reviews']['avg']}")
    lines.append("\nRecent decisions:")
    for d in DECISIONS[-10:]:
        lines.append(f"- {d['time']} • {d['action']}")
    body = "\n".join(lines)

    # If SMTP not configured, write to file and return
    if not (SMTP_HOST and DIGEST_TO):
        try:
            with open("./outputs/digest_last.txt","w",encoding="utf-8") as f:
                f.write(body)
            return {"ok": True, "saved_to": "./outputs/digest_last.txt", "note": "SMTP not configured"}
        except Exception as e:
            return {"ok": False, "error": str(e), "note":"SMTP not configured"}

    try:
        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = "Abducted Memories — Weekly Performance"
        msg["From"] = DIGEST_FROM
        msg["To"] = DIGEST_TO

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
            s.starttls()
            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)

        return {"ok": True, "sent_to": DIGEST_TO}
    except Exception as e:
        # Fallback to file
        try:
            with open("./outputs/digest_last.txt","w",encoding="utf-8") as f:
                f.write(body + f"\n\n[Email error: {e}]")
            return {"ok": False, "error": str(e), "saved_to":"./outputs/digest_last.txt"}
        except Exception as e2:
            return {"ok": False, "error": f"{e} | fallback failed: {e2}"}

@app.get("/health")
def health():
    return jsonify(ok=True, last_quick=last_quick, last_daily=last_daily, last_weekly=last_weekly)

@app.get("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD_HTML,
        meta=PLAYBOOK.get("meta", {}),
        kpi=type("O",(),{ "ads":type("O",(),KPI["ads"])(),
                          "social":type("O",(),KPI["social"])(),
                          "email":type("O",(),KPI["email"])(),
                          "reviews":type("O",(),KPI["reviews"])() })(),
        decisions=DECISIONS[::-1],  # newest first
        dry_run=DRY_RUN,
        last_quick=last_quick, last_daily=last_daily, last_weekly=last_weekly
    )

@app.get("/dashboard/summary")
def dashboard_summary():
    return jsonify(ok=True, playbook_meta=PLAYBOOK.get("meta", {}), kpi=KPI, dry_run=DRY_RUN)

@app.post("/playbook/reload")
def playbook_reload():
    res = load_playbook()
    return jsonify(res)

@app.post("/cron/quick")
def cron_quick():
    global last_quick
    if not auth_ok(request):
        return jsonify(ok=False, error="unauthorized"), 401
    with lock:
        out = evaluate_and_act(kind="quick")
        import datetime as dt
        last_quick = dt.datetime.utcnow().isoformat()+'Z'
    return jsonify(ok=True, ran="quick", timestamp=last_quick, result=out)

@app.post("/cron/daily")
def cron_daily():
    global last_daily
    if not auth_ok(request):
        return jsonify(ok=False, error="unauthorized"), 401
    with lock:
        out = evaluate_and_act(kind="daily")
        import datetime as dt
        last_daily = dt.datetime.utcnow().isoformat()+'Z'
    return jsonify(ok=True, ran="daily", timestamp=last_daily, result=out)

@app.post("/cron/weekly")
def cron_weekly():
    global last_weekly
    if not auth_ok(request):
        return jsonify(ok=False, error="unauthorized"), 401
    # Only send on the configured weekday
    now = datetime.datetime.utcnow()
    if weekday_str(now) != DIGEST_DAY:
        return jsonify(ok=False, error=f"Not scheduled day (today is {weekday_str(now)}, digest day is {DIGEST_DAY})"), 400
    with lock:
        res = send_weekly_digest()
        last_weekly = datetime.datetime.utcnow().isoformat()+'Z'
    return jsonify(ok=True, ran="weekly", timestamp=last_weekly, result=res)

if __name__ == "__main__":
    load_playbook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
