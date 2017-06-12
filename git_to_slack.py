from __future__ import print_function
import requests, json
from datetime import datetime
from dateutil.parser import parse

def repos_list(git_api_url, org_name, api_user, token):
    
    """
    Lists all repositories of the given org
    Returns the list of repository names
    """

    url = git_api_url + "/orgs/" + org_name + "/repos"

    #print("List URL: " + url)
    #print("User: " + api_user)
    #print("Token: " + token)

    #s = requests.Session()
    #s.headers.update({'access_token': token})

    tokenHeader = {'Authorization': 'token %s' % token}
    req = requests.get(url, headers=tokenHeader)  
    
    if req.status_code == 200:

        data = req.json()
        repoList = []
        for currentRepo in data:
            repoName = currentRepo["name"]
            repoList.append(repoName)

        return repoList
    else:
        print("Repo List Error Code: {} ".format(req.status_code))
        raise SystemExit


def pulls_list(git_api_url, org_name, repo_name, api_user, token):
    
    """
    Lists all open pull requests on a given repository 
    Returns a list of tuples containing some information for each pull request
    """
    url = git_api_url + "/repos/" + org_name + "/" + repo_name + "/pulls?status=open" 
    #print("List URL: " + url)
    tokenHeader = {'Authorization': 'token %s' % token}    
    req = requests.get(url, headers=tokenHeader)  
    
    if req.status_code == 200:

        data = req.json()

        pullRequests=[]
        for currentPull in data:
            
            pull_id = currentPull["id"]
            title = currentPull["title"]
            login = currentPull["user"]["login"]
            #creation_date = datetime.strptime(currentPull["created_at"], '%Y-%m-%dT%H:%M:%SZ')
            creation_date = parse(currentPull["created_at"])
            html_url= currentPull["html_url"]

            pullRequests.append((repo_name, pull_id, title, login, creation_date, html_url));
        
        return pullRequests
    else:
        print("Pulls List Error Code: {}".format(req.status_code))
        raise SystemExit

def post_to_slack(pull_requests, slack_webhook):
    
    """
    Posts the list of open pull requests provided to the slack thread 
    """
    for current_request in pull_requests:
        slack_data = {'text': 'Lambda User: ' + current_request[3] + "\n" + current_request[5] + "\n\n"}
        response = requests.post(slack_webhook, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
    
        if response.status_code != 200:
            raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))
    

def lambda_handler(event, context):
    api_user='ajavanshir'
    api_token='bd8e32ff3c059b4466e36b43409afb6f10bd4736'
    git_api_url='https://api.github.com'
    org_name=event['org']
    #repo_name="quickstart-oracle-database"
    slack_webhook='https://hooks.slack.com/services/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'

    repoList = repos_list(git_api_url, org_name, api_user, api_token)
    #print(repoList)

    for repo in repoList:
        pullRequests = pulls_list(git_api_url, org_name, repo, api_user, api_token)
        if len(pullRequests) > 0:
            post_to_slack(pullRequests, slack_webhook)

