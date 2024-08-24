import requests
from bs4 import BeautifulSoup as bs




headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def access_url_web3(url, keyword, page):    
    url = url + f"/{keyword}-jobs?page={page}"
    res = requests.get(url, headers=headers)    
    soup = bs(res.text, 'html.parser')
    return soup

def get_jobs_web3(soup, url):
    web3_info_list = []
    tbody = soup.select_one('tbody.tbody') #구역찾기
    trs = tbody.select('tr.table_row') #세부구역
    for tr in trs:
        title=tr.select_one('h2.fs-6.fs-md-5.fw-bold.my-primary')
        if title != None:
            title = title.get_text()

        company = tr.select_one('td.job-location-mobile')
        if company != None:
            company = company.get_text()

        whispers = tr.select('span.my-badge.my-badge-secondary')
        if whispers != None:
            whisper = [w.get_text().strip() for w in whispers]
        whispers = []            

        link = tr.select_one('div.mb-auto.align-middle.job-title-mobile a')
        if link != None:
            link = link.attrs['href']
            link = url + link
        web3_info = {
            'company': company,
            'title': title,
            'whisper': ', '.join(whisper),
            'link': link,
            'base': 'web3'
        }
        print(web3_info)
        web3_info_list.append(web3_info)
    return web3_info_list


