import argparse
from datetime import date, datetime, timedelta
import json
import os
import requests
from termcolor import colored

github_api = "https://kctbh9vrtdwd.statuspage.io/api/v2/"
heroku_api = "https://status.heroku.com/api/v4/"

time = datetime.now().strftime('%H:%M:%S')
today = date.today()
yesterday = today - timedelta(days = 1)

version = 'v0.1'

# Parse for arguments.
parser = argparse.ArgumentParser(description='Gather diagnostic information from third party providers for use during incidents and diagnostic operations.')
parser.add_argument('-p', '--providers', dest='providers', type=str, help='Comma separated list of providers to get reports from. Options are: heroku, github', default='')
args = parser.parse_args()

providers = args.providers

# Colorize function.
def color(i, cond):
  if i != cond:
    return(colored(i, 'red'))
  else:
    return(colored(i, 'green'))

# Heroku
def get_heroku_status(heroku_api):
  sr = requests.get('{}/current-status'.format(heroku_api))
  sp = json.loads(sr.text)

  print(colored('Heroku', 'magenta') + ' Status at ' + time)
  print('--------------------')

  apps_status = sp["status"]

  for a in apps_status:
    l = a['system']
    s = a['status']

    print(' System: ' + l)
    print(' Status: ' + color(s, 'green'))
    print()
  
  print('Current ' + colored('Heroku', 'magenta') + ' incidents:')
  print('--------------------')
  
  if sp['incidents'] == []:
    print('No incidents currently reported.')
  else:
    cinc = sp['incidents']

    for actinc in cinc:
      print('Title: ' + actinc['title'])
      print('Incident ID: ' + str(actinc['id']))
      print('State: ' + actinc['state'])
      print('More info: ' + actinc['full_url'])
      print('Last comment: ' + actinc['updates'][0]['contents'])
  
  print()
  print(colored('Heroku', 'magenta') + ' incidents in the past day:')
  print('--------------------')

  ir = requests.get('{}/incidents?since={}&per_page=3'.format(heroku_api, yesterday))
  ipr = json.loads(ir.text)

  if ipr == []:
    print(  'No incidents reported since ' + str(yesterday) + '.')
  else:
    for inc in ipr:
      print('Title: ' + inc['title'])
      print('State: ' + inc['state'])
      print('More info: ' + inc['full_url'])
      print('Last comment: ' + inc['updates'][0]['contents'])
  print()

# GitHub
def get_github_status(github_api):
  sr = requests.get('{}/summary.json'.format(github_api))
  sp = json.loads(sr.text)

  print(colored('GitHub', 'cyan') + ' Status at ' + time)
  print('--------------------')

  apps_status = sp['components']

  for a in apps_status:
    n = a['name']
    s = a['status']
    u = a['updated_at']
    d = a['description'] or 'None provided'

    print(' Component: ' + n + ' - ' + d)
    print(' Status: ' + color(s, 'operational'))
    print()
  print()

# Run
def run():
  print(colored('ᴡᴇᴀᴛʜᴇʀᴠᴀɴᴇ', 'cyan'))
  print(version)
  print()

  if 'heroku' in providers:
    get_heroku_status(heroku_api)
  if 'github' in providers:
    get_github_status(github_api)
  if providers == '':
    print(colored('Error: ', 'red') + ' No providers supplied. Please use -p to declare providers to check. Try -h for help.')

run()
