import requests

url = "http://www.google.com"
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "7726eab62c65435499c4d48190eb7824:" # Make sure to include ':' at the end
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


