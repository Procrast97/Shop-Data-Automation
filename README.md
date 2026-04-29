# Shop Automation

A full-stack Flask web application that automates daily sales data collection, reporting, and database management for retail shop locations.

## What it does

- **Automated data extraction** — Uses Selenium to log into shop management portals and scrape daily sales data on a schedule
- **Web dashboard** — Lets users add/remove/amend shop URLs, locations, and individual sales items through a browser UI
- **Report generation** — Filters sales data by shop, location, and date range, then exports to formatted Excel or PDF
- **Automated email reports** — Sends daily sales summaries by email, including totals and flagging empty stores
- **Persistent storage** — All shop and sales data is stored in a SQLite database via SQLAlchemy

## Tech stack

- **Backend**: Python, Flask, Flask-Login, Flask-WTF, SQLAlchemy
- **Automation**: Selenium, webdriver-manager
- **Reporting**: openpyxl, ReportLab
- **Frontend**: Bootstrap 5 (via Bootstrap-Flask), Jinja2 templates
- **Scheduling**: APScheduler / schedule library

## Project structure

```
├── app.py              # Flask app factory and login manager setup
├── main.py             # Routes and scheduled automation task
├── DBModels.py         # SQLAlchemy database models
├── DataExtract.py      # Selenium scraper and email logic
├── ExcelFormatting.py  # Excel report builder
├── ExportBrain.py      # Export controller (Excel + PDF)
├── forms.py            # WTForms form definitions
├── scheduler.py        # Standalone scheduler entry point
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, images
└── Fonts/              # Custom fonts for PDF generation
```

## Setup

**1. Clone the repo**
```bash
git clone <repo-url>
cd shop-automation
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `FLASK_KEY` | Secret key for Flask sessions |
| `DB_URI` | SQLAlchemy database URI (default: `sqlite:///data.db`) |
| `ACCOUNT_EMAIL` | Login email for the shop portal |
| `ACCOUNT_PASSWORD` | Login password for the shop portal |
| `SYSTEM_EMAIL` | Gmail address used to send automated reports |
| `SYSTEM_PASSWORD` | Gmail App Password for the above account |
| `SEND_EMAIL` | Sender address for outgoing emails |
| `SEND_PASSWORD` | Password for the sender email account |

> **Note:** For Gmail, you must use an [App Password](https://support.google.com/accounts/answer/185833), not your regular account password.

**5. Initialise the database**
```bash
flask shell
>>> from app import app
>>> from DBModels import db
>>> with app.app_context():
...     db.create_all()
```

**6. Run the app**
```bash
python main.py
```

The app will be available at `http://127.0.0.1:5000`.

## Automated scheduling

The daily data extraction task is defined in `main.py` (`task()`) and can be enabled by uncommenting the scheduler block at the bottom of the file. The task:

1. Iterates over all registered shop URLs
2. Logs in via Selenium and scrapes today's sales
3. Generates and emails an Excel + PDF report
4. Persists the data to the database after a configurable cutoff time

## Notes

- Selenium requires Chrome and a matching ChromeDriver. The app uses `webdriver-manager` to handle this automatically in most environments.
- The chromedriver path in `DataExtract.py` is set for a Linux server (`/usr/bin/chromedriver`). Update this for your environment if needed.