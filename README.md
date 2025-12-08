# Votações Assembleia da República

Small utility that scrapes the Portuguese Parliament "Arquivo de votações" page, downloads the latest voting results PDF and emails it to one or more recipients.

## Files
- `script.py` — main script
- `.gitignore` — ignores `.env`
- `last_url.txt` — created at runtime to avoid re-sending same PDF
- `README.md`, `LICENSE` — this project docs & license

## Requirements
- Python 3.8+
- pip
- Internet access
- SMTP account that allows programmatic login

Python packages (used by the script):
- requests
- beautifulsoup4
- python-dotenv

Install:
```powershell
python -m pip install -r 