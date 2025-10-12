import requests

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
    "Expect-CT",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Resource-Policy",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def check_security_headers(domain):
    if not domain.startswith("http"):
        domain = "https://" + domain

    try:
        response = requests.get(domain, headers=HEADERS, timeout=5)
        headers = response.headers

        #print(response.url)
        #print(response.status_code)
        #print(response.headers) 

        print(f"\n Security headers for {domain}:\n")

        for h in SECURITY_HEADERS:
            val = headers.get(h)
            if val:
                print(f" {h}: {val}")
            else:
                print(f"⚠️  {h} not present")
    except requests.exceptions.RequestException as e:
        print(f"\n Could not reach {domain}\n{e}")

check_security_headers(input("Enter domain: "))

'''
future ideas: 
- snazz up output w/ colorama etc
- more sophisticated validation/sanitization
- CLI arguments, maybe?
    - quick explanations of each header + context/relevance might be helpful
    - output spec
- grade or score based on what's present
- output to md, json, csv, etc.
- warnings for weaknesses, missing directives, overly permissive policies
- HSTS subdomain precheck
- check for redirects
- compare with other tools or results
- subdomain support **
'''