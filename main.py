from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs



app = Flask(__name__)

#headers & variables
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
base_url1 = "https://berlinstartupjobs.com/"
base_url2 = "https://web3.career/"
base_url3 = "https://weworkremotely.com/remote-jobs/"
base_urls = [base_url1, base_url2, base_url3]



@app.route('/')
def test():
    return render_template('home.html')




@app.route('/search')
def search():
    #company, title, link, description
    #skils = ["python", "typescript", "javascript", "rust"]
    keyword = request.args.get('keyword')

    page = 1
    for base_url in base_urls:
        if 'berlin' in base_url:
            while True:
                url = base_url + f"?s={keyword}&page={page}"
                print(url)
                res = requests.get(url, headers=headers)
                soup = bs(res.text, 'html.parser')
                print("soup complete")
                next_page = soup.select_one('li.nextPage')
                print(next_page)                
                
                if not next_page:
                    print('no next_page')
                    break
                page += 1


        elif 'web3' in base_url:
            pass
            

        elif 'wework' in base_url:
            pass


    

    



    return render_template('searchList.html', keyword=keyword)



if __name__ == "__main__":
    app.run(debug=True)
