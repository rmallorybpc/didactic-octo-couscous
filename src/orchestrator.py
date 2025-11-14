"""
Main Job Search Agent Orchestrator
"""
from typing import Dict, List
from src.agents.profile_analyzer import ProfileAnalyzer
from src.agents.job_search import JobSearchAgent
from src.agents.job_compiler import JobCompiler
from src.agents.slack_notifier import SlackNotifier
from src.utils.job_history import JobHistory
from src.utils.logger import setup_logger
from src.config import JOB_TITLES, JOB_HISTORY_FILE

logger = setup_logger(__name__)

class JobSearchOrchestrator:
    """Main orchestrator for the job search AI agent"""
    
    def __init__(self):
        """Initialize the orchestrator with all agents"""
        logger.info("Initializing Job Search Orchestrator")
        
        self.profile_analyzer = ProfileAnalyzer()
        self.job_search_agent = JobSearchAgent()
        self.job_compiler = JobCompiler(self.profile_analyzer)
        self.slack_notifier = SlackNotifier()
        self.job_history = JobHistory(JOB_HISTORY_FILE)
    
    def run_daily_search(self) -> Dict:
        """
        Run the complete daily job search workflow.
        
        Returns:
            Report dictionary with results
        """
        logger.info("=" * 80)
        logger.info("Starting Daily Job Search")
        logger.info("=" * 80)
        
        # Step 1: Analyze LinkedIn profile
        logger.info("Step 1: Analyzing LinkedIn profile")
        profile_data = self.profile_analyzer.analyze_profile()
        search_keywords = self.profile_analyzer.get_search_keywords(profile_data)
        
        # Step 2: Search for jobs
        logger.info("Step 2: Searching for jobs")
        all_jobs = []
        
        for job_title in JOB_TITLES:
            jobs = self.job_search_agent.search_jobs(
                job_title.strip(),
                search_keywords,
                profile_data
            )
            all_jobs.extend(jobs)
        
        logger.info(f"Found {len(all_jobs)} total jobs before filtering")
        
        # Step 3: Filter jobs
        logger.info("Step 3: Filtering jobs")
        filtered_jobs = self.job_search_agent.filter_jobs(all_jobs, profile_data)
        logger.info(f"After filtering: {len(filtered_jobs)} jobs")
        
        # Step 4: Remove duplicates from previous days
        logger.info("Step 4: Checking for duplicate jobs")
        new_jobs = []
        duplicate_count = 0
        
        for job in filtered_jobs:
            if not self.job_history.is_duplicate(job.get('url', '')):
                new_jobs.append(job)
            else:
                duplicate_count += 1
        
        logger.info(f"Found {len(new_jobs)} new jobs ({duplicate_count} duplicates excluded)")
        
        # Count excluded jobs
        inactive_count = len([j for j in all_jobs if not j.get('active', True)])
        total_filtered_out = len(all_jobs) - len(filtered_jobs)
        low_salary_count = max(0, total_filtered_out - inactive_count - duplicate_count)
        
        # Step 5: Compile report
        logger.info("Step 5: Compiling job report")
        report = self.job_compiler.compile_jobs(
            new_jobs,
            profile_data,
            duplicate_count,
            inactive_count,
            low_salary_count
        )
        
        # Step 6: Send to Slack
        logger.info("Step 6: Sending report to Slack")
        success = self.slack_notifier.send_report(report)
        
        # Step 7: Update job history
        if success and new_jobs:
            logger.info("Step 7: Updating job history")
            job_urls = [job.get('url') for job in new_jobs if job.get('url')]
            self.job_history.add_jobs_batch(job_urls)
        
        # Step 8: Cleanup old entries (keep 30 days)
        self.job_history.cleanup_old_entries(days=30)
        
        logger.info("=" * 80)
        logger.info(f"Daily Job Search Complete - Found {len(new_jobs)} new jobs")
        logger.info("=" * 80)
        
        return report
    
    def test_connection(self):
        """Test all connections and configurations"""
        logger.info("Testing connections...")
        
        # Test profile analysis
        try:
            profile_data = self.profile_analyzer.analyze_profile()
            logger.info(f"✓ Profile analysis working - Found {len(profile_data.get('skills', []))} skills")
        except Exception as e:
            logger.error(f"✗ Profile analysis failed: {e}")
        
        # Test job search
        try:
            test_jobs = self.job_search_agent.search_jobs(
                "test position",
                ["test"],
                {}
            )
            logger.info(f"✓ Job search working - Found {len(test_jobs)} test jobs")
        except Exception as e:
            logger.error(f"✗ Job search failed: {e}")
        
        # Test Slack connection
        try:
            if self.slack_notifier.send_test_message():
                logger.info("✓ Slack connection working")
            else:
                logger.warning("⚠ Slack connection not configured")
        except Exception as e:
            logger.error(f"✗ Slack connection failed: {e}")
        
        # Test job history
        try:
            stats = self.job_history.get_stats()
            logger.info(f"✓ Job history working - {stats['total_jobs']} jobs tracked")
        except Exception as e:
            logger.error(f"✗ Job history failed: {e}")
