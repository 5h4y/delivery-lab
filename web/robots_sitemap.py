import requests

def check_robots_and_sitemap(domain, show_content=False):
    for path in ["/robots.txt", "/sitemap.xml"]:
        url = f"https://{domain}{path}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"{path}: ✅ Found")
                if show_content:
                    print(f"\n--- {path} contents ---\n{r.text[:1000]}")  # limit to 1000 chars
                    if len(r.text) > 1000:
                        print("... [truncated]")
                    print("-" * 40)
            else:
                print(f"{path}: ❌ Not Found (Status {r.status_code})")
        except requests.RequestException as e:
            print(f"{path}: ❌ Error\n{e}")

if __name__ == "__main__":
    domain = input("Enter domain: ").strip()
    show = input("Wanna see the contents? (y/N): ").strip().lower() == "y"
    check_robots_and_sitemap(domain, show_content=show)

