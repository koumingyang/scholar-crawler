from lxml import etree
import requests
import xlrd
import time
import csv

search_url = 'https://www.google.com/search?q=google+scholar+citations+{}'
'''
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
'''
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "7726eab62c65435499c4d48190eb7824:" # Make sure to include ':' at the end
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
      "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

table = xlrd.open_workbook('exportAwards-2016.xls')
sheet = table.sheet_by_index(0)
column2 = sheet.col_values(2)[1:]

f = open('result.csv', 'w', newline='', encoding='utf8')
table_header = ['Researcher', 'ID', 'Title', 'Authors', 'Publication date', 'Journal', 'Volume', 'Issue', 'Pages', 'Publisher', 'Description']
index = ['Title', 'Authors', 'Publication date', 'Journal', 'Volume', 'Issue', 'Pages', 'Publisher', 'Description']
writer = csv.DictWriter(f, table_header)
writer.writeheader()

for ID, researcher in enumerate(column2):
	response = requests.get(search_url.format(researcher.replace(' ', '+')), proxies=proxies,
                 verify=False)
	html = etree.HTML(response.text)
	result = html.xpath('//h3[@class="r"]/a')
	
	if not result:
		print('can not find {}'.format(researcher))
		continue
	
	target = 'http://scholar.google.com/citations?user=' + \
		result[0].get('href').split('%')[2][2:] + \
		'&sortby=pubdate'
	response = requests.get(target, proxies=proxies,
                 verify=False)
	html = etree.HTML(response.text)
	result = html.xpath('//a[@class="gsc_a_at"]')
	year = html.xpath('//span[@class="gs_oph"]')

	if not result:
		print('can not find paper by {}'.format(researcher))
		continue

	for i, j in zip(result, year):
		if int(j.text[2:]) > 2015:
			time.sleep(2)
			data = {'Researcher': researcher, 'ID': ID + 1}
			target = 'https://scholar.google.com' + i.get('data-href')
			response = requests.get(target, proxies=proxies,
                 verify=False)
			html = etree.HTML(response.text.replace('<br>', ''))
			try:
				title = html.xpath('//div[@id="gsc_vcd_title"]/a')[0].text
				print(title)
			except:
				continue
			# print('title:' + title)
			data['Title'] = title
			filed = html.xpath('//div[@class="gsc_vcd_field"]')
			value = html.xpath('//div[@class="gsc_vcd_value"]')
			if (not filed) or (not value):
				continue
			for (f_, v_) in zip(filed, value):
				if f_.text in index:
					data[f_.text] = v_.text
			writer.writerow(data)
		else:
			break
				# print(index[i] + information[i].text)
f.close()