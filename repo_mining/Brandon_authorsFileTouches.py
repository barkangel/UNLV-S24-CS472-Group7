import json
import requests
import csv
import os
import base64

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

def get_file_commits(repo, filename, lsttokens):
    try:
        # Get commit history for the file from the GitHub API
        commits_url = f'https://api.github.com/repos/{repo}/commits?path={filename}&per_page=100'
        json_commits, _ = github_auth(commits_url, lsttokens, 0)

        return json_commits

    except Exception as e:
        print(f"Error retrieving commit history for {filename}: {e}")

    return None

def countfilecommits(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # Get the root tree of the repository
        root_tree_url = f'https://api.github.com/repos/{repo}/git/trees/master?recursive=1'
        root_tree, ct = github_auth(root_tree_url, lsttokens, ct)

        if 'tree' in root_tree:
            # Iterate through the tree and find files in the rootbeerlib/src folder
            for file_info in root_tree['tree']:
                filename = file_info.get('path', '')

                if filename.startswith('rootbeerlib/src/'):
                    commits = get_file_commits(repo, filename, lsttokens)

                    if commits:
                        # Extract commit information
                        for commit in commits:
                            commit_info = commit.get('commit', {})
                            committer_name = commit_info.get('committer', {}).get('name', '')
                            date_accessed = commit_info.get('committer', {}).get('date', '')

                            if committer_name and date_accessed:
                                dictfiles[filename] = dictfiles.get(filename, [])
                                dictfiles[filename].append({'Committer': committer_name, 'Date': date_accessed})
                                print(f"Committer: {committer_name}, File: {filename}, Date: {date_accessed}")

            ipage += 1
    except Exception as e:
        print("Error receiving data:", e)
        exit(0)

# GitHub repo
repo = 'scottyab/rootbeer'
# Personal token
lstTokens = ["REDACTED"]

dictfiles = dict()
countfilecommits(dictfiles, lstTokens, repo)

# Output data to CSV
output_file_path = 'data/newoutput.csv'
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_csvfile:
    fieldnames = ['Committer', 'Filename', 'Date']
    writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for filename, commit_data_list in dictfiles.items():
        for commit_data in commit_data_list:
            writer.writerow({'Committer': commit_data['Committer'], 'Filename': filename, 'Date': commit_data['Date']})

print(f'Data exported to: {output_file_path}')

