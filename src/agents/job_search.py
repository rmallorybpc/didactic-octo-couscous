"""
Job Search Agent - Searches multiple sources for job postings
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from datetime import datetime
import time
import re
from src.utils.logger import setup_logger
from src.config import MIN_SALARY, LOCATIONS

logger = setup_logger(__name__)

class JobSearchAgent:
    """Search for job postings from multiple sources"""
    
    def __init__(self):
        """Initialize job search agent"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_jobs(self, job_title: str, keywords: List[str], profile_data: Dict) -> List[Dict]:
        """
        Search for jobs across multiple sources.
        
        Args:
            job_title: Job title to search for
            keywords: Additional keywords from profile
            profile_data: Profile data for matching
            
        Returns:
            List of job postings
        """
        logger.info(f"Searching for: {job_title}")
        
        all_jobs = []
        
        # Search each source
        all_jobs.extend(self._search_linkedin(job_title, keywords))
        all_jobs.extend(self._search_indeed(job_title, keywords))
        all_jobs.extend(self._search_glassdoor(job_title, keywords))
        
        logger.info(f"Found {len(all_jobs)} total jobs for {job_title}")
        
        return all_jobs
    
    def _search_linkedin(self, job_title: str, keywords: List[str]) -> List[Dict]:
        """
        Search LinkedIn for jobs.
        
        Note: This is a simulated search. In production, you would use:
        - LinkedIn API (if available)
        - Web scraping with Selenium
        - Third-party job search APIs
        
        Args:
            job_title: Job title to search
            keywords: Search keywords
            
        Returns:
            List of job postings from LinkedIn
        """
        logger.info(f"Searching LinkedIn for: {job_title}")
        
        # Simulated LinkedIn jobs for demonstration
        jobs = [
            {
                'title': job_title.title(),
                'company': 'Tech Innovators Inc',
                'location': 'Remote',
                'salary_range': '$150,000 - $180,000',
                'url': f'https://www.linkedin.com/jobs/view/{hash(job_title + "1") % 10000000}',
                'source': 'LinkedIn',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'description': f'Leading {job_title} role with focus on HR Strategy, Talent Management, Organizational Development, Employee Relations, Change Management, Leadership Development, Performance Management, Compensation Benefits, HR Analytics, People Operations, Culture Transformation, Talent Acquisition, HRIS Systems, Compliance, Employee Engagement, Diversity Inclusion, Workforce Planning. SPHR certification required. Remote position with competitive compensation.',
                'easy_apply': True,
                'active': True  # Will be verified
            },
            {
                'title': job_title.title(),
                'company': 'Mountain View Solutions',
                'location': 'Denver, CO',
                'salary_range': '$140,000 - $170,000',
                'url': f'https://www.linkedin.com/jobs/view/{hash(job_title + "2") % 10000000}',
                'source': 'LinkedIn',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'description': f'{job_title} position focused on People Operations, Employee Relations, Culture Transformation, HR Strategy, Talent Management, Organizational Development, Leadership Development, Performance Management, HR Analytics, Employee Engagement, Diversity Inclusion, Executive Coaching. Based in Denver with flexible work options. SPHR or equivalent certification preferred.',
                'easy_apply': True,
                'active': True
            }
        ]
        
        return jobs
    
    def _search_indeed(self, job_title: str, keywords: List[str]) -> List[Dict]:
        """
        Search Indeed for jobs.
        
        Args:
            job_title: Job title to search
            keywords: Search keywords
            
        Returns:
            List of job postings from Indeed
        """
        logger.info(f"Searching Indeed for: {job_title}")
        
        # Simulated Indeed jobs for demonstration
        jobs = [
            {
                'title': job_title.title(),
                'company': 'Colorado Health Systems',
                'location': 'Remote',
                'salary_range': '$135,000 - $165,000',
                'url': f'https://www.indeed.com/viewjob?jk={hash(job_title + "indeed1")}',
                'source': 'Indeed',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'description': f'Seeking experienced {job_title} with expertise in HR Analytics, Performance Management, Leadership Development, Talent Management, HR Strategy, Organizational Development, Employee Relations, People Operations, Compensation Benefits, Workforce Planning, Talent Acquisition, HRIS Systems. Healthcare industry experience preferred.',
                'easy_apply': True,
                'active': True
            }
        ]
        
        return jobs
    
    def _search_glassdoor(self, job_title: str, keywords: List[str]) -> List[Dict]:
        """
        Search Glassdoor for jobs.
        
        Args:
            job_title: Job title to search
            keywords: Search keywords
            
        Returns:
            List of job postings from Glassdoor
        """
        logger.info(f"Searching Glassdoor for: {job_title}")
        
        # Simulated Glassdoor jobs for demonstration
        jobs = [
            {
                'title': job_title.title(),
                'company': 'Financial Services Group',
                'location': 'Boulder, CO',
                'salary_range': '$145,000 - $175,000',
                'url': f'https://www.glassdoor.com/job-listing/{hash(job_title + "glass1")}',
                'source': 'Glassdoor',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'description': f'{job_title} role with emphasis on Talent Acquisition, Workforce Planning, Employee Engagement, HR Strategy, Organizational Development, Talent Management, Change Management, Leadership Development, Performance Management, HR Analytics, Culture Transformation, Diversity Inclusion, HRIS Systems, Compliance. Finance industry background a plus.',
                'easy_apply': True,
                'active': True
            }
        ]
        
        return jobs
    
    def verify_linkedin_job_active(self, job_url: str) -> bool:
        """
        Verify that a LinkedIn job is still accepting applications.
        
        Args:
            job_url: LinkedIn job URL
            
        Returns:
            True if job is active, False if "No longer accepting applications"
        """
        # In production, this would actually visit the URL and check
        # For this implementation, we'll simulate it
        logger.info(f"Verifying job status: {job_url}")
        
        # Simulate that most jobs are active
        # In production, you would:
        # 1. Use Selenium to load the page
        # 2. Check for "No longer accepting applications" text
        # 3. Return False if found, True otherwise
        
        return True  # Simulated as active
    
    def filter_jobs(self, jobs: List[Dict], profile_data: Dict) -> List[Dict]:
        """
        Filter jobs based on criteria.
        
        Args:
            jobs: List of job postings
            profile_data: Profile data for filtering
            
        Returns:
            Filtered list of jobs
        """
        filtered_jobs = []
        
        for job in jobs:
            # Check salary requirement
            if not self._meets_salary_requirement(job):
                continue
            
            # Check location requirement
            if not self._meets_location_requirement(job):
                continue
            
            # Verify LinkedIn jobs are still active
            if job.get('source') == 'LinkedIn':
                if not self.verify_linkedin_job_active(job.get('url', '')):
                    job['active'] = False
                    continue
            
            # Check easy apply
            if not job.get('easy_apply', False):
                continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _meets_salary_requirement(self, job: Dict) -> bool:
        """Check if job meets minimum salary requirement"""
        salary_range = job.get('salary_range', '')
        
        # If no salary posted, keep the job
        if not salary_range or salary_range == 'Not specified':
            return True
        
        # Extract minimum salary from range
        numbers = re.findall(r'\$?([\d,]+)', salary_range)
        if numbers:
            try:
                min_salary = int(numbers[0].replace(',', ''))
                return min_salary >= MIN_SALARY
            except ValueError:
                return True  # Keep if we can't parse
        
        return True  # Keep if we can't determine
    
    def _meets_location_requirement(self, job: Dict) -> bool:
        """Check if job meets location requirement"""
        location = job.get('location', '').lower()
        
        # Check if remote or Colorado
        return any(loc.lower() in location for loc in LOCATIONS)
