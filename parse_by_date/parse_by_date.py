import os
import json
import requests as req
import datetime as dt
from requests.exceptions import HTTPError
from config_class import ReadConfig


def by_date(var_auth, var_api):

    var_auth_url = var_auth['url']
    var_result_url = var_api['url']
    var_header = var_auth['headers']
    var_cread = var_auth['cread']
    var_period_start = var_api['date']
    var_period_end = var_api['date_end']

    # Auth
    try:
        auth_conn = req.post(var_auth_url, data=var_cread, headers=var_header)
        auth_conn.raise_for_status()
    except HTTPError as exp:
        print(f'AUTH ERROR: {exp}')
    else:
        # Get Result
        auth_token = 'JWT ' + auth_conn.json()['access_token']
        var_header['Authorization'] = auth_token
        # Create period
        var_period_end_date = dt.datetime.strptime(json.loads(var_period_end)['date'], '%Y-%m-%d')
        var_period_start_date = dt.datetime.strptime(json.loads(var_period_start)['date'], '%Y-%m-%d')

        for x in range(0, (var_period_end_date-var_period_start_date).days+1):
            var_date_generated = (var_period_start_date+dt.timedelta(days=x)).date()
            var_period = json.dumps({'date': str(var_date_generated)})
            try:
                api_result = req.get(var_result_url, data=var_period, headers=var_header)
                api_result.raise_for_status()
            except HTTPError as exp:
                print(f'API ERROR: {exp} ; Date Processing: {var_date_generated}')
            else:
                # Write Result
                var_path = os.path.join('.', str(var_date_generated))
                var_file_name = os.path.join(var_path, str(var_date_generated) + '.json')
                os.makedirs(var_path, exist_ok=True)
                api_result_data = api_result.json()
                with open(var_file_name, 'w') as json_file:
                    json.dump(api_result_data, json_file)
                print('Done File: {}'.format(var_file_name))


if __name__ == '__main__':
    var_config = ReadConfig('config.yaml')
    by_date(var_config.get_config('AUTH'), var_config.get_config('API'))
