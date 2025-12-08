# Votações Assembleia da República

Small utility that scrapes the Portuguese Parliament "Arquivo de votações" page, downloads the latest voting results PDF and emails it to one or more recipients.

## Purpose
This repo is intended to run inside a Docker container (suitable for Raspberry Pi 5 / ARM64) so the script can run reliably as a service or scheduled job.

## Files
- `script.py` — main script
- `Dockerfile` — builds the runtime image (ARM64 compatible)
- `docker-compose.yml` — optional convenience for running the container
- `requirements.txt` — Python dependencies
- `.env` — (ignored) environment variables for credentials
- `.gitignore`, `LICENSE`, `last_url.txt`

## Requirements (host)
- Raspberry Pi 5 with Docker installed
- Docker Compose (optional)
- Internet access

## Configuration
Create a `.env` file in the project root with EMAIL_SENDER, EMAIL_PASSWORD and EMAIL_RECEIVER. First two must be strings and last must be a list of strings.

The container will expect these env vars (same names used by the script).

## Build and run (recommended for Raspberry Pi 5 / ARM64)

1. Build the image (ensure ARM64 platform):
```bash
docker build --platform linux/arm64 -t votacoes_ar:latest .

```bash
docker run -d voting_job:voting
```

## Crontab

Edit the * in crontab file to receive the email in specific schedules