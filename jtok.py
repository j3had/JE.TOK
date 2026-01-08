import requests
import itertools
import string
import threading
import time
from colorama import Fore, Back, Style, init
from datetime import datetime
import json

init(autoreset=True)

class TikTokUsernameGuesser:
    def __init__(self):
        self.base_url = "https://www.tiktok.com/api/user/detail/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.found_usernames = []
        self.checked_count = 0
        self.start_time = None
        self.lock = threading.Lock()
        self.stop_flag = False
        
    def print_header(self):
        """Print the tool header"""
        print("\n" + "="*70)
        print(f"{Back.CYAN}{Fore.BLACK}{'':^70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'':^70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'🎵  J TOK - TikTok Username Finder  🎵':^70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'':^70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'':^70}{Style.RESET_ALL}")
        print("="*70)
        print(f"{Fore.MAGENTA}{'Discover Available Usernames (2-4 Characters Only)':^70}{Style.RESET_ALL}")
        print("="*70 + "\n")
    
    def generate_usernames(self, min_length=2, max_length=4):
        """Generate usernames"""
        characters = string.ascii_lowercase + string.digits
        usernames = []
        
        for length in range(min_length, max_length + 1):
            for combo in itertools.product(characters, repeat=length):
                usernames.append(''.join(combo))
        
        return usernames
    
    def check_username(self, username):
        """Check if username is available using TikTok API"""
        try:
            # Try multiple API endpoints to verify username availability
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
                'Referer': 'https://www.tiktok.com/'
            }
            
            # Method 1: Check via web page and look for specific user data
            response = requests.get(
                f"https://www.tiktok.com/@{username}",
                headers=headers,
                timeout=10
            )
            
            with self.lock:
                self.checked_count += 1
            
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Look for actual user data patterns
            has_user_data = (
                f'"uniqueId":"{username}"' in content or
                f'@{username}' in content and '"id":"' in content and '"stats"' in content
            )
            
            # Exclude 404 or not found pages
            is_not_found = (
                'not found' in content.lower() or 
                'page not found' in content.lower() or
                '<title>Not Found</title>' in content or
                '404' in content[:1000]
            )
            
            # Must have user data AND not be a 404 page
            return has_user_data and not is_not_found
            
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.RequestException:
            return False
    
    def format_time(self, seconds):
        """Format time display"""
        mins, secs = divmod(int(seconds), 60)
        return f"{mins}m {secs}s"
    
    def print_progress(self, total):
        """Print progress bar"""
        progress = (self.checked_count / total) * 100
        bar_length = 45
        filled = int(bar_length * self.checked_count / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        elapsed = time.time() - self.start_time
        
        print(f"\r{Fore.GREEN}Progress: {bar} {progress:.1f}% | "
              f"Checked: {self.checked_count}/{total} | "
              f"Time: {self.format_time(elapsed)}", end='', flush=True)
    
    def print_found_username(self, username):
        """Print found available username"""
        with self.lock:
            self.found_usernames.append(username)
            status = len(self.found_usernames)
            print(f"\n{Back.GREEN}{Fore.BLACK}✓ FOUND! [{status}]{Style.RESET_ALL} "
                  f"{Fore.CYAN}@{username}{Style.RESET_ALL} is available! 🎉\n", flush=True)
    
    def save_results(self):
        """Save results to file"""
        if self.found_usernames:
            filename = f"J_TOK_usernames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("AVAILABLE TikTok USERNAMES FROM J TOK\n")
                f.write("="*50 + "\n")
                f.write(f"Search Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                for i, username in enumerate(self.found_usernames, 1):
                    f.write(f"{i}. @{username}\n")
            
            print(f"\n{Fore.YELLOW}💾 Results saved to: {filename}{Style.RESET_ALL}")
    
    def run(self, num_threads=10):
        """Run the tool"""
        self.print_header()
        
        print(f"{Fore.YELLOW}⏳ Generating usernames...{Style.RESET_ALL}")
        usernames = self.generate_usernames()
        total = len(usernames)
        
        print(f"{Fore.CYAN}✓ Generated {total:,} usernames to check{Style.RESET_ALL}\n")
        
        self.start_time = time.time()
        print(f"{Fore.YELLOW}🔍 Starting search for available usernames...{Style.RESET_ALL}\n")
        
        # Distribute usernames across threads
        threads = []
        chunk_size = len(usernames) // num_threads
        
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size if i < num_threads - 1 else len(usernames)
            chunk = usernames[start:end]
            
            thread = threading.Thread(target=self._worker, args=(chunk, total))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        self.print_results(total)
    
    def _worker(self, usernames_chunk, total):
        """Worker thread processor"""
        for username in usernames_chunk:
            if self.check_username(username):
                self.print_found_username(username)
            
            self.print_progress(total)
    
    def print_results(self, total):
        """Print final results"""
        elapsed = time.time() - self.start_time
        
        print("\n\n" + "="*70)
        print(f"{Back.CYAN}{Fore.BLACK}{'📊 FINAL RESULTS':^70}{Style.RESET_ALL}")
        print("="*70)
        
        print(f"{Fore.CYAN}Total Usernames Checked:{Style.RESET_ALL} {Fore.GREEN}{total:,}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Available Usernames Found:{Style.RESET_ALL} {Fore.GREEN}{len(self.found_usernames)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total Time Elapsed:{Style.RESET_ALL} {Fore.GREEN}{self.format_time(elapsed)}{Style.RESET_ALL}")
        
        if self.found_usernames:
            print(f"\n{Back.GREEN}{Fore.BLACK}✓ AVAILABLE USERNAMES:{Style.RESET_ALL}\n")
            for i, username in enumerate(self.found_usernames, 1):
                print(f"  {Fore.CYAN}{i}. @{username}{Style.RESET_ALL}")
            
            self.save_results()
        else:
            print(f"\n{Fore.YELLOW}⚠️  No available usernames found in this session{Style.RESET_ALL}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Main function"""
    try:
        guesser = TikTokUsernameGuesser()
        guesser.run(num_threads=15)
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Search interrupted by user{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
