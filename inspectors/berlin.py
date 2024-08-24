import requests
from bs4 import BeautifulSoup as bs



headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_jobs_berlin(soup):
    berlin_job_list = []
    info_boxes = soup.select('div.bjs-jlid__wrapper')
    print("belin")
    for box in info_boxes:
        whisper_box = box.select_one('div.links-box')
        whispers = whisper_box.select('a.bjs-bl.bjs-bl-whisper')

        company = box.select_one('a.bjs-jlid__b').get_text()
        title = box.select_one('h4.bjs-jlid__h').get_text()
        whisper = ', '.join([w.get_text().strip() for w in whispers])
        link = box.select_one('h4.bjs-jlid__h a').attrs['href']        
        
        berlin_info = {
            'company': company,
            'title': title,
            'whisper': whisper,
            'link': link,
            'base': 'berlin'
        }
        print(berlin_info)
        berlin_job_list.append(berlin_info)
    return berlin_job_list
    


def access_url_berlin(url, keyword):        
    url = url + keyword
    res = requests.get(url, headers=headers)
    print(f"{url}\tstatus_code:{res.status_code}")
    if res.status_code >= 300:
        raise Exception(f"Request fail: {res.status_code}")
    soup = bs(res.text, 'html.parser')
    return soup



