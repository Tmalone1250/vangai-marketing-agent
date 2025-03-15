import time
from src.web3_script import check_balance, send_vangai
from src.linkedin_script import post_to_linkedin, like_post, automate_linkedin
from src.utils.auth import get_access_token, refresh_access_token
from src.self_improve import SelfImproveAgent

class AIAgent:
    def __init__(self, linkedin_access_token, wallet_address, private_key, repo_url, branch):
        self.linkedin_access_token = linkedin_access_token
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.self_improve = SelfImproveAgent(repo_url, branch)
        self.performance_metrics = {
            'linkedin_posts': 0,
            'linkedin_likes': 0,
            'transactions': 0,
            'errors': 0
        }

    def check_wallet_balance(self):
        """
        Check the balance of VANGAI tokens in the wallet.
        """
        balance = check_balance(self.wallet_address)
        print(f"VANGAI Balance: {balance}")
        return balance

    def send_vangai_tokens(self, receiver_address, amount):
        """
        Send VANGAI tokens to a specified address.
        """
        txn_hash = send_vangai(self.private_key, receiver_address, amount)
        print(f"Sent {amount} VANGAI to {receiver_address}. Transaction Hash: {txn_hash}")
        return txn_hash

    def run_linkedin_automation(self):
        """
        Run LinkedIn automation tasks (e.g., posting, liking).
        """
        try:
            print("Starting LinkedIn automation...")
            post_to_linkedin(self.linkedin_access_token, "Check out Vanguard AI - the future of AI agents! 🚀 #AI #Blockchain #VANGAI")
            self.performance_metrics['linkedin_posts'] += 1
            
            like_post(self.linkedin_access_token, "urn:li:share:1234567890")  # Replace with actual post URN
            self.performance_metrics['linkedin_likes'] += 1
        except Exception as e:
            print(f"Error in LinkedIn automation: {str(e)}")
            self.performance_metrics['errors'] += 1

    def attempt_self_improvement(self):
        """
        Analyze performance and trigger self-improvement if needed.
        """
        # Check if errors exceed threshold or performance is declining
        if (self.performance_metrics['errors'] > 5 or 
            (self.performance_metrics['linkedin_posts'] + self.performance_metrics['linkedin_likes']) < 10):
            print("Performance metrics indicate need for improvement...")
            
            # Determine focus area based on metrics
            focus_area = None
            if self.performance_metrics['errors'] > 0:
                focus_area = 'error_handling'
            elif self.performance_metrics['linkedin_posts'] < 5:
                focus_area = 'linkedin'
                
            # Trigger self-improvement
            if self.self_improve.trigger_self_improvement(focus_area):
                print("Self-improvement successful, resetting metrics...")
                self.performance_metrics = {key: 0 for key in self.performance_metrics}
            else:
                print("Self-improvement attempt completed without changes")

    def monitor_and_act(self):
        """
        Monitor goals and take actions to achieve them.
        """
        improvement_interval = 12 * 3600  # Check for improvements every 12 hours
        last_improvement_check = time.time()

        while True:
            try:
                # Run regular tasks
                self.run_linkedin_automation()

                balance = self.check_wallet_balance()
                if balance > 1000:  # Example threshold
                    self.send_vangai_tokens("0xReceiverAddress", 100)
                    self.performance_metrics['transactions'] += 1

                # Check if it's time for self-improvement
                current_time = time.time()
                if current_time - last_improvement_check >= improvement_interval:
                    self.attempt_self_improvement()
                    last_improvement_check = current_time

                # Wait for 3 hours before the next cycle
                time.sleep(3 * 3600)
                
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                self.performance_metrics['errors'] += 1
                time.sleep(300)  # Wait 5 minutes before retrying on error

if __name__ == "__main__":
    # Load credentials from environment variables or user input
    linkedin_access_token = "your_linkedin_access_token"  # Replace with actual token
    wallet_address = "0xYourWalletAddress"
    private_key = "your_private_key"  # Securely handle this!
    repo_url = "https://github.com/yourusername/yourrepo"  # Replace with actual repo URL
    branch = "main"  # Replace with your target branch

    # Initialize the AI Agent
    ai_agent = AIAgent(linkedin_access_token, wallet_address, private_key, repo_url, branch)

    # Start the AI Agent
    ai_agent.monitor_and_act()