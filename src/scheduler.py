"""
Scheduler for the Job Search AI Agent
"""
import schedule
import time
import pytz
from datetime import datetime
from src.orchestrator import JobSearchOrchestrator
from src.utils.logger import setup_logger
from src.config import SCHEDULE_TIME, TIMEZONE

logger = setup_logger(__name__)

class JobSearchScheduler:
    """Schedule and run the job search agent"""
    
    def __init__(self):
        """Initialize the scheduler"""
        self.orchestrator = JobSearchOrchestrator()
        self.timezone = pytz.timezone(TIMEZONE)
    
    def run_scheduled_job(self):
        """Run the job search and handle any errors"""
        try:
            logger.info(f"Running scheduled job at {datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S %Z')}")
            self.orchestrator.run_daily_search()
        except Exception as e:
            logger.error(f"Error running scheduled job: {e}", exc_info=True)
    
    def start(self):
        """Start the scheduler with daily job at specified time"""
        logger.info(f"Starting Job Search Scheduler")
        logger.info(f"Scheduled to run daily at {SCHEDULE_TIME} {TIMEZONE}")
        
        # Schedule the job
        schedule.every().day.at(SCHEDULE_TIME).do(self.run_scheduled_job)
        
        # Print next run time
        next_run = schedule.next_run()
        logger.info(f"Next run scheduled for: {next_run}")
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
    
    def run_once(self):
        """Run the job search once immediately"""
        logger.info("Running job search once (immediate execution)")
        self.run_scheduled_job()
