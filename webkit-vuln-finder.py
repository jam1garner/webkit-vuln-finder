import re
import urllib.request
from github import Github
from password import username, password

g = Github(username, password)
repo = g.get_repo('webkit/Webkit')

newlyDenied = []
reportRegex = re.compile("bugs\\.webkit\\.org\\/show_bug\\.cgi\\?id=[0-9]+")

with open('bad_bugs_from_commits.txt', 'w') as f:
    for commit in repo.get_commits():
        match = re.search(reportRegex, commit.commit.message)
        if match:
            with urllib.request.urlopen('https://'+match.group()) as response:
                if response.read().find(b'You are not authorized to access bug') != -1:
                    print("Commit %s, webkit bug: %s" % (commit.url.replace('api.github.com/repos', 'www.github.com').replace('commits', 'commit'), 'https://'+match.group()))
                    print("Commit %s, webkit bug: %s" % (commit.url.replace('api.github.com/repos', 'www.github.com').replace('commits', 'commit'), 'https://'+match.group()), file=f)
                    f.flush()
