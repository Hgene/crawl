from bs4 import BeautifulSoup as bs
import urllib
from selenium import webdriver
import time
import pandas as pd

import ssl
context = ssl._create_unverified_context()


def get_links(url,count, Img_Str):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    for c_i in range(count):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight*0.85);")

    htmlSource = driver.page_source
    soup = bs(htmlSource, 'html.parser')
    site = soup.find_all("a",{'class':Img_Str})
    driver.quit()

    links=[]
    baseurl = 'https://www.wadiz.kr/'
    for site_i in site:
        links.append(baseurl + site_i['href'])
    print('======  총 회사 수 : ',len(site),'======')

    return links

def get_info(url):
    page = urllib.request.urlopen(url, context=context)

    soup = bs(page, 'html.parser') # Soup으로 만들어 줍시다.
    company = soup.find('div',attrs={'class':"maker-info"})
    company = company.find('p',attrs={'class':'name'}).text

    contact = soup.find('div',attrs={'class':"contact-info"})
    mail = contact.find('p',attrs={'class':'mail'}).text
    phone = contact.find('p',attrs={'class':'phone'}).text

    return [company, mail, phone]

if __name__ == '__main__':

    number = input("원하는 타입을 입력하세요. 1:추천순, 2:인기순, 3:펀딩액순, 4:마감임박순, 5:최신순, 6:응원참여자순 \n")
    number = int(number)
    dict1 = {1: 'recommend', 2: 'popluar', 3: 'amount', 4: 'closing', 5: 'recent', 6: 'support'}
    print("'======  Type : ", dict1[number],'======')

    url = 'https://www.wadiz.kr/web/wreward/category?keyword=&endYn=N&order={}'.format(dict1[number])
    count = input("page Down 수를 입력하세요(최소 10이상) \n")
    count = int(count)
    print("'======  Page down : ",count,'======')

    Img_Str = "ProjectCardLink_link__3iR_4 CommonProjectCard_image__6--Wu" #Only this part you can change
    links = get_links(url,count, Img_Str)

    info = pd.DataFrame(columns = ['company','mail','phone','url'])

    for link_i in links:
        info1 = get_info(link_i)
        if '-' not in info1[2] and len(info1[2])==9:
            info1[2]=info1[2][:2]+'-'+info1[2][2:5]+'-'+info1[2][5:]
        elif '-' not in info1[2] and len(info1[2])==10:
            info1[2] =info1[2][:2] + '-' + info1[2][2:6] + '-' + info1[2][6:]
        elif '-' not in info1[2] and len(info1[2])==11:
            info1[2] =info1[2][:3] + '-' + info1[2][3:7] + '-' + info1[2][7:]
        print(info1)
        info=info.append({'company':info1[0],'mail':info1[1],'phone':info1[2],'url':link_i},ignore_index=True)
    info.to_csv('./company_info_{}.csv'.format(dict1[number]), encoding='cp949')