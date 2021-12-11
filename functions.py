import requests
import datetime
from datetime import date
import dateutils
import time
import json
import pprint

#FUNCTIONS:

#Users from Spain within a range of dates:
def user_api_call(start_date, end_date, gh_session, saved_items, login_list):
    # fecha inicial
    dt = start_date

    # hasta fecha final
    while dt < end_date:

        # pasamos la fecha a string para poderla poner en la query
        date_str_from = dt.strftime("%Y-%m-%d")
        
        # aumentamos una semana la fecha y la pasamos a string
        dt += dateutils.relativedelta(weeks=1)
        date_str_to = dt.strftime("%Y-%m-%d")
        
        # configuramos la query para este rango de fechas
        query_string = f'location:SPAIN created:+{date_str_from}..{date_str_to}'

        # log
        print(f"Querying: {query_string}")
        
        # iniciamos la pagina, la coleccion de items vacia para este rango y la variable num_records a un valor que nos entre en el bucle
        page = 0
        num_records = 999

        # iteramos paginas mientras recibamos 100 o más elementos
        while num_records >= 100:
        
            # log
            print(f"Querying page {page}")
                # configuramos la requests
            params1 = {
                'q':query_string,
                'per_page':'100',                    
                'page': f'{page}'
            }
        
            # llamamos a la api y recibimos los datos
            res = gh_session.get("https://api.github.com/search/users", params=params1)
            items = res.json().get("items", [])

            # guardamos los datos en la lista
            saved_items += items
            
            #login_list = [element['login'] for element in saved_items]
            # calculamos los datos para el siguiente loop
            num_records = len(items)
            page = page + 1
            
            # esperamos un segundo para no saturar la api
            time.sleep(1)

# Function to call the API for any endpoint and save results into a list
def api_call(owner, repo, url, saving_list, gh_session):       
    params_users = {'per_page':'100',
                    'page':'1'}
    header1 = {'accept' : 'application/vnd.github.london-preview+json'} 
    res2 =gh_session.get(url, params= params_users, headers = header1)
    try:
        saving_list.append(res2.json())
                       
    except ValueError:
        print("Response content is not valid JSON")
    
    print(f'user name: {owner} and repo name: {repo} and URL : {url}')
    time.sleep(1)

# Function for calling the api for repo user:
def repo_api_call(user, gh_session , url, saving_list):
    
    params2 = {'per_page':'100',
                        'page':'1'}    
        
    # llamamos a la api y recibimos los datos
    res1 =gh_session.get(url, params= params2).json()
    
    print(f'Saving {user} profile')
    # guardamos los datos en la lista
    saving_list.append(res1)

# Function for extracting names repos and names owners from list_repos_user:
def get_repo_and_owner_names(array, repos_name, repos_owner):
    for repos in array:
        for element in repos:
            repos_name.append(element['name'])
            repos_owner.append(element['owner']['login'])


#Function to save jsons:
def save_json(endpoint, list_name):
# LEt's get today date to named the file
    today = date.today()
   
    # Save the results in json:
    filename = f"C://Users/juanc/OneDrive/Escritorio/data/{endpoint}{today}.json"   # YOU CAN PASTE YOUR DATABASE URL HERE (FILENAME)
    print(f"Obtained {len(list_name)} items, saving in {filename}\n")               

    with open(filename, "w") as f:
        f.write(json.dumps(list_name))
