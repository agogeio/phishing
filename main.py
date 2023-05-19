""" Application to log into email account and check emails for phishing """

# import base64
import email
# https://docs.python.org/3/library/email.parser.html
import imaplib
# https://docs.python.org/3/library/imaplib.html
import os

from email.parser import HeaderParser

email_user = os.environ.get('EMAIL_ACCOUNT')
email_pass = os.environ.get('EMAIL_PW')
imap_server = os.environ.get('IMAP_SERVER')

MAILBOX = 'INBOX'

IMAP = imaplib.IMAP4_SSL(f'{imap_server}', 993)
IMAP.login(email_user, email_pass)
IMAP.select(MAILBOX)

parser = HeaderParser() # https://docs.python.org/3/library/email.parser.html

# IMAP Commands
# https://www.atmail.com/blog/imap-commands/
status, email_ids = IMAP.search(None, 'UNANSWERED') # for unseen emails, use 'UNSEEN' instead of 'ALL'

email_ids = email_ids[0].split()

for email_id in email_ids:
    status, email_data = IMAP.fetch(email_id, '(RFC822)')
    email_data = email_data[0][1].decode('utf-8')
    # https://docs.python.org/3/library/email.parser.html
    header = parser.parsestr(email_data)
    msg = email.message_from_string(email_data)

    #? Show process of walking through all the header keys    
    # for key in header.keys():
    #     print(f'Email Header: {key} | {header[key]}')
    
    print(f'Email ID: {email_id.decode("utf-8")}')
    print(f'Header Data')
    print(f'Sender IP Address: {header["X-Sender-IP"]}')
    print(f'Sender SID-PRA: {header["X-SID-PRA"]}')
    print(f'Sender Authentication-Results: {header["Authentication-Results"]}')
    if 'spf=pass' not in header['Authentication-Results']:
        print('SPF Failed')
    else:
        print('SPF Passed')
        
    if 'dkim=pass' not in header['Authentication-Results']:
        print('DKIM Failed')
    else:
        print('DKIM Passed')

    print()
    print(f'Message From: {msg["From"]}')
    print(f'Message To: {msg["To"]}')
    print(f'Message Subject: {msg["Subject"]}')
    
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            email_body = part.get_payload()
            print(f'Message Body: {email_body}')

IMAP.close()
IMAP.logout()
