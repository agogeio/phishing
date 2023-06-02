""" Check Email from an IMAP Server """
import bs4
#* https://pypi.org/project/beautifulsoup4/
#* https://www.crummy.com/software/BeautifulSoup/
import imapclient
import json
#* https://pypi.org/project/IMAPClient/
import os
import pyzmail
#* https://www.magiksys.net/pyzmail/
#* https://pypi.org/project/pyzmail39/
#* Had to use 39 because: "At installation time, pyzmail sources are automatically converted by distribute using 2to3.""

from google_sb import safebrowsing


EMAIL_USER = os.environ.get('EMAIL_ACCOUNT')
EMAIL_PASS = os.environ.get('EMAIL_PW')
IMAP_SERVER = os.environ.get('IMAP_SERVER')
MAILBOX = 'INBOX'

IP_HEADERS = [
    'src_ip',
    "Received",
    'X-Orig-ip',
    "X-Originating-IP",
    "X-Sender-IP",
    "X-Sender",
    "X-Original-Sender",
    "X-Sender-Domain",
    "X-From",
    "Reply-To",
]

def extract_links(email_body) -> list:
    link_list = []
    soup = bs4.BeautifulSoup(email_body, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            link_list.append(href)
            
    return link_list


def get_emails() -> None :
    try:
        #* Log into to the IMAP server and get a list of all emails
        IMAP = imapclient.IMAPClient(IMAP_SERVER, ssl=True)
        IMAP.login(EMAIL_USER, EMAIL_PASS)
        IMAP.select_folder(MAILBOX)
        UIDS = IMAP.search(['ALL'])
        print(f"UIDS: {UIDS}")
    except Exception as e:
        print(e)
    else:
        for UID in UIDS:
            #* Get the contents of individual emails
            raw_message = IMAP.fetch([UID],['BODY[]'])
            try:
                pass
            except Exception as e:
                print(e)
            else:    
                message = pyzmail.PyzMessage.factory(raw_message[UID][b'BODY[]'])
                print("\n****** Begin Email Message ******")
                print(f"To: {message.get_address('to')}")
                print(f"From: {message.get_address('from')}")
                print(f'Subject: {message.get_subject()}')

                for ip_header in IP_HEADERS:
                    if message.get_decoded_header(ip_header):
                        print()
                        print(f"{ip_header} Header: {message.get_decoded_header(ip_header)}")
                
                if message.text_part is not None:
                    print(message.text_part.get_payload().decode(message.text_part.charset))
                elif message.html_part is not None:
                    print('Identified Links in the Email Are:')
                    response = message.html_part.get_payload().decode(message.html_part.charset)
                    urls = extract_links(response)
                    print(urls)
                print("****** End Email Message ******\n")


if __name__ == '__main__':
    get_emails()
    