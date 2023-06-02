import json
import os
import requests

def get_safe_browsing_report(submit_url: str, sb_api_key) -> bool:
    """Accept a single url as a string and return a boolean value"""
    #? URL for the safe browsing API
    
    if sb_api_key is None:
        print('No Safe Browsing API key found')
        exit(1)
    
    url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=' + sb_api_key

    #? https://developers.google.com/safe-browsing/v4/lookup-api 
    payload = {
                "client": {
                "clientId":      "agoge.io",
                "clientVersion": "1.5.2"
                },
                "threatInfo": {
                "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes":    ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": submit_url},
                ]
                }
            }

    #? https://developers.google.com/safe-browsing/v4/reference/rest/v4/ThreatInfo
    #? To understand the options in the payload, read the above link
    
    try:
        response = requests.post(url, json=payload)
    except Exception as err:
        print(err)
    else:
        #? https://developers.google.com/safe-browsing/v4/lookup-api
        #? If there is no threat detected, the response will be an empty JSON object
        
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json.get('matches'):
                return { 'URL' : submit_url, 'Result' : True}
            else:
                return { 'URL' : submit_url, 'Result' : False}


if __name__ == '__main__':
    sb_api_key = os.environ.get('safe_browsing')
    
    #? https://testsafebrowsing.appspot.com/ 
    #? provides a list of URLs that you can use for testing
    test_phishing = 'https://testsafebrowsing.appspot.com/s/phishing.html'
    test_malware = 'https://testsafebrowsing.appspot.com/s/malware.html'
    print(get_safe_browsing_report(test_malware, sb_api_key))