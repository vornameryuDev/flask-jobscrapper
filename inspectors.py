from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs



headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
skills = ["python", "typescript", "javascript", "rust"]




            
        
#keyword > url에 박힘

url1 = f"https://berlinstartupjobs.com/?s=python&page=1"
    # url2 = f"https://web3.career/{keyword}-jobs"
    # url3 = f"https://weworkremotely.com/remote-jobs/search?search_uuid=&term={keyword}"

res = requests.get(url1, headers=headers)
soup = bs(res.text, 'html.parser')
nextBtn = soup.find('a.ais-Pagination-link')
print(nextBtn)