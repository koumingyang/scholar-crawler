import requests

url = "http://httpbin.org/ip"
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "ae1e63bb02d94301898ddf121e5efb3e:" # Make sure to include ':' at the end
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