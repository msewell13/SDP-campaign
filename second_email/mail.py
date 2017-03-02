import email.utils, time
import requests
import os
import sys


domain = "mg.spokanediscountproperties.com" 
api = os.environ.get('MAILGUN_KEY')
request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(domain)
brand = "SpokaneDiscountProperties.com"
future30minutes = time.time() + 30 * 60;

html_filename = './templates/welcome_mail.html'
if not open(html_filename):
    print 'File doesn\'t exist. Check it.'
    sys.exit(0)

html_file_content = str()
with open(html_filename) as fp:
    html_file_content = fp.read()
    
def sendHtmlMessage(recipient, subject):
    return requests.post(
        request_url,
        auth=("api", api),
        data={"from": "{} <Matt@{}>".format(brand, brand),
              "to": "{}".format(recipient),
              "subject": subject,
              "html": html_file_content,
              "o:deliverytime": email.utils.formatdate(future30minutes)})