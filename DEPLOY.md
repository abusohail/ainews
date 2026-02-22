# 🤖 AI News Digest — Deployment Guide

Step-by-step guide to deploy on your KVM2 Ubuntu server.

---

## Prerequisites

- Ubuntu server (KVM2 hosting)
- Python 3.8+ installed
- Gmail account with 2-Step Verification enabled

---

## Step 1: Generate Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already)
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select **"Mail"** → click **"Generate"**
5. Copy the **16-character password** (e.g., `abcd efgh ijkl mnop`)

---

## Step 2: Upload Project to Server

From your local machine:

```bash
# Option A: SCP (replace with your server IP)
scp -r "AI News" user@your-server-ip:/home/user/ai-news

# Option B: Git (if using a repo)
ssh user@your-server-ip
git clone https://your-repo-url.git ai-news
```

---

## Step 3: Configure

```bash
cd /home/user/ai-news

# Create .env from template
cp .env.example .env

# Edit .env and paste your Gmail App Password
nano .env
```

Your `.env` should look like:
```
GMAIL_ADDRESS=abusohail09@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

---

## Step 4: Run Setup Script

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

This will:
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Set timezone to Asia/Karachi
- ✅ Add a cron job for 10:00 AM daily

---

## Step 5: Test

```bash
# Dry run (collect data but don't send email)
cd /home/user/ai-news
venv/bin/python main.py --dry-run

# Send a test email with sample data
venv/bin/python main.py --test

# Full run (collect + send)
venv/bin/python main.py
```

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `venv/bin/python main.py` | Run full pipeline |
| `venv/bin/python main.py --dry-run` | Collect & rank without emailing |
| `venv/bin/python main.py --test` | Send test email with sample data |
| `tail -f digest.log` | Watch live logs |
| `crontab -l` | View scheduled jobs |
| `crontab -e` | Edit cron schedule |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Gmail auth fails | Use App Password, not regular password |
| No data collected | Check internet connectivity on server |
| Cron not running | Check `crontab -l` and timezone (`timedatectl`) |
| Missing Python | `sudo apt install python3 python3-pip python3-venv` |

---

## Customization

Edit `config.py` to:
- Add/remove subreddits
- Change AI keyword filters
- Adjust minimum score thresholds
- Add YouTube channels
- Change email recipient
