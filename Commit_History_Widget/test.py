"""
 Monthly Commit History:
    This file handles the networking side of the widget.
    This file uses Python's 'Requests Library', whyich acts as HTTP client & interact with REST APIs
    Requests in this case inteacts with 'GitHub REST API (Search endpoint)'
"""
from datetime import datetime, timezone, timedelta
import requests

def fetch_30_day_commits(username: str) -> int:
    # 1. Calculate the sliding window date boundary
    today = datetime.now(timezone.utc)
    thirty_days_ago = today - timedelta(days=30)
    date_str = thirty_days_ago.strftime('%Y-%m-%d') # Format: YYYY-MM-DD
    # ISO 8601 standard for dates: YYYY-MM-DD
    # Why ISO 8601: Efficient & accurate date sorting

    # 2. Build the Search API Query
    # q=author:username filters by you
    # committer-date:>=YYYY-MM-DD filters the timeline
    url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:>={date_str}"
    # 'https://api.github.com/search/commits' tells to search global commit log DB
    # '?' Separation Wall-> LEFT = Routing dest. RIGHT = data prara.
    # 'q =' Query Key: Search Criteria (Read Only?)
    # 'Criteria & values'-> author-restricts search to specific github user name & committer-date->'≍' SQL WHERE
    # '+' Connector in HTTP req.

    # The Search API requires a specific 'Accept' header alongside the User-Agent
    # HTTP headers = meta-data sent alongside HTTP req. & res.
    headers = {
        'User-Agent': 'GitCommitEngine30Day', #User Agent: HTTP req. header-identifies user,OS,etc.
        'Accept': 'application/vnd.github+json' # What type of return data
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200: # HTTP OK- prevents scripot from running when server throws error
        data = response.json()
        # The Search API explicitly hands back the total match count upfront!
        total_commits = data.get('total_count', 0) # (total_count = search key ,0 Fallback) | Prevents KEY ERROR
        return total_commits
    elif response.status_code == 403: # Forbidden- Boundary violation
        print("Rate limit hit! Wait a minute before trying again.") # 403= Stop execution
        return 0
    else:
        print(f"Failed with status code: {response.status_code}")
        return 0
# 422 Unprocessable: Wrong Quey syntax (server rejects logical arguments)


if __name__ == "__main__":
    my_user = input("YOUR_GITHUB_USERNAME: ")
    commits_count = fetch_30_day_commits(my_user)
    print(f"📊 Commits in the last 30 days by {my_user}: {commits_count}")

