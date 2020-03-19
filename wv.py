import argparse
from datetime import date, datetime, timedelta
import json
import os
import requests
from termcolor import colored

from lib.utils import errcolor
from lib.gcp import get_gcp_status
from lib.github import get_github_status
from lib.heroku import get_heroku_status

version = 'v0.1'

# API Base URLs
gcp_api = "https://status.cloud.google.com"
github_api = "https://kctbh9vrtdwd.statuspage.io/api/v2"
heroku_api = "https://status.heroku.com/api/v4"

# Time/Data Scoping Variables
time = datetime.now().strftime('%H:%M:%S')
today = date.today()
yesterday = today - timedelta(days = 1)

# Parse for arguments.
parser = argparse.ArgumentParser(description='Gather diagnostic information from third party providers for use during incidents and diagnostic operations.')
parser.add_argument('-p', '--providers', dest='providers', type=str, help='Comma separated list of providers to get reports from. Options are: gcp, github, heroku', default='')
parser.add_argument('-c', '--compact', dest='compact', help='Show compact summary instead of verbose output. Ignores incident details and header.', action='store_true')
args = parser.parse_args()

# Set variables based on argument parsing.
compact = args.compact
providers = args.providers

# Run!
def run():
  if not compact:
    print(colored('𝚠𝚎𝚊𝚝𝚑𝚎𝚛𝚟𝚊𝚗𝚎', 'cyan'))
    print(version)
    print('𝚑𝚝𝚝𝚙𝚜://𝚐𝚒𝚝𝚑𝚞𝚋.𝚌𝚘𝚖/𝚜𝚑𝚒𝚙𝚠𝚛𝚎𝚌𝚔𝚍𝚎𝚟/𝚠𝚎𝚊𝚝𝚑𝚎𝚛𝚟𝚊𝚗𝚎')
    print()

  if 'heroku' in providers:
    get_heroku_status(heroku_api, compact, time, today, yesterday)
  if 'gcp' in providers:
    get_gcp_status(gcp_api)
  if 'github' in providers:
    get_github_status(github_api, compact, time)
  if providers == '':
    print(colored('Error: ', 'red') + ' No providers supplied. Please use -p to declare providers to check. Try -h for help.')

run()
