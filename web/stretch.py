import requests

def unwrap_url(shortened_url):
    try:
        response = requests.head(shortened_url, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Could not unwrap {shortened_url}: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter shortened URL: ")
    expanded_url = unwrap_url(url)

    if expanded_url:
        print(f"Expanded URL: {expanded_url}")
    else:
        print(f"Could not unwrap {url}.")


# test URL (wikipedia): https://tinyurl.com/2p8x3767