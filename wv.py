import argparse
from datetime import date, datetime, timedelta
import json
import os
import requests
from termcolor import colored

github_api = "https://kctbh9vrtdwd.statuspage.io/api/v2"
heroku_api = "https://status.heroku.com/api/v4"

time = datetime.now().strftime('%H:%M:%S')
today = date.today()
yesterday = today - timedelta(days = 1)

version = 'v0.1'

# Parse for arguments.
parser = argparse.ArgumentParser(description='Gather diagnostic information from third party providers for use during incidents and diagnostic operations.')
parser.add_argument('-p', '--providers', dest='providers', type=str, help='Comma separated list of providers to get reports from. Options are: heroku, github', default='')
parser.add_argument('-c', '--compact', dest='compact', help='Show compact summary instead of verbose output. Ignores incident details and header.', action='store_true')
args = parser.parse_args()

compact = args.compact
providers = args.providers

# Colorize function.
def color(i, cond):
  if i != cond:
    return(colored(i, 'red'))
  else:
    return(colored(i, 'green'))

# Heroku
def get_heroku_status(heroku_api, compact):
  sr = requests.get('{}/current-status'.format(heroku_api))
  sp = json.loads(sr.text)

  print(colored('Heroku', 'magenta', attrs=['bold']) + ' Status at ' + time + ':')
  print('-------------------------')

  apps_status = sp["status"]

  for a in apps_status:
    l = a['system']
    s = a['status']

    print(' System: ' + l)
    print(' Status: ' + color(s, 'green'))
    print()
  
  if not compact:
    print('Current ' + colored('Heroku', 'magenta', attrs=['bold']) + ' incidents:')
    print('-------------------------')
  
    if sp['incidents'] == []:
      print('No incidents currently reported.')
    else:
      cinc = sp['incidents']

      for actinc in cinc:
        print(colored('Title: ', attrs=['bold']) + actinc['title'])
        print(colored('Incident ID: ', attrs=['bold']) + str(actinc['id']))
        print(colored('State: ', attrs=['bold']) + actinc['state'])
        print(colored('More info: ', attrs=['bold']) + actinc['full_url'])
        print(colored('Last comment: ', attrs=['bold']) + actinc['updates'][0]['contents'])

    print()
    print(colored('Heroku', 'magenta', attrs=['bold']) + ' incidents in the past day:')
    print('-------------------------')

    ir = requests.get('{}/incidents?since={}&per_page=3'.format(heroku_api, yesterday))
    ipr = json.loads(ir.text)

    if ipr == []:
      print(  'No incidents reported since ' + str(yesterday) + '.')
    else:
      for inc in ipr:
        print(colored('Title: ', attrs=['bold']) + inc['title'])
        print(colored('State: ', attrs=['bold']) + inc['state'])
        print(colored('More info: ', attrs=['bold']) + inc['full_url'])
        print(colored('Created at: ', attrs=['bold']) + inc['created_at'])
        print(colored('Initial comment: ', attrs=['bold']) + inc['updates'][-1]['contents'])
        print(colored('Final comment: ', attrs=['bold']) + inc['updates'][0]['contents'])
    print()

# GitHub
def get_github_status(github_api, compact):
  if not compact:
    sr = requests.get('{}/summary.json'.format(github_api))
    sp = json.loads(sr.text)

    print(colored('GitHub', 'cyan', attrs=['bold']) + ' Status at ' + time + ':')
    print('-------------------------')

    apps_status = sp['components']

    for a in apps_status:
      n = a['name']
      s = a['status']
      d = a['description'] or 'None provided'

      print(' Component: ' + n + ' - ' + d)
      print(' Status: ' + color(s, 'operational'))
      print()
    print()

    print('Current ' + colored('GitHub', 'cyan', attrs=['bold']) + ' incidents:')
    print('-------------------------')
  
    ir = requests.get('{}/incidents/unresolved.json'.format(github_api))
    ipr = json.loads(ir.text)

    if ipr['incidents'] == []:
      print(' No incidents currently reported.')
    else:
      for inc in ipr['incidents']:
        print(colored('Title: ', attrs=['bold']) + inc['name'])
        print(colored('State: ', attrs=['bold']) + inc['status'])
        print(colored('More info: ', attrs=['bold']) + inc['shortlink'])
        print(colored('Last comment: ', attrs=['bold']) + inc['incident_updates'][0]['body'])
    print()
  elif compact:
    sr = requests.get('{}/status.json'.format(github_api))
    sp = json.loads(sr.text)

    print(colored('GitHub', 'cyan', attrs=['bold']) + ' Status at ' + time + ':')
    print('-------------------------')
    print(' ' + sp['status']['description'])

# Run
def run():
  if not compact:
    print(colored('𝚠𝚎𝚊𝚝𝚑𝚎𝚛𝚟𝚊𝚗𝚎', 'cyan'))
    print(version)
    print('𝚑𝚝𝚝𝚙𝚜://𝚐𝚒𝚝𝚑𝚞𝚋.𝚌𝚘𝚖/𝚜𝚑𝚒𝚙𝚠𝚛𝚎𝚌𝚔𝚍𝚎𝚟/𝚠𝚎𝚊𝚝𝚑𝚎𝚛𝚟𝚊𝚗𝚎')
    print()

  if 'heroku' in providers:
    get_heroku_status(heroku_api, compact)
  if 'github' in providers:
    get_github_status(github_api, compact)
  if providers == '':
    print(colored('Error: ', 'red') + ' No providers supplied. Please use -p to declare providers to check. Try -h for help.')

run()
