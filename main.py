#!/usr/bin/env python3
"""
Job Search AI Agent - Main Entry Point

This agent searches for senior HR job postings daily and sends reports to Slack.
"""
import sys
import argparse
from src.scheduler import JobSearchScheduler
from src.orchestrator import JobSearchOrchestrator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Job Search AI Agent - Automated job search and Slack notifications'
    )
    parser.add_argument(
        '--mode',
        choices=['schedule', 'run-once', 'test'],
        default='run-once',
        help='Execution mode: schedule (run daily at 7 AM MT), run-once (run immediately), test (test connections)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'schedule':
            logger.info("Starting in SCHEDULE mode - will run daily at 7:00 AM MT")
            scheduler = JobSearchScheduler()
            scheduler.start()
            
        elif args.mode == 'run-once':
            logger.info("Starting in RUN-ONCE mode - executing immediately")
            scheduler = JobSearchScheduler()
            scheduler.run_once()
            
        elif args.mode == 'test':
            logger.info("Starting in TEST mode - checking connections")
            orchestrator = JobSearchOrchestrator()
            orchestrator.test_connection()
            
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
