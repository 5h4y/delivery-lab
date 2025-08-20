'''
Super basic mailbox validation. 

- checks MX records
- connects to the mail server
- simulates an SMTP session without actually sending an email
- 250 response = mailbox is more likely to exist
- otherwise, nope

Keep in mind that some servers will return positive/generic/negative responses regardless of input (Gmail, MSFT, etc.). This is not definitive evidence and you shouldn't rely on it. Think of it more as a potentially useful data point.  

'''

import smtplib
import dns.resolver

def validate_mailbox(email_address, from_address="validator@test.com"):
    try:
        domain = email_address.split("@")[1]

        answers = dns.resolver.resolve(domain, "MX")
        mx_record = sorted(answers, key=lambda r: r.preference)[0].exchange.to_text()
        print(f"MX Record Found: {mx_record}")

        server = smtplib.SMTP(mx_record, 25, timeout=10)
        server.ehlo_or_helo_if_needed()

        server.mail(from_address)
        code, message = server.rcpt(email_address)

        if code == 250:
            print(f"Mailbox probably exists: {email_address}")
        elif code == 550:
            print(f"Mailbox probably does NOT exist: {email_address}")
        else:
            print(f"Who knows, dude. Response: ({code}): {message.decode()}")

        server.quit()

    except dns.resolver.NXDOMAIN:
        print(f"Domain does not exist: {domain}")
    except dns.resolver.NoAnswer:
        print(f"No MX record found for domain: {domain}")
    except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as e:
        print(f"SMTP Connection Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    email = input("Enter email address: ").strip()
    validate_mailbox(email)
