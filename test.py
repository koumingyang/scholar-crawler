import requests

url = "https://www.google.com/search?q=google+scholar+citations+Katherine+McMillan"
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "<175911a0b77a47148042c9e1b75bf3eb>:" # Make sure to include ':' at the end
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
      "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

r = requests.get(url, proxies=proxies,
                 verify=False)

print("""
Requesting [{}]
through proxy [{}]

Request Headers:
{}

Response Time: {}
Response Code: {}
Response Headers:
{}

""".format(url, proxy_host, r.request.headers, r.elapsed.total_seconds(),
           r.status_code, r.headers, r.text))


