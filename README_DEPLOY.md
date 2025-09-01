# Simple Cloud Agent (Starter) — Abducted Memories

Deploy this to Render / Fly.io / Cloud Run.

## Endpoints
- GET /health
- GET /dashboard/summary
- POST /playbook/reload
- POST /cron/quick  (every 15 min)
- POST /cron/daily  (daily 09:00)

Protect cron: set CRON_TOKEN and include it as header X-CRON-TOKEN or ?token=...

## Render (example)
- Create Web Service (Docker)
- Set env vars from `.env.sample`
- Add two Cron Jobs:
  - Every 15 min: POST /cron/quick?token=<your-token>
  - Daily 09:00: POST /cron/daily?token=<your-token>

## Cloud Run (example)
- `gcloud builds submit --tag gcr.io/<PROJECT>/simple-agent`
- `gcloud run deploy simple-agent --image gcr.io/<PROJECT>/simple-agent --allow-unauthenticated --region <REGION> --set-env-vars DRY_RUN=true,PLAYBOOK_PATH=./playbook/Abducted_Memories_Campaign_Playbook.json,CRON_TOKEN=<token>`
- Use Cloud Scheduler to POST to those endpoints on schedule.

## Remote playbook
- Host your JSON privately; set PLAYBOOK_URL. Call /playbook/reload to apply changes.

## Next steps
- Integrate connectors in `connectors/`.
- Add a database if you want persistent metrics/decisions.


## Dashboard & Weekly Digest
- Open `/dashboard` for a simple HTML dashboard.
- Configure SMTP in env to email a weekly digest (or it saves to `./outputs/digest_last.txt`).
- Add a weekly scheduler to POST `/cron/weekly?token=<token>` on your chosen weekday (env `DIGEST_DAY`).
