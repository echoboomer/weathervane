import json
import requests
from termcolor import colored
from .utils import errcolor


def get_gcp_status(gcp_api):
    print(colored('Google Cloud Platform', 'blue',
                  attrs=['bold']) + ' most recent incidents:')
    print('-------------------------')

    ir = requests.get('{}/incidents.json'.format(gcp_api))
    ipr = json.loads(ir.text)

    for inc in ipr[0:3]:
        print(colored('Description: ', attrs=['bold']) + inc['external_desc'])
        print(colored('Created: ', attrs=['bold']) + inc['begin'])
        print(colored('Last comment: ', attrs=[
              'bold']) + inc['most-recent-update']['text'])
        print()
    print()
