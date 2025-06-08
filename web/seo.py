import requests
from bs4 import BeautifulSoup

SEO_TAGS = {
    "title": lambda soup: soup.title.string if soup.title else None,
    "meta[name=description]": lambda soup: soup.select_one("meta[name=description]") and soup.select_one("meta[name=description]")["content"],
    "meta[name=robots]": lambda soup: soup.select_one("meta[name=robots]") and soup.select_one("meta[name=robots]")["content"],
    "link[rel=canonical]": lambda soup: soup.select_one("link[rel=canonical]") and soup.select_one("link[rel=canonical]")["href"],
    "meta[property=og:title]": lambda soup: soup.select_one("meta[property='og:title']") and soup.select_one("meta[property='og:title']")["content"],
    "meta[property=og:description]": lambda soup: soup.select_one("meta[property='og:description']") and soup.select_one("meta[property='og:description']")["content"],
    "meta[name=twitter:card]": lambda soup: soup.select_one("meta[name='twitter:card']") and soup.select_one("meta[name='twitter:card']")["content"],
}

def check_seo_tags(domain):
    if not domain.startswith("http"):
        domain = "https://" + domain

    try:
        response = requests.get(domain, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        print(f"\n🔍 SEO tag check for {domain}:\n")

        for tag, extractor in SEO_TAGS.items():
            try:
                value = extractor(soup)
                if value:
                    print(f"✅ {tag}: {value[:100]}{'...' if len(value) > 100 else ''}")
                else:
                    print(f"⚠️  {tag} not found")
            except Exception as e:
                print(f"❌ Error checking {tag}: {e}")

    except requests.RequestException as e:
        print(f"\n❌ Could not retrieve {domain}\n{e}")

check_seo_tags(input("Enter domain: "))
