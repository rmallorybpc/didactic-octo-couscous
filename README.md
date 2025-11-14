# Job Search AI Agent 🤖

An intelligent AI agent that automatically searches for senior HR job postings and sends daily reports to Slack.

## Overview

This agent performs daily searches across multiple job platforms (LinkedIn, Indeed, Glassdoor) to find relevant job postings for senior HR positions. It analyzes a LinkedIn profile to understand skills and experience, matches jobs based on this profile, filters out duplicates and inactive postings, and delivers a comprehensive report to Slack.

## Features

✅ **Automated Daily Searches** - Runs at 7:00 AM Mountain Time every day  
✅ **Profile-Based Matching** - Analyzes LinkedIn profile for skill alignment  
✅ **Multi-Source Aggregation** - Searches LinkedIn, Indeed, and Glassdoor  
✅ **Smart Filtering** - Removes duplicates, inactive jobs, and low-salary positions  
✅ **Location Focus** - Prioritizes remote and Colorado-based opportunities  
✅ **Salary Filtering** - Excludes jobs below $130,000  
✅ **Active Job Verification** - Checks that jobs are still accepting applications  
✅ **Top Recommendations** - Highlights 10-15 best matches with explanations  
✅ **Slack Integration** - Delivers clean, formatted reports to your Slack channel

## Job Titles Searched

- Head of People and Culture
- Chief People Officer
- VP of Human Resources
- Human Resources Director

## Requirements

- Python 3.8 or higher
- Slack workspace with bot token
- OpenAI API key (optional, for enhanced profile analysis)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/rmallorybpc/didactic-octo-couscous.git
cd didactic-octo-couscous
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-actual-slack-bot-token
SLACK_CHANNEL=#all-the-mallory-group

# OpenAI Configuration (optional)
OPENAI_API_KEY=your-openai-api-key

# LinkedIn Profile URL
LINKEDIN_PROFILE_URL=https://www.linkedin.com/in/theresa-mcdonald-mallory-sphr/

# Job Search Configuration
MIN_SALARY=130000
JOB_TITLES=head of people and culture,chief people officer,vp of human resources,human resources director

# Scheduler Configuration
SCHEDULE_TIME=07:00
TIMEZONE=America/Denver

# Job History File
JOB_HISTORY_FILE=data/job_history.json
```

## Usage

### Run Once (Immediate Execution)
Execute the job search immediately:
```bash
python main.py --mode run-once
```

### Schedule Daily Runs
Start the scheduler to run automatically at 7:00 AM MT:
```bash
python main.py --mode schedule
```

### Test Connections
Verify that all integrations are working:
```bash
python main.py --mode test
```

## Setting Up Slack Bot

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app or use an existing one
3. Navigate to "OAuth & Permissions"
4. Add the following bot token scopes:
   - `chat:write`
   - `chat:write.public`
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token" (starts with `xoxb-`)
7. Add the token to your `.env` file
8. Invite the bot to your Slack channel:
   ```
   /invite @YourBotName
   ```

## Report Format

The agent sends three types of messages to Slack:

### 1. Summary Message
- Total new jobs found
- Skill match breakdown (high/medium/low)
- Remote vs Colorado positions
- Search filters applied
- Jobs excluded (duplicates, inactive, low salary)

### 2. Top Recommendations (10-15 jobs)
- Job title and company
- Match quality indicator (🟢 🟡 🔴)
- Location and salary
- Direct application link
- Explanation of why it matches your profile

### 3. Complete Job List
- All jobs sorted by match quality
- Full details for each position
- Direct application links

## Architecture

```
src/
├── agents/
│   ├── profile_analyzer.py    # LinkedIn profile analysis
│   ├── job_search.py          # Multi-source job searching
│   ├── job_compiler.py        # Job formatting and compilation
│   └── slack_notifier.py      # Slack integration
├── utils/
│   ├── logger.py              # Logging utilities
│   └── job_history.py         # Duplicate detection
├── config.py                  # Configuration management
├── orchestrator.py            # Main workflow orchestration
└── scheduler.py               # Daily scheduling
```

## Job Filtering Criteria

The agent applies multiple filters to ensure quality results:

1. **Salary Filter**: Minimum $130,000 (keeps jobs without posted salary)
2. **Location Filter**: Remote or Colorado only
3. **Active Status**: Verifies jobs are still accepting applications
4. **Easy Apply**: Only includes jobs with easy apply option
5. **Duplicate Detection**: Tracks previously reported jobs
6. **Skill Match**: Scores based on profile alignment

## Job History

The agent maintains a history of all reported jobs in `data/job_history.json` to prevent sending duplicates. This file:
- Tracks all previously sent job URLs
- Records when each job was reported
- Automatically cleans up entries older than 30 days

## Troubleshooting

### Slack messages not sending
- Verify your `SLACK_BOT_TOKEN` is correct
- Ensure the bot is invited to the channel
- Check that the bot has `chat:write` permissions

### No jobs found
- Check that your search criteria aren't too restrictive
- Verify internet connectivity
- Review logs for any errors

### Profile analysis fails
- Ensure `LINKEDIN_PROFILE_URL` is correct
- Check if `OPENAI_API_KEY` is set (if using AI analysis)

## Development

### Running Tests
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests (when test suite is added)
pytest
```

### Adding New Job Sources
To add a new job search source:
1. Add a new method to `src/agents/job_search.py`
2. Follow the pattern of existing search methods
3. Return job dictionaries with the standard format

### Customizing Job Titles
Edit the `JOB_TITLES` variable in `.env`:
```env
JOB_TITLES=title1,title2,title3
```

## Deployment

### Using Cron (Linux/Mac)
```bash
# Run daily at 7:00 AM
0 7 * * * cd /path/to/didactic-octo-couscous && /usr/bin/python3 main.py --mode run-once
```

### Using Task Scheduler (Windows)
1. Open Task Scheduler
2. Create a new task
3. Set trigger to daily at 7:00 AM
4. Set action to run `python main.py --mode run-once`

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py", "--mode", "schedule"]
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.