from __future__ import print_function
import requests, json
from datetime import datetime
from dateutil.parser import parse


def pulls_list(git_api_url, org_name, repo_name, api_user, token):
    
    """
    Lists all open pull requests on a given repository 
    Returns a list of tuples containing some information for each pull request
    """
    url = git_api_url + "/repos/" + org_name + "/" + repo_name + "/pulls?state=all" 
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
            state = currentPull["state"]

            pullRequests.append((repo_name, pull_id, title, login, creation_date, html_url, state));
        
        return pullRequests
    else:
        print("Pulls List Error Code: {}".format(req.status_code))
        raise SystemExit

def post_to_slack(pull_requests, slack_webhook):
    
    """
    Posts the list of open pull requests provided to the slack thread 
    """
    for current_request in pull_requests:
        slack_data = {'text': 'Lambda User: ' + current_request[3] + "\n" + current_request[2] + ": " + current_request[6] + "\n" + current_request[5] + "\n\n"}
        response = requests.post(slack_webhook, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
    
        if response.status_code != 200:
            raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))
    

def lambda_handler(event, context):
    api_user='YOUR API User'
    api_token='YOUR Token'
    git_api_url='https://api.github.com'
    org_name=event['org']
    repo_name=event['repo']
    slack_webhook='https://hooks.slack.com/services/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'
    

    pullRequests = pulls_list(git_api_url, org_name, repo_name, api_user, api_token)
    if len(pullRequests) > 0:
        post_to_slack(pullRequests, slack_webhook)


if __name__ == '__main__':
    event = {'org': 'ajavanshir', 'repo': 'git-to-slack'}
    lambda_handler(event, 'context')
   
            
