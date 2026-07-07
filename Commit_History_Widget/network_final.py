"""
Monthly Commit History Networking File:
Handles the networking side of the widget.
This file uses Python's 'Requests Library', whyich acts as HTTP client & interact with REST APIs
Requests in this case inteacts with 'GitHub REST API (Search endpoint)'
HTTPAdapter, utillib3's Retry Class help in creating sessions & maintaining them.
Sessions allow TCP pooling, which only needs the 3 way handshake one for establishing connection, Payload can be transported hasslefree
'datetime' module is responsible for Time management of the widget
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timezone, timedelta

# 1. Why class: Allows to hold state (session)
class GitCommitEngine:

    def __init__(self, username: str, token: str |  None = None): # Private Access Token is optional!
         # By initializing here, the TCP connection stays open permanently!
        self.username = username
        self.token = token
        self.session = self._create_resilient_session()

    def _create_resilient_session(self) -> requests.Session:
        # Builds a TCP-pooled session with Exponential Backoff.
        session = requests.Session()

        # 2: Smart Retry (Don't spam servers->repeated requests may signal DDoS )
        # backoff_factor=1 -> Waits 0s, 2s, 4s between attempts.
        # status_forcelist -> ONLY retry if the server is having internal issues (5xx) or Rate Limited (429)
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"] # Read Only
        )

        # Mount the strategy: Tells Python to use these rules for all HTTPS traffic in this session
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    def fetch_30_day_commits(self) -> dict:
        # 3. Fetches data using the pooled session and strict timeouts (Defensive Timeout).
        today = datetime.now(timezone.utc)
        thirty_days_ago = today - timedelta(days=30)
        date_str = thirty_days_ago.strftime('%Y-%m-%d')

        # Base URL
        url = "https://api.github.com/search/commits"
        
        # 'Params' Dictionary- helps in HTTP encoding
        query_params = {
        "q": f"author:{self.username} committer-date:>={date_str}"
        }

        headers = {
            'User-Agent': 'GitCommitEngine30Day',
            'Accept': 'application/vnd.github+json',
        }
        if self.token:
            # Private Repo Commit History Access (optional)
            headers ['Authorization'] = f'Bearer {self.token}'

        try:
            # (3.05s to establish connection, 10s max to download payload)
            response = self.session.get(url, params= query_params, headers=headers, timeout=(3.05, 10))
            # Instantly throws an exception if status is 4xx or 5xx (bypassing the need for manual if/else checks)
            response.raise_for_status()

            data = response.json()
            return {"count": data.get('total_count', 0), "error": None}
        # Catch specific issues for clean terminal logging
        except requests.exceptions.ConnectionError:
            print("CRITICAL: Wi-Fi dropped or DNS failed.")
            return {"count": None, "error": "offline"}
        except requests.exceptions.Timeout:
            print("CRITICAL: Server took too long to respond.")
            return {"count": None, "error": "offline"}
        except requests.exceptions.HTTPError as err:
            print(f"CRITICAL: Server returned an error code: {err}")
            return {"count": None, "error": "offline"}
        # The Ultimate Safety Net for anything else we missed
        except requests.exceptions.RequestException as e:
            print(f"CRITICAL: Unknown network error: {e}")
            return {"count": None, "error": "offline"}

if __name__ == "__main__":
    # passing username into constructor
    my_user = input(" Enter username: ")
    engine = GitCommitEngine(username=my_user)
    # Call fetch funtion.
    result = engine.fetch_30_day_commits()

    if result.get("error") == "offline":
        print("Widget UI Action: Paint text red, display '--'")
    else:
        print(f"Widget UI Action: Paint text green, display count: {result['count']}")