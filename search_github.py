import urllib.request
import json
import urllib.parse

search_url = "https://api.github.com/search/code?q=filename:Housing.csv+furnishingstatus"
req = urllib.request.Request(
    search_url,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])
        print(f"Found {len(items)} files.")
        for item in items[:5]:
            repo_fullname = item['repository']['full_name']
            path = item['path']
            # Find default branch
            repo_url = f"https://api.github.com/repos/{repo_fullname}"
            repo_req = urllib.request.Request(
                repo_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            try:
                with urllib.request.urlopen(repo_req) as repo_res:
                    repo_info = json.loads(repo_res.read().decode())
                    branch = repo_info.get('default_branch', 'master')
                    raw_url = f"https://raw.githubusercontent.com/{repo_fullname}/{branch}/{path}"
                    print(f"Candidate: {raw_url}")
            except Exception as re:
                print(f"Could not get repo details for {repo_fullname}: {re}")
except Exception as e:
    print(f"GitHub Search API failed: {e}")
