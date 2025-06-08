import os
import time
from sendgrid import SendGridAPIClient

def load_emails_from_file(file_path):
    with open(file_path, 'r') as file:
        emails = [line.strip() for line in file if line.strip()]  # strip whitespace etc
    return emails

# batching so SG doesn't get angry
def batch_emails(emails, batch_size=1000):
    for i in range(0, len(emails), batch_size):
        yield emails[i:i + batch_size]

email_list_file = 'flagged_for_suppression.txt'
emails_to_suppress = load_emails_from_file(email_list_file)

# init SG API
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

# batched
email_batches = batch_emails(emails_to_suppress, batch_size=1000)

# process batches
for batch_num, batch in enumerate(email_batches, start=1):
    data = {
        "recipient_emails": batch
    }
    
    try:
        # send suppression request using getattr to handle 'global' keyword
        response = getattr(sg.client.asm.suppressions, 'global').post(
            request_body=data
        )
        
        # response status for debugging
        print(f"Batch {batch_num} - Status Code: {response.status_code}")
        if response.status_code != 201:
            print(f"Batch {batch_num} - Failed: {response.body}")
        
    except Exception as e:
        print(f"An error occurred with batch {batch_num}: {e}")
    
    # quick nap to avoid rate limits
    time.sleep(1)