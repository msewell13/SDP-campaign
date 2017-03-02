#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import json
from os.path import join as opj
from os.path import dirname as opd
from os.path import exists as ope
import requests
from jinja2 import Environment
from jinja2 import FileSystemLoader


reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == '__main__':

    PATH = opd(os.path.abspath(__file__))
    TEMPLATES_DIR = './templates'
    TEMPLATE_FILENAME = 'first_email.html'

    env = Environment(loader=FileSystemLoader(opj(PATH, TEMPLATES_DIR)))
    template = env.get_template(TEMPLATE_FILENAME)

    context = {
    'image': 'https://s3-us-west-2.amazonaws.com/spokane-discount-properties/image.jpeg',
    'video': 'https://s3-us-west-2.amazonaws.com/spokane-discount-properties/girard.mp4',
    'address': '3319 N. Girard',
    'ARV': 250000,
    'RCE': 20000,
    'price': 150000,
    'phone': '(509) 863-3607',
    'beds': '3',
    'baths': '2',
    'sq_feet': '1,360',
    'basement': 'Full - Finishable',
    'garage': 'Detached - Very large',
    'yr_built': '1914',
    'roof': 'Newer - Comp',
    'property_type': 'Single Family',
    'neighborhood': 'Felts Field - Valley',
    'feature1': 'Tons of high quality oak woodwork and cabinets',
    'feature2': 'Literally a stones throw from Felts Field aviation park',
    'feature3': 'Large shop for all the tools and toys',
    'gallery': 'https://www.facebook.com/media/set/?set=a.1254875894592680.1073741828.1210956768984593&type=1&l=7339a8cb63',
    'paragraph': 'This property is in the valley and one of the main concerns that investors in the valley have is if the property is connected to sewer or not. This property is not conected yet but all of the city and county fees are paid for (literally thousands of dollars). The only thing left to be paid for is the actual hookup from the house to the street. It is our understanding that your own vendors may be used for this.'
    }

    template = template.render(context)
    context = json.dumps(context)

    # init data
    domain = "mg.spokanediscountproperties.com"
    base_url = 'https://api.mailgun.net/v3/{0}/messages'.format(domain)
    api_key = os.environ.get('MAILGUN_KEY')
    data = {
        'from':     'Matt@SpokaneDiscountProperties.com',
        'to':       'user@example.com',
        'subject':  "Wholesale near Felts Field",
        'html':     template,
        "v:image": "%recipient.image%",
        "v:video": "%recipient.video%",
        "v:address": "%recipient.address%",
        "v:ARV": "%recipient.ARV%",
        "v:RCE": "%recipient.RCE%",
        "v:price": "%recipient.price%",
        "v:phone": "%recipient.phone%",
        "v:beds": "%recipient.beds%",
        "v:baths": "%recipient.baths%",
        "v:sq_feet": "%recipient.sq_feet%",
        "v:basement": "%recipient.basement%",
        "v:garage": "%recipient.garage%",
        "v:yr_built": "%recipient.yr_built%",
        "v:roof": "%recipient.roof%",
        "v:property_type": "%recipient.property_type%",
        "v:neighborhood": "%recipient.neighborhood%",
        "v:feature1": "%recipient.feature1%",
        "v:feature2": "%recipient.feature2%",
        "v:feature3": "%recipient.feature3%",
        "v:gallery": "%recipient.gallery%",
        "v:paragraph": "%recipient.paragraph%",
        "recipient-variables": context
    }

    response = requests.post(base_url,
                             auth=('api', api_key),
                             data=data)
    print 'Response status code: ', response.status_code
    print 'Data: ', response.json()
