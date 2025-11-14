"""
Slack Notification Agent - Sends job reports to Slack
"""
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict
from src.utils.logger import setup_logger
from src.config import SLACK_BOT_TOKEN, SLACK_CHANNEL

logger = setup_logger(__name__)

class SlackNotifier:
    """Send job reports to Slack channel"""
    
    def __init__(self, token: str = SLACK_BOT_TOKEN, channel: str = SLACK_CHANNEL):
        """
        Initialize Slack notifier.
        
        Args:
            token: Slack bot token
            channel: Slack channel to post to
        """
        self.client = WebClient(token=token) if token else None
        self.channel = channel
    
    def send_report(self, report: Dict) -> bool:
        """
        Send job report to Slack channel.
        
        Args:
            report: Compiled job report
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("Slack client not configured. Printing report to console instead.")
            self._print_report(report)
            return False
        
        try:
            # Send summary message
            self._send_summary(report)
            
            # Send top recommendations
            self._send_recommendations(report)
            
            # Send complete job list in thread or separate message
            self._send_job_list(report)
            
            logger.info(f"Successfully sent report to {self.channel}")
            return True
            
        except SlackApiError as e:
            logger.error(f"Error sending to Slack: {e.response['error']}")
            self._print_report(report)
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending to Slack: {e}")
            self._print_report(report)
            return False
    
    def _send_summary(self, report: Dict):
        """Send summary message to Slack"""
        summary = report.get('summary', '')
        
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=summary,
                unfurl_links=False,
                unfurl_media=False
            )
            return response
        except Exception as e:
            logger.error(f"Error sending summary: {e}")
            raise
    
    def _send_recommendations(self, report: Dict):
        """Send top recommendations to Slack"""
        recommendations = report.get('recommendations', '')
        
        # Split into chunks if too long (Slack has a 3000 char limit per message)
        chunks = self._split_message(recommendations, 2900)
        
        for i, chunk in enumerate(chunks):
            try:
                self.client.chat_postMessage(
                    channel=self.channel,
                    text=chunk,
                    unfurl_links=False,
                    unfurl_media=False
                )
            except Exception as e:
                logger.error(f"Error sending recommendations chunk {i}: {e}")
    
    def _send_job_list(self, report: Dict):
        """Send complete job list to Slack"""
        job_list = report.get('job_list', '')
        
        # Split into chunks if too long
        chunks = self._split_message(job_list, 2900)
        
        for i, chunk in enumerate(chunks):
            try:
                self.client.chat_postMessage(
                    channel=self.channel,
                    text=chunk,
                    unfurl_links=False,
                    unfurl_media=False
                )
            except Exception as e:
                logger.error(f"Error sending job list chunk {i}: {e}")
    
    def _split_message(self, message: str, max_length: int = 2900) -> list:
        """
        Split a long message into chunks.
        
        Args:
            message: Message to split
            max_length: Maximum length per chunk
            
        Returns:
            List of message chunks
        """
        if len(message) <= max_length:
            return [message]
        
        chunks = []
        current_chunk = ""
        
        for line in message.split('\n'):
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _print_report(self, report: Dict):
        """Print report to console as fallback"""
        logger.info("=" * 80)
        logger.info("PRINTING REPORT TO CONSOLE (Slack not configured)")
        logger.info("=" * 80)
        
        print("\n" + report.get('summary', ''))
        print("\n" + report.get('recommendations', ''))
        print("\n" + report.get('job_list', ''))
        
        logger.info("=" * 80)
    
    def send_test_message(self) -> bool:
        """
        Send a test message to verify Slack connection.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("Slack client not configured")
            return False
        
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text="🤖 Job Search AI Agent - Test Message\n\nSlack integration is working correctly!"
            )
            logger.info("Test message sent successfully")
            return True
        except SlackApiError as e:
            logger.error(f"Error sending test message: {e.response['error']}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
