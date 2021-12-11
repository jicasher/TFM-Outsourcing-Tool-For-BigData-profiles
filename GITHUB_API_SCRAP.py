# Import packages:
import requests
import datetime
from datetime import date
import dateutils
import time
import json
import pprint

#Import own functions:
from GITHUB import *
from GITHUB.functions import api_call
from GITHUB.functions import repo_api_call
from GITHUB.functions import get_repo_and_owner_names
from GITHUB.functions import save_json

# CREDENTIALS:

username = 'jicasher'
token = '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'

gh_session = requests.Session()
gh_session.auth = (username, token)


# Getting users from Spain:
#Declaring variables:
saved_items = []
start_date = datetime.datetime.fromisoformat("2021-01-01")
end_date = datetime.datetime.fromisoformat("2021-01-10")

# Call the function
user_api_call(start_date= start_date, end_date= end_date, gh_session= gh_session, saved_items=saved_items, login_list=saved_items)
#Save in json:
save_json('user', saved_items)


#Getting profiles:
#Declaring variables:
list_profiles_user = []

#Loop and calling function:
for name in range(0, len(saved_items)):
    user= saved_items[name]['login']
    repo_api_call(user=user,gh_session=gh_session , url= f'https://api.github.com/users/{user}' , saving_list= list_profiles_user)
#Save in Json:
save_json('profile', list_profiles_user) 


# Getting repos list from users
#Declaring variables:
list_repos_user = []

#Loop and calling function:
for name in range(0, len(saved_items)):
    user= saved_items[name]['login']
    repo_api_call(user=user,gh_session=gh_session , url= f'https://api.github.com/users/{user}/repos' , saving_list= list_repos_user)
#Save in Json:
save_json('repos', list_repos_user)   


# Getting repos and owners lists of names:
#Declaring varianles:
repos_name = []
repos_owner = []
#Call the function:
get_repo_and_owner_names(list_repos_user, repos_name = repos_name, repos_owner= repos_owner)


# Contributors endpoint
# Declaring variables:
contributors_list = [] 

# Loop and calling function:
for (owner, repo) in zip(repos_owner, repos_name):
    # Call the function and pass the parameters needed.   
    api_call(owner, repo, url= f'https://api.github.com/repos/{owner}/{repo}/contributors', saving_list= contributors_list, gh_session = gh_session)

# Associating repo names with contributor lists:
contributor_plus_repo =  list(zip(repos_name, contributors_list))

# Save in jsons:
save_json('contributors', contributor_plus_repo)



# COMMITS endpoint
# Decclaring variables:
commits_list = [] 

# Loop and calling function:
for (owner, repo) in zip(repos_owner, repos_name):
    # Call the function and pass the parameters needed.   
    api_call(owner, repo, url= f'https://api.github.com/repos/{owner}/{repo}/commits', saving_list= commits_list, gh_session=gh_session)

# Save in json:
save_json('commits', commits_list)


# ISSUES endpoint
# Declaring variables:
issues_list = [] 

# Loop and calling function:
for (owner, repo) in zip(repos_owner, repos_name):
    # Call the function and pass the parameters needed.   
    api_call(owner, repo, url= f'https://api.github.com/repos/{owner}/{repo}/issues', saving_list= issues_list, gh_session = gh_session)

# Save in json:
save_json('issues', issues_list)


# PULLS endpoint
# Declaring variables:
pulls_list = [] 

# Loop and calling function:
for (owner, repo) in zip(repos_owner, repos_name):
    # Call the function and pass the parameters needed.   
    api_call(owner, repo, url= f'https://api.github.com/repos/{owner}/{repo}/pulls', saving_list= pulls_list, gh_session = gh_session)

# Save in json:
save_json('pulls', pulls_list)


# SUBSCRIBERS endpoint
# Declaring variables:
subscribers_list = [] 

# Loop and calling function:
for (owner, repo) in zip(repos_owner, repos_name):
    # Call the function and pass the parameters needed.   
    api_call(owner, repo, url= f'https://api.github.com/repos/{owner}/{repo}/subscribers', saving_list= subscribers_list, gh_session= gh_session)

#  Save in json:
save_json('subscribers', subscribers_list)