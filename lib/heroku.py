import json
import requests
from termcolor import colored
from .utils import errcolor

def get_heroku_status(heroku_api, compact, time, today, yesterday):
  sr = requests.get('{}/current-status'.format(heroku_api))
  sp = json.loads(sr.text)

  print(colored('Heroku', 'magenta', attrs=['bold']) + ' Status at ' + time + ':')
  print('-------------------------')

  apps_status = sp["status"]

  for a in apps_status:
    l = a['system']
    s = a['status']

    print(' System: ' + l)
    print(' Status: ' + errcolor(s, 'green'))
    print()
  
  if not compact:
    print('Current ' + colored('Heroku', 'magenta', attrs=['bold']) + ' incidents:')
    print('-------------------------')
  
    if sp['incidents'] == []:
      print('No incidents currently reported.')
    else:
      cinc = sp['incidents']

      for actinc in cinc:
        print(colored(' Title: ', attrs=['bold']) + actinc['title'])
        print(colored(' Incident ID: ', attrs=['bold']) + str(actinc['id']))
        print(colored(' State: ', attrs=['bold']) + actinc['state'])
        print(colored(' More info: ', attrs=['bold']) + actinc['full_url'])
        print(colored(' Last comment: ', attrs=['bold']) + actinc['updates'][0]['contents'])

    print()
    print(colored('Heroku', 'magenta', attrs=['bold']) + ' incidents in the past day:')
    print('-------------------------')

    ir = requests.get('{}/incidents?since={}&per_page=3'.format(heroku_api, yesterday))
    ipr = json.loads(ir.text)

    if ipr == []:
      print(  'No incidents reported since ' + str(yesterday) + '.')
    else:
      for inc in ipr:
        if inc['state'] != 'open':
          print(colored(' Title: ', attrs=['bold']) + inc['title'])
          print(colored(' State: ', attrs=['bold']) + inc['state'])
          print(colored(' More info: ', attrs=['bold']) + inc['full_url'])
          print(colored(' Created at: ', attrs=['bold']) + inc['created_at'])
          print(colored(' Initial comment: ', attrs=['bold']) + inc['updates'][-1]['contents'])
          print(colored(' Final comment: ', attrs=['bold']) + inc['updates'][0]['contents'])
          print()
    print()
