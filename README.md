# Castaways 🍦

A website and admin dashboard for an ice cream shop: a customer-facing homepage plus a behind-the-counter system for tracking inventory, sales and feedback.

---

## ✨ Features

**For customers**
- Homepage showing the shop's ice cream flavors and which ones are currently available
- Feedback form

**For staff (admin dashboard)**
- Sales analytics with charts, including history over time
- Inventory management for ice cream flavors, add-ons and supplies: add, edit and delete entries
- Automatic daily and monthly inventory resets
- Feedback inbox with read/unread tracking
- Login with lockout after too many failed attempts, plus session timeouts

## 🧰 Built with

- Python + [Flask](https://flask.palletsprojects.com/)
- SQLite
- Bootstrap (SB Admin 2 theme), Chart.js, Font Awesome
- Gunicorn, ready for Heroku-style deployment (`Procfile`)

## 🚀 Run it locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:8000. The admin dashboard is at `/login`.

The admin login comes from environment variables: `ADMIN_USERNAME` and `ADMIN_PASSWORD` (the demo defaults are `admin` / `demo`). See `.env.example` and `DEPLOYMENT_GUIDE.md`.

> The included database uses demo employee names and sample feedback.
