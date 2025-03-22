import dns.resolver
import dns.reversename
import argparse
import ipaddress
import json

def get_ptr_record(target):
    try:
        # is IP?
        ip = ipaddress.ip_address(target)
        rev_name = dns.reversename.from_address(str(ip))
        ptr = dns.resolver.resolve(rev_name, "PTR")[0]
        return {"target": target, "ptr_record": str(ptr)}
    except ValueError:
        # if not, try rDNS
        try:
            ip = dns.resolver.resolve(target, "A")[0].to_text()
            rev_name = dns.reversename.from_address(ip)
            ptr = dns.resolver.resolve(rev_name, "PTR")[0]
            return {"target": target, "ip": ip, "ptr_record": str(ptr)}
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            return {"error": f"No PTR record found for {target}"}
        except dns.exception.DNSException:
            return {"error": f"Invalid domain or IP address: {target}"}

def process_list(file_path):
    with open(file_path, 'r') as file:
        targets = [line.strip() for line in file if line.strip()]
    results = [get_ptr_record(target) for target in targets]
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query PTR records for an IP or domain.")
    parser.add_argument("target", help="IP address, domain, or file path to a list of targets")
    args = parser.parse_args()

    if args.target.endswith('.txt'):
        process_list(args.target)
    else:
        print(json.dumps(get_ptr_record(args.target), indent=2))
