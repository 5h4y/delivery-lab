import dns.resolver

# ANSI color codes
class Colors:
    HEADER = "\033[95m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    INFO = "\033[94m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

def color_text(text, color):
    return f"{color}{text}{Colors.ENDC}"

def fetch_dmarc_record(domain):
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, "TXT")
        for rdata in answers:
            for txt_string in rdata.strings:
                record = txt_string.decode('utf-8')
                if record.startswith("v=DMARC1"):
                    return record
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return None
    return None

def parse_dmarc_record(record):
    tags = {}
    for part in record.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            tags[key] = value
    return tags

def explain_dmarc_tags(tags):
    explanations = {
        "v": "DMARC version; there's currently only one defined version, so this should always be 1.",
        "p": {
            "none": "Policy: Monitor only; no enforcement.",
            "quarantine": "Policy: Quarantine failing messages in spam/junk.",
            "reject": "Policy: Reject failing messages outright."
        },
        "sp": {
            "none": "Subdomain Policy: Monitor only; no enforcement.",
            "quarantine": "Subdomain Policy: Quarantine failing messages in spam/junk.",
            "reject": "Subdomain Policy: Reject failing messages outright."
        },
        "rua": "Aggregate reports sent here.",
        "ruf": "Forensic reports sent here.",
        "pct": "Applies to this percentage of emails.",
        "adkim": {
            "r": "DKIM Alignment: Relaxed (subdomains allowed).",
            "s": "DKIM Alignment: Strict (exact match required)."
        },
        "aspf": {
            "r": "SPF Alignment: Relaxed (subdomains allowed).",
            "s": "SPF Alignment: Strict (exact match required)."
        },
        "fo": "Failure reporting options.",
    }

    for tag, value in tags.items():
        explanation = explanations.get(tag)
        tag_display = color_text(tag, Colors.INFO)
        value_display = color_text(value, Colors.OKGREEN)

        if isinstance(explanation, dict):
            detail = explanation.get(value, color_text(f"Unknown value '{value}' for {tag}.", Colors.WARNING))
            print(f"{tag_display}: {value_display} — {detail}")
        elif explanation:
            print(f"{tag_display}: {value_display} — {explanation}")
        else:
            print(f"{tag_display}: {value_display} — {color_text('(No standard explanation available.)', Colors.WARNING)}")

def main():
    domain = input(color_text("Enter a domain to check DMARC: ", Colors.BOLD)).strip()
    record = fetch_dmarc_record(domain)
    if not record:
        print(color_text(f"No DMARC record found for {domain}.", Colors.FAIL))
        return
    print(f"\n{color_text('DMARC Record Found:', Colors.HEADER)}\n{record}\n")
    print(color_text("Explanation:", Colors.BOLD))
    explain_dmarc_tags(parse_dmarc_record(record))

if __name__ == "__main__":
    main()
