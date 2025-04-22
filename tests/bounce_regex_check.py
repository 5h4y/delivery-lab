import re

bounce_pattern = r"450 4\.1\.8 <bounces\+\d+-[a-zA-Z0-9]+-[^@]+@([^>]+)>: Sender address rejected: Domain not found"

# Example test
test_string = "450 4.1.8 <bounces+6003214-123b-shaytest=icloudexample.com@em123.example.com>: Sender address rejected: Domain not found"
match = re.search(auth_bounce_pattern, test_string)
if match:
    sending_domain = match.group(1)
    print(sending_domain, "authentication block")
else:
    print("No match found.")
