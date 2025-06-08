import os
import json
import dns.resolver
from datetime import datetime
from sendgrid import SendGridAPIClient
from termcolor import colored

# init SG client
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

# check DNS against expected SG values
def check_dns_records(subdomain, root_domain):
    expected_values = {
        f'{subdomain}': 'INSERT_EXPECTED_VALUE',
        f's1._domainkey.{root_domain}': 's1.domainkey.INSERT_EXPECTED_VALUE',
        f's2._domainkey.{root_domain}': 's2.domainkey.INSERT_EXPECTED_VALUE',
    }
    records_found = {}
    for record, expected in expected_values.items():
        try:
            answers = dns.resolver.resolve(record, 'CNAME')
            for answer in answers:
                if expected in answer.target.to_text():
                    records_found[record] = 'Present'
                else:
                    records_found[record] = 'Mismatch'
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            records_found[record] = 'Missing'
    return records_found

# is DMARC present?
def check_dmarc_record(root_domain):
    try:
        answers = dns.resolver.resolve('_dmarc.' + root_domain, 'TXT')
        return ', '.join([answer.to_text().strip('"') for answer in answers])
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return 'No DMARC Record found'

# process domains
def process_domains(domain):
    query_params = {"domain": domain}
    response = sg.client.whitelabel.domains.get(query_params=query_params)
    domains_data = json.loads(response.body)

    for domain_info in domains_data:
        subdomain = domain_info["subdomain"] + "." + domain_info["domain"]
        root_domain = domain_info["domain"]
        valid = domain_info["valid"]
        last_validation_attempt = domain_info.get("last_validation_attempt_at")
        if last_validation_attempt:
            last_validation_attempt = datetime.fromtimestamp(last_validation_attempt).strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_validation_attempt = "N/A"

        print(f"\nSubdomain: {subdomain}, Domain: {root_domain}, Valid: {valid}, Last Validation Attempt: {last_validation_attempt}")


'''
wishlist:

- subusers 
- brief DMARC analysis
- nameservers
- MX check
    - query common DKIM selectors etc.
    - 
'''