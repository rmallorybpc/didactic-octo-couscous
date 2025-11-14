"""
Configuration module for the Job Search AI Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Slack Configuration
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#all-the-mallory-group')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# LinkedIn Profile
LINKEDIN_PROFILE_URL = os.getenv(
    'LINKEDIN_PROFILE_URL',
    'https://www.linkedin.com/in/theresa-mcdonald-mallory-sphr/'
)

# Job Search Configuration
MIN_SALARY = int(os.getenv('MIN_SALARY', '130000'))
JOB_TITLES = os.getenv(
    'JOB_TITLES',
    'head of people and culture,chief people officer,vp of human resources,human resources director'
).split(',')

# Scheduler Configuration
SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', '07:00')
TIMEZONE = os.getenv('TIMEZONE', 'America/Denver')

# Job History File
JOB_HISTORY_FILE = os.getenv('JOB_HISTORY_FILE', 'data/job_history.json')

# Search Configuration
SEARCH_SOURCES = ['linkedin', 'indeed', 'glassdoor']
LOCATIONS = ['remote', 'Colorado']
