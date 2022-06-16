from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager




# Create your views here.
# def main(request):
#     return render(
#         request,
#         'main_page/main.html'
#     )

def crawling(request):
    options = Options()
    options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
    options.add_argument('--incognito')    # 시크릿모드
    options.add_argument('--headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
    options.add_argument('--no-sandbox')# 대부분 리소스에 대한 액세스를 방지
    options.add_argument('--disable-dev-shm-usage')## 메모리 부족 에러 방지
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--window-size=1920x1080')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.implicitly_wait(time_to_wait=10)
    driver.get('http://127.0.0.1:8000/community/')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    post_data = []

    post_list = soup.find_all("div",{"class":"post_label"})

    for i in range(len(post_list)-1,-1,-1):
        row = post_list[i].find("div",{'class':'row'})
        url = row.select_one("a").get("href")
        title = row.find("h3").text.strip()
        heart = row.find("i",{"class":"fa-heart"}).text.strip()[:-1]
        heart = int(heart)
        post_data.append([url,title,heart])

    sorted_post_data = sorted(post_data, key=lambda x : (-x[2], x[2]))
    for i in range(len(sorted_post_data)):
        sorted_post_data[i].append(i)

    context ={
        'data':sorted_post_data
    }

    return render(request, 'main_page/main.html', context)

    