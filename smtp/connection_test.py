import smtplib
import dns.resolver

def smtp_check(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX")
        mx_record = sorted(answers, key=lambda r: r.preference)[0].exchange.to_text()
        print(f"🔍 Trying SMTP on: {mx_record}")

        server = smtplib.SMTP(mx_record, 25, timeout=5)
        banner = server.docmd("HELO", "test.com")
        print(f"✅ SMTP connection successful — HELO banner: {banner}")
        server.quit()
    except Exception as e:
        print(f"❌ Could not connect to SMTP: {e}")

if __name__ == "__main__":
    domain = input("Enter domain (e.g. example.com): ").strip()
    smtp_check(domain)

