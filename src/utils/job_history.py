"""
Job history tracking module to prevent duplicate job postings
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Set
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class JobHistory:
    """Track previously sent job postings to avoid duplicates"""
    
    def __init__(self, history_file: str):
        """
        Initialize job history tracker.
        
        Args:
            history_file: Path to JSON file storing job history
        """
        self.history_file = history_file
        self.history = self._load_history()
        
    def _load_history(self) -> Dict:
        """Load job history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading job history: {e}")
                return {'jobs': [], 'last_cleanup': datetime.now().isoformat()}
        return {'jobs': [], 'last_cleanup': datetime.now().isoformat()}
    
    def _save_history(self):
        """Save job history to file"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving job history: {e}")
    
    def is_duplicate(self, job_url: str, posting_date: str = None) -> bool:
        """
        Check if a job has been previously reported.
        
        Args:
            job_url: URL of the job posting
            posting_date: Optional posting date
            
        Returns:
            True if job is a duplicate, False otherwise
        """
        for job in self.history.get('jobs', []):
            if job.get('url') == job_url:
                return True
        return False
    
    def add_job(self, job_url: str, posting_date: str = None):
        """
        Add a job to the history.
        
        Args:
            job_url: URL of the job posting
            posting_date: Optional posting date
        """
        if not self.is_duplicate(job_url):
            self.history['jobs'].append({
                'url': job_url,
                'posting_date': posting_date,
                'reported_date': datetime.now().isoformat()
            })
            self._save_history()
    
    def add_jobs_batch(self, job_urls: List[str]):
        """
        Add multiple jobs to history.
        
        Args:
            job_urls: List of job URLs to add
        """
        for url in job_urls:
            if not self.is_duplicate(url):
                self.history['jobs'].append({
                    'url': url,
                    'reported_date': datetime.now().isoformat()
                })
        self._save_history()
    
    def cleanup_old_entries(self, days: int = 30):
        """
        Remove job entries older than specified days.
        
        Args:
            days: Number of days to keep history
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered_jobs = []
        for job in self.history.get('jobs', []):
            reported_date = datetime.fromisoformat(job.get('reported_date', datetime.now().isoformat()))
            if reported_date > cutoff_date:
                filtered_jobs.append(job)
        
        removed_count = len(self.history.get('jobs', [])) - len(filtered_jobs)
        self.history['jobs'] = filtered_jobs
        self.history['last_cleanup'] = datetime.now().isoformat()
        self._save_history()
        
        logger.info(f"Cleaned up {removed_count} old job entries")
    
    def get_stats(self) -> Dict:
        """Get statistics about job history"""
        return {
            'total_jobs': len(self.history.get('jobs', [])),
            'last_cleanup': self.history.get('last_cleanup', 'Never')
        }
