#!/bin/bash
# ──────────────────────────────────────────────────────────────
# AI News Digest — Cron Job Setup Script
# Run this on your KVM2 Ubuntu server to schedule the daily digest.
# ──────────────────────────────────────────────────────────────

set -e

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🤖 AI News Digest — Cron Setup"
echo "================================"
echo ""
echo "Script directory: $SCRIPT_DIR"
echo ""

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Install it first:"
    echo "   sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "   ✓ Virtual environment created"
fi

# Install dependencies
echo "📦 Installing dependencies..."
"$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" --quiet
echo "   ✓ Dependencies installed"

# Check if .env exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo ""
    echo "⚠  .env file not found! Creating from template..."
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    echo "   → Edit $SCRIPT_DIR/.env and add your Gmail App Password"
    echo "   → Then run this script again."
    exit 1
fi

# Set timezone
echo ""
echo "🕐 Setting timezone to Asia/Karachi..."
sudo timedatectl set-timezone Asia/Karachi 2>/dev/null || echo "   ⚠ Could not set timezone (non-critical)"

# Build the cron command
CRON_CMD="0 10 * * * cd $SCRIPT_DIR && $SCRIPT_DIR/venv/bin/python main.py >> $SCRIPT_DIR/digest.log 2>&1"

# Check if cron job already exists
EXISTING=$(crontab -l 2>/dev/null | grep "ai-news.*main.py" || true)
if [ -n "$EXISTING" ]; then
    echo "⚠  Existing cron job found. Replacing..."
    crontab -l 2>/dev/null | grep -v "ai-news.*main.py" | crontab -
fi

# Add the cron job
echo ""
echo "⏰ Adding cron job (10:00 AM PKT daily)..."
(crontab -l 2>/dev/null; echo "# AI News Digest — daily at 10:00 AM PKT") | crontab -
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
echo "   ✓ Cron job added!"

# Verify
echo ""
echo "📋 Current cron jobs:"
crontab -l 2>/dev/null | tail -2
echo ""

echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Commands:"
echo "  Test run:     cd $SCRIPT_DIR && venv/bin/python main.py --dry-run"
echo "  Test email:   cd $SCRIPT_DIR && venv/bin/python main.py --test"
echo "  Full run:     cd $SCRIPT_DIR && venv/bin/python main.py"
echo "  View logs:    tail -f $SCRIPT_DIR/digest.log"
echo ""
