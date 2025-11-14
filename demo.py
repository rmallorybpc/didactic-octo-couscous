#!/usr/bin/env python3
"""
Demo script to test the Job Search AI Agent without requiring API keys
"""
import sys
import os

# Set demo environment variables
os.environ['SLACK_BOT_TOKEN'] = ''  # Empty to use console output
os.environ['OPENAI_API_KEY'] = ''   # Empty to use default profile
os.environ['SLACK_CHANNEL'] = '#all-the-mallory-group'

from src.orchestrator import JobSearchOrchestrator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Run a demo of the job search agent"""
    logger.info("=" * 80)
    logger.info("JOB SEARCH AI AGENT - DEMO MODE")
    logger.info("=" * 80)
    logger.info("Running without API keys - using simulated data")
    logger.info("")
    
    try:
        # Initialize orchestrator
        orchestrator = JobSearchOrchestrator()
        
        # Run the job search
        report = orchestrator.run_daily_search()
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("DEMO COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total jobs found: {report['stats']['total_jobs']}")
        logger.info(f"High match jobs: {report['stats']['high_match']}")
        logger.info(f"Medium match jobs: {report['stats']['medium_match']}")
        logger.info(f"Low match jobs: {report['stats']['low_match']}")
        logger.info("")
        logger.info("The report has been printed to console (Slack not configured)")
        logger.info("")
        logger.info("To use with real data:")
        logger.info("1. Copy .env.example to .env")
        logger.info("2. Add your SLACK_BOT_TOKEN and OPENAI_API_KEY")
        logger.info("3. Run: python main.py --mode run-once")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
