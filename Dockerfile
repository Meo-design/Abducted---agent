FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Recommended env
ENV PYTHONUNBUFFERED=1

# Render sets $PORT dynamically, so bind to it
EXPOSE 8080
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:${PORT}"]
