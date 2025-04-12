'''
Super basic SNDS data retrieval + parsing function. Returns CSV data as a list of lists which makes it easy to load into a DataFrame, use in dashboards, etc.  
'''
import os
import requests
import csv
from io import StringIO

SNDS_KEY = os.getenv("SNDS_KEY")

def pull_snds_data(snds_key_url):
    try:
        response = requests.get(snds_key_url)
        response.raise_for_status()
        
        # MSFT provides as .CSV
        f = StringIO(response.text)
        reader = csv.reader(f, delimiter=',')
        snds_data = list(reader)
        return snds_data

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

'''
The data returned by the first URL, the View Data page, is identical to the result of pushing the Export to .CSV button on that page.  To request data for a specific date, append "&date=MMDDYY" to the URL (for example: "&date= 030406" for data for the day of March 4, 2006 in Pacific Standard Time).  To request a sample message, either of type "complaint" or "trap", for a given IP and date, append the following in addition to the data parameter:"&ip=1.2.3.4&sampletype=trap".

Example complaint URL: ""https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={SNDS_KEY}&date=020525&ip=149.72.185.106&sampletype=complaint""

'''

def main():
    snds_key_url = f"https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={SNDS_KEY}"

    snds_data = pull_snds_data(snds_key_url)
    if snds_data:
        print("SNDS Data:")
        for row in snds_data:
            print(row)  # needs formatting, columns = IP address, Activity Period [start, finish], RCPT commands, DATA commands, Message recipients, Filter result, Complaint rate, Trap message period, Trap hits, Sample HELO, JMR P1 Sender, Comments

if __name__ == '__main__':
    main()