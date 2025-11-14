"""
Job Compiler - Formats and compiles job postings into reports
"""
from typing import Dict, List
from datetime import datetime
from src.utils.logger import setup_logger
from src.agents.profile_analyzer import ProfileAnalyzer

logger = setup_logger(__name__)

class JobCompiler:
    """Compile and format job postings into reports"""
    
    def __init__(self, profile_analyzer: ProfileAnalyzer):
        """
        Initialize job compiler.
        
        Args:
            profile_analyzer: Profile analyzer for skill matching
        """
        self.profile_analyzer = profile_analyzer
    
    def compile_jobs(
        self,
        jobs: List[Dict],
        profile_data: Dict,
        duplicate_count: int = 0,
        inactive_count: int = 0,
        low_salary_count: int = 0
    ) -> Dict:
        """
        Compile jobs into a formatted report.
        
        Args:
            jobs: List of job postings
            profile_data: Profile data for skill matching
            duplicate_count: Number of duplicate jobs excluded
            inactive_count: Number of inactive jobs excluded
            low_salary_count: Number of jobs excluded due to low salary
            
        Returns:
            Compiled report dictionary
        """
        logger.info(f"Compiling {len(jobs)} jobs into report")
        
        # Score and sort jobs
        scored_jobs = self._score_jobs(jobs, profile_data)
        sorted_jobs = self._sort_jobs(scored_jobs)
        
        # Get top recommendations
        top_jobs = sorted_jobs[:15]  # Top 10-15 jobs
        
        # Generate summary
        summary = self._generate_summary(
            sorted_jobs,
            profile_data,
            duplicate_count,
            inactive_count,
            low_salary_count
        )
        
        # Format job list
        job_list = self._format_job_list(sorted_jobs)
        
        # Format top recommendations
        recommendations = self._format_recommendations(top_jobs, profile_data)
        
        return {
            'summary': summary,
            'job_list': job_list,
            'recommendations': recommendations,
            'top_jobs': top_jobs,
            'all_jobs': sorted_jobs,
            'stats': {
                'total_jobs': len(sorted_jobs),
                'high_match': len([j for j in sorted_jobs if j.get('skill_match') == 'high']),
                'medium_match': len([j for j in sorted_jobs if j.get('skill_match') == 'medium']),
                'low_match': len([j for j in sorted_jobs if j.get('skill_match') == 'low']),
                'remote_jobs': len([j for j in sorted_jobs if 'remote' in j.get('location', '').lower()]),
                'colorado_jobs': len([j for j in sorted_jobs if 'colorado' in j.get('location', '').lower() or 'co' in j.get('location', '').lower()]),
                'duplicates_excluded': duplicate_count,
                'inactive_excluded': inactive_count,
                'low_salary_excluded': low_salary_count
            }
        }
    
    def _score_jobs(self, jobs: List[Dict], profile_data: Dict) -> List[Dict]:
        """Add skill match scores to jobs"""
        for job in jobs:
            job_description = job.get('description', '') + ' ' + job.get('title', '')
            job['skill_match'] = self.profile_analyzer.calculate_skill_match(
                profile_data,
                job_description
            )
        return jobs
    
    def _sort_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Sort jobs by skill match score, then by posting date"""
        match_order = {'high': 0, 'medium': 1, 'low': 2}
        
        return sorted(
            jobs,
            key=lambda x: (
                match_order.get(x.get('skill_match', 'low'), 3),
                x.get('posted_date', '')
            ),
            reverse=True
        )
    
    def _generate_summary(
        self,
        jobs: List[Dict],
        profile_data: Dict,
        duplicate_count: int,
        inactive_count: int,
        low_salary_count: int
    ) -> str:
        """Generate summary message"""
        stats = {
            'total': len(jobs),
            'high': len([j for j in jobs if j.get('skill_match') == 'high']),
            'medium': len([j for j in jobs if j.get('skill_match') == 'medium']),
            'low': len([j for j in jobs if j.get('skill_match') == 'low']),
            'remote': len([j for j in jobs if 'remote' in j.get('location', '').lower()]),
            'colorado': len([j for j in jobs if 'colorado' in j.get('location', '').lower() or ', co' in j.get('location', '').lower()])
        }
        
        summary = f"""📊 Daily Job Search Report
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p MT')}

🎯 NEW Job Opportunities Found: {stats['total']}
   • Remote positions: {stats['remote']}
   • Colorado-based: {stats['colorado']}

📈 Skill Match Breakdown:
   • High Match: {stats['high']} jobs
   • Medium Match: {stats['medium']} jobs
   • Low Match: {stats['low']} jobs

🔍 Search Filters Applied:
   • Minimum Salary: $130,000+
   • Locations: Remote or Colorado
   • Status: Actively accepting applications
   • Application Type: Easy Apply

📉 Jobs Excluded:
   • Duplicate postings: {duplicate_count}
   • No longer accepting applications: {inactive_count}
   • Salary below $130,000: {low_salary_count}
"""
        
        return summary
    
    def _format_job_list(self, jobs: List[Dict]) -> str:
        """Format complete job list"""
        if not jobs:
            return "No jobs found matching criteria."
        
        job_list = "\n📋 COMPLETE JOB LIST:\n" + "=" * 80 + "\n\n"
        
        for i, job in enumerate(jobs, 1):
            match_emoji = {
                'high': '🟢',
                'medium': '🟡',
                'low': '🔴'
            }.get(job.get('skill_match', 'low'), '⚪')
            
            job_list += f"{i}. {match_emoji} {job.get('title', 'N/A')}\n"
            job_list += f"   Company: {job.get('company', 'N/A')}\n"
            job_list += f"   Location: {job.get('location', 'N/A')}\n"
            job_list += f"   Salary: {job.get('salary_range', 'Not specified')}\n"
            job_list += f"   Skill Match: {job.get('skill_match', 'N/A').title()}\n"
            job_list += f"   Source: {job.get('source', 'N/A')}\n"
            job_list += f"   Posted: {job.get('posted_date', 'N/A')}\n"
            job_list += f"   Apply: {job.get('url', 'N/A')}\n"
            job_list += "\n"
        
        return job_list
    
    def _format_recommendations(self, top_jobs: List[Dict], profile_data: Dict) -> str:
        """Format top job recommendations with explanations"""
        if not top_jobs:
            return "No top recommendations available."
        
        recommendations = "\n🌟 TOP RECOMMENDATIONS:\n" + "=" * 80 + "\n\n"
        
        for i, job in enumerate(top_jobs, 1):
            match_emoji = {
                'high': '🟢 EXCELLENT MATCH',
                'medium': '🟡 GOOD MATCH',
                'low': '🔴 POTENTIAL MATCH'
            }.get(job.get('skill_match', 'low'), '⚪ MATCH')
            
            recommendations += f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}\n"
            recommendations += f"   {match_emoji}\n"
            recommendations += f"   📍 {job.get('location', 'N/A')}\n"
            recommendations += f"   💰 {job.get('salary_range', 'Not specified')}\n"
            recommendations += f"   📅 Posted: {job.get('posted_date', 'N/A')}\n"
            recommendations += f"   🔗 Apply: {job.get('url', 'N/A')}\n"
            
            # Generate match explanation
            explanation = self._generate_match_explanation(job, profile_data)
            recommendations += f"   ℹ️  Why this matches: {explanation}\n"
            recommendations += "\n"
        
        return recommendations
    
    def _generate_match_explanation(self, job: Dict, profile_data: Dict) -> str:
        """Generate explanation for why a job matches the profile"""
        explanations = []
        
        job_text = (job.get('description', '') + ' ' + job.get('title', '')).lower()
        skills = profile_data.get('skills', [])
        
        # Find matching skills
        matching_skills = [skill for skill in skills[:10] if skill.lower() in job_text]
        
        if matching_skills:
            skills_str = ', '.join(matching_skills[:3])
            explanations.append(f"Matches your skills in {skills_str}")
        
        # Check location preference
        location = job.get('location', '').lower()
        if 'remote' in location:
            explanations.append("Offers remote work flexibility")
        elif 'colorado' in location or ', co' in location:
            explanations.append("Located in Colorado")
        
        # Check salary
        salary = job.get('salary_range', '')
        if salary and salary != 'Not specified':
            explanations.append(f"Competitive compensation")
        
        if not explanations:
            explanations.append("Aligns with your experience level and career goals")
        
        return "; ".join(explanations)
