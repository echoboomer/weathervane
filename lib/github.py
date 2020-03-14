import json
import requests
from termcolor import colored
from .utils import color

def get_github_status(github_api, compact, time):
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
