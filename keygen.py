"""
THIS SCRIPT IS USED FOR EDUCATIONAL PURPOSES ONLY. DO NOT USE IT IN ILLEGAL WAY!!!
"""

import base64
from datetime import datetime
from hashlib import sha1
import zlib
from M2Crypto import DSA


def keymaker(organisation, server_id, license_edition, license_type_name, purchase_date=datetime.today(), private_key='./private.pem'):
    license_types = ('ACADEMIC', 'COMMERCIAL', 'COMMUNITY', 'DEMONSTRATION', 'DEVELOPER', 'NON_PROFIT', 'OPEN_SOURCE', 'PERSONAL', 'STARTER', 'HOSTED', 'TESTING')
    license_editions = ('BASIC', 'STANDARD', 'PROFESSIONAL', 'ENTERPRISE')
    if license_type_name not in license_types:
        raise ValueError('License Type Name must be one of the following values:\n\t%s' % ', '.join(license_types))
    if license_edition not in license_editions:
        raise ValueError('License Edition must be one of the following values:\n\t%s' % ', '.join(license_editions))

    header = purchase_date.ctime()
    properties = {
        'Description': 'JIRA\\: Developer',
        'CreationDate': purchase_date.strftime('%Y-%m-%d'),
        'jira.LicenseEdition': license_edition,
        'Evaluation': 'false',
        'jira.LicenseTypeName': license_type_name,
        'jira.active': 'true',
        'licenseVersion': '2',
        'MaintenanceExpiryDate': '2099-12-31',
        'Organisation': organisation,
        'jira.NumberOfUsers': '-1',
        'ServerID': server_id,
        'SEN': 'SEN-L0000000',
        'LicenseID': 'LIDSEN-L0000000',
        'LicenseExpiryDate': '2099-12-31',
        'PurchaseDate': purchase_date.strftime('%Y-%m-%d')
    }
    properties_text = '#%s\n%s' % (header, '\n'.join(['%s=%s' % (key, value) for key, value in properties.iteritems()]))
    compressed_properties_text = zlib.compress(properties_text, 9)
    license_text_prefix = map(chr, (13, 14, 12, 10, 15))
    license_text = ''.join(license_text_prefix + [compressed_properties_text])

    dsa = DSA.load_key(private_key)
    assert dsa.check_key()
    license_signature = dsa.sign_asn1(sha1(license_text).digest())
    license_pair_base64 = base64.b64encode('%s%s%s' % (unichr(len(license_text)).encode('UTF-32BE'), license_text, license_signature))
    license_str = '%sX02%s' % (license_pair_base64, base_n(len(license_pair_base64), 31))
    return license_str


def main():
    license_edition = 'ENTERPRISE'
    license_type_name = 'DEVELOPER'
    organisation = 'PUT YOUR ORGANIZATION NAME'  # Change this to what you like
    server_id = 'ABCD-1234-EFGH-5678'  # Change this to your server ID
    print(keymaker(organisation, server_id, license_edition, license_type_name))


def base_n(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and "0") or (base_n(num // b, b).lstrip("0") + numerals[num % b])

if __name__ == '__main__':
    main()