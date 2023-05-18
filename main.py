""" Application to log into email account and check emails for phishing """

# import base64
import email
# https://docs.python.org/3/library/email.parser.html
import imaplib
# https://docs.python.org/3/library/imaplib.html
import os

email_user = os.environ.get('EMAIL_ACCOUNT')
email_pass = os.environ.get('EMAIL_PW')
imap_server = os.environ.get('IMAP_SERVER')

MAILBOX = 'INBOX'


IMAP = imaplib.IMAP4_SSL(f'{imap_server}', 993)
IMAP.login(email_user, email_pass)
IMAP.select(MAILBOX)

# IMAP Commands
# https://www.atmail.com/blog/imap-commands/
status, email_ids = IMAP.search(None, 'UNANSWERED') # for unseen emails, use 'UNSEEN' instead of 'ALL'

email_ids = email_ids[0].split()

for email_id in email_ids:
    status, email_data = IMAP.fetch(email_id, '(RFC822)')
    email_data = email_data[0][1].decode('utf-8')
    # https://docs.python.org/3/library/email.parser.html
    msg = email.message_from_string(email_data)
    
    # print(msg)
    
    print(msg['From'])
    print(msg['To'])
    print(msg['Subject'])
    
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            print(part.get_payload())
            
        if part.get_payload
            continue

IMAP.close()
IMAP.logout()
