import csv
from flask import Flask, redirect, render_template, request, send_file
from inspectors.berlin import access_url_berlin, get_jobs_berlin
from inspectors.web3 import access_url_web3, get_jobs_web3



app = Flask(__name__)


#파일저장
def save_csv_file(file_path, keyword):
    
    #경로에 파일 만들기
    with open(file_path, "w", newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ["Title", "Company", "Wisper", "Link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader() #필드넣기
        for job_dict in db[keyword]:
            writer.writerow({
                "Title": job_dict['title'],
                "Company": job_dict['company'],
                "Wisper": job_dict['whisper'],
                "Link": job_dict['link']
            })



#headers & variables
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

berlin_url = "https://berlinstartupjobs.com/skill-areas/"
web3_url = "https://web3.career"

db = {}

@app.route('/')
def test():
    return render_template('home.html')


@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword in db:
        keyword_jobs = db[keyword]
    else:
        #berlin scrapper: 페이징 없음
        soup = access_url_berlin(berlin_url, keyword)
        berlin_info_list = get_jobs_berlin(soup)


        #web3 scrapper: 페이징 있음
        page = 1        
        while page < 4:             
            print("web3\t", page)
            soup = access_url_web3(web3_url, keyword, page)
            error = soup.select_one('div.header h1')
            if error:
                if error.get_text() == "404":
                    web3_info_list = []
                    break   
            else:
                #next버튼 없을 경우 종료
                next_btn = soup.select_one('li.page-item.next')
                if next_btn == None:
                    break                            
                web3_info_list = get_jobs_web3(soup, web3_url)
                page += 1
        keyword_jobs = berlin_info_list + web3_info_list #berlin + web3
        db[keyword] = keyword_jobs #db저장


    return render_template(
        'searchList.html',
        keyword=keyword,
        keyword_jobs=keyword_jobs
    )


@app.route('/export')
def export():
    keyword = request.args.get('keyword')
    
    if keyword is None: #keyword없을 때
        return redirect('/')
        
    if keyword not in db: #db에 없을때: 검색하지 않고 url로 들어왔을때
        return redirect(f'/search?keyword={keyword}')

    #정상실행
    file_path = f"{keyword}.csv"
    save_csv_file(file_path, keyword) #파일저장

    return send_file(file_path, as_attachment=True) #다운로드



if __name__ == "__main__":
    app.run(debug=True)
