import os, re, json
from twilio.rest import Client

''' 
This script uses Twilio's Line Type Intelligence API to identify carrier, line type, known issues, country, etc.

It's cost-prohibitive for many businesses to programmatically implement this. But for one-offs or small batches when you need to troubleshoot/explain an SMS delivery problem for a client, I find it helpful. 

'''

account_sid = os.environ['TWILIO_ACCOUNT_SID'] 
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

raw = input("Phone number: ").strip()
digits = re.sub(r'\D', '', raw)

if raw.startswith('+') and digits:
    e164 = f'+{digits}'
elif len(digits) == 10:           # quick e164 normalization, US default
    e164 = f'+1{digits}'
else:
    e164 = f'+{digits}'

resp = client.lookups.v2.phone_numbers(e164)\
    .fetch(fields='line_type_intelligence')

lti = resp.line_type_intelligence or {}
carrier = lti.get("carrier_name")
mcc = (lti.get("mobile_country_code") or "").strip() 
mnc = (lti.get("mobile_network_code") or "").strip()
plmn_hyphen = f"{mcc}-{mnc}" if mcc and mnc else None   
plmn6 = f"{mcc}{mnc.zfill(3)}" if mcc and mnc else None  # auto converting country/network codes to PLMN IDs for mobile  
lt = (lti.get("type") or "")
error = lti.get("error_code")

parsed = {
    "e164 format": e164,
    "carrier": lti.get("carrier_name"),
    "country": mcc,
    "mobile network": mnc,
    "plmn": plmn_hyphen,   
    "plmn6": plmn6,        
    "line": lt or "unknown",
    "is_mobile": lt == "mobile",
    "error": lti.get("error_code"),
}

print(json.dumps(parsed, indent=2))
# print(json.dumps(lti, indent=2)) <-- raw dump for debugging 
