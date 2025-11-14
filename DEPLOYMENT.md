# Deployment Guide for Job Search AI Agent

## Prerequisites

- Python 3.8+ installed
- Slack workspace with admin access
- (Optional) OpenAI API account

## Local Deployment

### 1. Clone and Setup

```bash
git clone https://github.com/rmallorybpc/didactic-octo-couscous.git
cd didactic-octo-couscous
./setup.sh
```

### 2. Configure Environment

Edit `.env` file with your credentials:

```bash
nano .env
```

Required settings:
- `SLACK_BOT_TOKEN` - Your Slack bot token (starts with xoxb-)
- `SLACK_CHANNEL` - Slack channel name (e.g., #all-the-mallory-group)

Optional settings:
- `OPENAI_API_KEY` - For enhanced profile analysis
- `MIN_SALARY` - Minimum salary filter (default: 130000)
- `SCHEDULE_TIME` - Daily run time in HH:MM format (default: 07:00)
- `TIMEZONE` - Timezone for scheduling (default: America/Denver)

### 3. Test the Agent

```bash
# Test without API keys
python demo.py

# Test with your API keys
python main.py --mode test

# Run once
python main.py --mode run-once
```

### 4. Start Scheduled Agent

```bash
# Run continuously with daily schedule
python main.py --mode schedule
```

## Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t job-search-agent .

# Run the container
docker run -d \
  --name job-search-agent \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  job-search-agent
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## Cloud Deployment Options

### Option 1: AWS EC2

1. Launch an EC2 instance (t2.micro is sufficient)
2. SSH into the instance
3. Clone the repository and run setup
4. Use `screen` or `tmux` to run the agent in background:

```bash
screen -S job-agent
python main.py --mode schedule
# Ctrl+A, D to detach
```

5. Or use systemd service (see below)

### Option 2: Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/YOUR_PROJECT/job-search-agent

# Deploy
gcloud run deploy job-search-agent \
  --image gcr.io/YOUR_PROJECT/job-search-agent \
  --platform managed \
  --region us-central1 \
  --set-env-vars "$(cat .env | xargs)"
```

### Option 3: Heroku

```bash
# Create Heroku app
heroku create job-search-agent

# Set environment variables
heroku config:set SLACK_BOT_TOKEN=your_token
heroku config:set SLACK_CHANNEL=#your-channel
# ... set other variables

# Deploy
git push heroku main
```

### Option 4: DigitalOcean Droplet

1. Create a droplet
2. SSH and setup
3. Use systemd service (see below)

## Systemd Service Setup (Linux)

Create `/etc/systemd/system/job-search-agent.service`:

```ini
[Unit]
Description=Job Search AI Agent
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/didactic-octo-couscous
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /path/to/didactic-octo-couscous/main.py --mode schedule
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable job-search-agent
sudo systemctl start job-search-agent
sudo systemctl status job-search-agent
```

## Cron Job Setup

Alternative to running continuously, use cron:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 7 AM)
0 7 * * * cd /path/to/didactic-octo-couscous && /usr/bin/python3 main.py --mode run-once >> /path/to/logs/cron.log 2>&1
```

## Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 7:00 AM
4. Set action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\main.py --mode run-once`
   - Start in: `C:\path\to\didactic-octo-couscous`

## Monitoring and Logs

### View Logs

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u job-search-agent -f

# Local
tail -f logs/*.log
```

### Check Job History

```bash
cat data/job_history.json
```

### Health Checks

Create a monitoring script:

```bash
#!/bin/bash
# check-agent.sh

if pgrep -f "main.py --mode schedule" > /dev/null; then
    echo "Agent is running"
    exit 0
else
    echo "Agent is not running"
    exit 1
fi
```

## Troubleshooting

### Agent not sending messages to Slack

1. Check Slack token is correct
2. Verify bot is invited to the channel
3. Check bot permissions include `chat:write`
4. Run test mode: `python main.py --mode test`

### No jobs found

1. Check internet connectivity
2. Verify search criteria in `.env`
3. Review logs for errors
4. Test with demo: `python demo.py`

### Jobs not being filtered correctly

1. Check `MIN_SALARY` in `.env`
2. Verify location filters match your needs
3. Review job history: `cat data/job_history.json`

### Agent crashes

1. Check logs for error messages
2. Ensure all dependencies are installed
3. Verify Python version is 3.8+
4. Test in demo mode first

## Backup and Maintenance

### Backup Job History

```bash
# Create backup
cp data/job_history.json data/job_history.backup.json

# Scheduled backup (add to cron)
0 0 * * 0 cp /path/to/data/job_history.json /path/to/backups/job_history.$(date +\%Y\%m\%d).json
```

### Clear Job History

```bash
# Clear old entries (keeps last 30 days)
# This happens automatically, but you can force it:
python -c "from src.utils.job_history import JobHistory; jh = JobHistory('data/job_history.json'); jh.cleanup_old_entries(30)"
```

### Update Agent

```bash
git pull origin main
pip install -r requirements.txt
# Restart service
sudo systemctl restart job-search-agent
```

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive API keys
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Limit bot permissions** to only what's needed
5. **Use HTTPS** for any web interfaces
6. **Keep dependencies updated**: `pip install -U -r requirements.txt`

## Scaling Considerations

- For multiple profiles: Run multiple instances with different `.env` files
- For multiple channels: Modify `SLACK_CHANNEL` or run multiple instances
- For high volume: Consider using a job queue (Celery, RQ)
- For analytics: Export job data to a database

## Cost Estimates

- **AWS EC2 (t2.micro)**: ~$8-10/month
- **DigitalOcean Droplet**: ~$5-10/month
- **Google Cloud Run**: ~$0-5/month (free tier)
- **Heroku**: $7/month (Eco dyno)
- **Slack**: Free (standard workspace)
- **OpenAI API**: Optional, ~$0-5/month for this use case
