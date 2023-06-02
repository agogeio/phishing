""" Utility Functions for PiParse """

import json
import re
import whois

def check_is_ip(ip_address) -> bool:
    """ Accepts a string and returns True if it is an IP address """
    IP_REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(IP_REGEX, ip_address):
        return True
    else:
        return False


def get_domain_newer_than_year(whois_file, newer_than_year) -> list:
    whois_data = whois_file
    creation_years = []
    
    try:
        with open(whois_data, 'r', encoding='utf-8') as whois_file:
            whois_data = json.load(whois_file)    
    except Exception as err:
        print(err)
    else:
        for domain in whois_data:
            
            try:
                if not domain['domain_name']:
                    continue
                
                if not domain['creation_date']:
                    print(f">>> {domain['domain_name']} - with no creation date")
                    continue
                
            except KeyError as err:
                print(f'Key Error of: {err} for domain: {domain["domain_name"]}')
                
            else:
                if type(domain['domain_name']) == list: 
                    domain_name = domain['domain_name'][0]
                elif type(domain['domain_name']) == str:
                    domain_name = str(domain["domain_name"])
            
                if type(domain['creation_date']) == list: 
                    creation_date = domain['creation_date'][0]
                else:
                    creation_date = str(domain["creation_date"])


                creation_date_list = creation_date.split(' ')
                creation_year_month_day = creation_date_list[0]
                creation_year = creation_year_month_day.split('-')[0]
              
                if int(creation_year) > int(newer_than_year):
                    domain_data = {'domain_name': domain_name,
                                   'creation_year': creation_year}
                    # print(f'{domain_data}')
                    creation_years.append(domain_data)
                    
    return creation_years


def get_whois(domain_list) -> list:
    """ Accepts a URL list and returns whois data in form a list of dictionaries"""
    whois_list = [] 
    try:
        with open(domain_list, 'r', encoding='utf-8') as domains:
            for domain in domains:
                domain = domain.strip()
                if not check_is_ip(domain):
                    try:
                        whois_info = str(whois.whois(domain))
                        whois_json = json.loads(whois_info)
                        whois_list.append(whois_json)
                        
                        print(f'{domain} added to whois_data')
                    except Exception as err:
                        print(f'Whois error - {err}')
    except Exception as err:
        print(err)

    return whois_list


def write_whois_to_log(whois_data, log_path) -> None:
    """ Accepts a list of whois dictionaries and writes them to a JSON file """
    try:
        with open(log_path, 'w', encoding='utf-8') as whois_file:
            json.dump(whois_data, whois_file, indent=4)
    except Exception as err:
        print(err)
        
        
