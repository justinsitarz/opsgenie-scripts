import requests
import json
import time

# Instructions for use:
# 1) api_key should be a key from the 'API Key Management' section in the app, with 'Read' and 'Configuration Access' rights
# 2) url can be updated to 'https://api.eu.opsgenie.com/v2/integrations' in cases where the account is in the EU region
# 3) account_name can be taken from the url of the account - for example, if the url is 'https://abc.app.opsgenie.com', account_name will be 'abc'
# 4) cookie_value can be found by following this video guide: https://share.getcloudapp.com/8LuDnRZO

api_key = ''
headers = {'Content-Type': 'application/json','Authorization':'GenieKey ' + api_key}
url = 'https://api.opsgenie.com/v2/integrations'
account_name = '' 
cookie_value = ''
cookie = 'cloud.session.token={}'.format(cookie_value)

def get_integration_details(url, headers):
	res = requests.get(url=url, headers=headers)
	integrations = json.loads(res.text)
	integration_details = [[x['name'], x['id'], x['type']] for x in integrations['data']]
	return integration_details

def get_api_keys(integration_details, web_api_headers):
	no_api_key_list = ['jira-software-cloud', 'jira-service-management-cloud', 'IncomingCall', 'Webhook', 'Email']
	integrations_and_keys = []
	for integration in integration_details:
		integration_name = integration[0]
		integration_id = integration[1]
		integration_type = integration[2]
		if integration_type not in no_api_key_list:
			url = "https://{}.app.opsgenie.com/webapi/v1/integrations/{}Integration/update?id={}&settings=true".format(account_name, integration_type, integration_id)
			res = requests.get(url=url, headers=web_api_headers)
			response = json.loads(res.text)
			api_key = response.get('integration').get('apiKey')
			integrations_and_keys.append({"Integration Name": integration_name, "Integration ID": integration_id, "API Key": api_key})
	return integrations_and_keys


def main():
    global headers
    global account_name
    global url
    global cookie
    web_api_headers = {'content-type': 'application/json','cookie': cookie}

    integration_details = get_integration_details(url, headers)
    api_keys = get_api_keys(integration_details, web_api_headers)
    print(api_keys)

if __name__ == '__main__':
    main()