import pandas as pd
import time
import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

data = []

id_pw = open('id_pw.txt')
bm_id = str(id_pw.readline()).strip()
bm_pw = str(id_pw.readline()).strip()
cp_id = str(id_pw.readline()).strip()
cp_pw = str(id_pw.readline()).strip()

s = Service('./TEMP/chromedriver"') # Service 객체 생성
driver = webdriver.Chrome(service=s) # 웹 드라이버 생성 및 Service 객체 전달
################# 배단의민족 ################################################
############################################################################

df_temp =  pd.read_csv('./TEMP/order_data.csv',encoding='utf-8',low_memory=False) # 최근 날짜 체크
df_temp = df_temp[df_temp['플랫폼'] == '배달의민족'].reset_index(drop=True)
check_date = df_temp.loc[0]['주문날짜']

baemin_url = 'https://ceo.baemin.com/self-service/orders/history'
driver.get(baemin_url)  # 배달의민족 사장님 사이트 접속
time.sleep(1)
driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div/form/div[1]/span/input').send_keys(bm_id)  # ID입력
driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div/form/div[2]/span/input').send_keys(bm_pw)  # PW입력
driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div/form/button').click()  # 로그인 버튼 클릭
time.sleep(4)

menu_list = ['고소한 삼겹', '고단백 삼겹', '황금비율 삼겹', '세트 (250g)', '고기만 (250g)', '고기만 (500g)', '100g', '200g',
              '쌈장', '와사비', '말돈소금', '명이나물', '쌈무', '김치', '된장찌개', '편마늘', '고추', '공기밥', '계란찜',
              '사이다 500', '코카콜라 355', '코카콜라 500', '제로콜라 355', '제로콜라 500']
check = 0
while True:
    try:
        html = driver.page_source
        bs = BeautifulSoup(html, 'html.parser')
        table = bs.findAll('table', {'class': 'bsds-table DesktopVersion-module__DcMM css-18du3ut'})[0].findAll('tbody')[0].findAll('tr')
        for i in range(20):

            if i % 2 == 0: # 주문번호, 기타, 주문날짜, 주문시간, 주문요일, 주문금액
                order_num = str(table[i].findAll('td')[1].text)[4:]
                order_gita = str(table[i].findAll('td')[3].text)
                
                if order_gita == '배민1 한집배달':
                    order_gita = '배민1'
                raw_date = str(table[i].findAll('td')[2].text).split()
                order_date = f'{raw_date[0][:-1]}-{raw_date[1][:-1]}-{raw_date[2][:-1]}'
                order_time = int(raw_date[-1].split(':')[0])
                order_marketing = 0
                if raw_date[-2] == '오후': # 오후면 시간을 24시 기준으로 맞추기 위해 12 더하기
                    order_time += 12
                    if order_time == 24:
                        order_time -= 12
                elif order_time == 12: # 오전 12시는 24시로 변경
                    order_time = 24
                order_week = raw_date[3][1:-1]
                order_price = str(table[i].findAll('td')[8].text).replace(',', '').replace('원', '')
                
                if order_date == check_date: # 날짜 체크
                    check = 1
                    
            if i % 2 == 1: # 상세 메뉴
                detail = table[i].findAll('div', {'class': 'DetailInfo-module__j9yH'})[0].findAll('div')
                menu_cnt = {} # 메뉴 카운트 리셋
                for menu in menu_list:
                    menu_cnt[menu] = 0
                    
                for j in detail:
                    detail_line = j.text
                    if '사장님부담 쿠폰할인' in detail_line: # 배민 쿠폰 금액 체크
                        try:
                            order_marketing += int(detail_line.split('원')[0].split('사장님부담 쿠폰할인')[-1].replace(',',''))
                        except:
                            order_marketing += int(detail_line.split('사장님부담 쿠폰할인')[-1].split('원')[0].replace(',',''))
                        break

                    if '┗' not in detail_line: # 메뉴 카운트                      
                        try:
                            cnt = int(detail_line.split('개')[0][-1])
                            for menu in menu_list:
                                if menu in detail_line:
                                    menu_cnt[menu] += cnt
                        except:
                            pass
                    else: # 옵션 카운트          
                        for menu in menu_list:
                            if menu in detail_line:
                                menu_cnt[menu] += cnt
                
                data.append([order_num, '배달의민족', order_gita, order_date, order_time, order_week, order_price, order_marketing, '', '']+list(menu_cnt.values()))

        if check == 1 and order_date != check_date: # 최신 날짜까지만 크롤링 
            break
        
        driver.find_element("xpath", '//*[@id="root"]/div/div[3]/div[2]/div[1]/div/nav/ul/li[13]/div[1]/button').click() # 다음페이지 버튼 클릭

        time.sleep(1)
   
    except:
        break  # 다음페이지 버튼이 눌리지 않으면 종료
driver.quit()

for i in range(len(df_temp)):
    data.append(df_temp.loc[i].to_list())

################# 쿠팡이츠 ##################################################
############################################################################

df_temp =  pd.read_csv('./TEMP/order_data.csv',encoding='utf-8') # 최근 날짜 체크
df_temp = df_temp[df_temp['플랫폼'] == '쿠팡이츠'].reset_index(drop=True)
check_date = df_temp.loc[0]['주문날짜']

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") # 쿠팡에서 차단을 막기위해 자동조작되고 있음을 숨기기
coupang_url = 'https://store.coupangeats.com/merchant/management/orders/490509'
driver = webdriver.Chrome("./TEMP/chromedriver",options=options)

driver.get(coupang_url) # 쿠팡이츠 사장님 사이트 접속
time.sleep(3)

driver.find_element("xpath", '//*[@id="loginId"]').send_keys(cp_id) # ID입력
driver.find_element("xpath", '//*[@id="password"]').send_keys(cp_pw) # PW입력
driver.find_element("xpath", '//*[@id="merchant-login"]/div/div[2]/div/div/div/form/button').click() # 로그인 버튼 클릭
time.sleep(6)

try: # 광고가 뜨면 하고 아니면 패스
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[4]/div/div/div/button').click() # x
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[3]/div/div/div/button').click() # x
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[2]/div/div/div/button').click() # x
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/header/a/img').click() # 메뉴
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-management"]/div/nav/div[2]/ul/li[3]/a').click() # 매출관리
    time.sleep(0.5)
except:
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[2]/div/div/div/button').click() # 신고 광고 x
    time.sleep(0.5)
    
driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[1]').click() # 기간선택 버튼 클릭
time.sleep(0.2)
driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[6]/div/label').click() # 1년 버튼 클릭
time.sleep(0.2)
driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/button').click() # 조회 버튼 클릭
time.sleep(2)

menu_list = ['고소한 삼겹', '고단백 삼겹', '황금비율 삼겹', '메카삼겹 세트', '메카삼겹 고기만 (삼겹살250g)', '메카삼겹 고기만(500g)', '100g 추가', '200g 추가',
              '쌈장', '와사비', '말돈소금', '명이나물', '쌈무', '김치', '된장찌개', '편마늘', '고추', '공기밥', '계란찜',
              '사이다 500', '코카콜라 355', '코카콜라 500', '제로콜라 355', '제로콜라 500']
check = 0
while True:
    try:
        html = driver.page_source
        bs = BeautifulSoup(html, 'html.parser')
        table = bs.findAll('li',{'class':'col-12'})

        for i in table:
            order_num = i.findAll('div',{'class':'col-4 col-md-3'})[0].text[:6]
            order_date = i.findAll('div',{'class':'order-date col-3 d-none d-md-block'})[0].text.split()[0].replace('.','-')
            order_time = int(i.findAll('div',{'class':'order-date col-3 d-none d-md-block'})[0].text.split()[1].split(':')[0])
            order_price = i.findAll('div',{'class':'order-price col-4 col-md-3 text-right'})[0].text
            order_marketing = 0
            order_week = ['월','화','수','목','금','토','일'][datetime.date(int(order_date.split('-')[0]),int(order_date.split('-')[1]),int(order_date.split('-')[2])).weekday()]
            
            if '취소' in order_price: # 취소 주문 제외
                continue
            else:
                order_price = order_price.split('원')[0].replace(',','')
            
            if order_date == check_date: # 날짜 체크
                check = 1

            menu_cnt = {} # 메뉴 카운트 리셋
            for menu in menu_list:
                menu_cnt[menu] = 0
            
            detail = i.findAll('ul',{'order-items'})[0].text.split('원')[:-1]
            for detail_line in detail:
                cnt = int(re.findall('([0-9])개',detail_line)[0])
                for menu in menu_list:
                    if menu in detail_line:
                        menu_cnt[menu] += cnt
            
            money_detail = i.findAll('ul',{'order-price-summary'})[0].findAll('li')
            for d in money_detail:
                money_text = d.text
                if '광고비' in money_text or '쿠폰' in money_text:
                    if '-' in money_text:
                        order_marketing += int(money_text.split('-')[-1][:-1].replace(',',''))
                        
            data.append([order_num, '쿠팡이츠', '', order_date, order_time, order_week, order_price, order_marketing, '', '']+list(menu_cnt.values()))
        
        if check == 1 and order_date != check_date: # 최신 날짜까지만 크롤링
            break
        
        driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[5]/div/div/div/div/ul/li[8]/button').click() # 다음페이지 버튼 클릭
        time.sleep(2)
        
    except: # 다음페이지 없으면 종료
        break
driver.quit()

for i in range(len(df_temp)): # 쿠팡 주문 데이터 불러오기
    data.append(df_temp.loc[i].to_list())

################# 요기요 ###################################################
############################################################################

yogiyo_df = pd.read_csv('./TEMP/yogiyo_raw.csv',encoding='utf-8')
for i in range(len(yogiyo_df)):
    order_num = yogiyo_df.loc[i]['주문번호'].split()[1]
    order_date = yogiyo_df.loc[i]['거래일시'].split()[0]
    order_time = yogiyo_df.loc[i]['거래일시'].split()[1][:2]
    order_week = ['월','화','수','목','금','토','일'][datetime.date(int(order_date.split('-')[0]),int(order_date.split('-')[1]),int(order_date.split('-')[2])).weekday()]
    order_price = yogiyo_df.loc[i]['주문금액']
    order_marketing = yogiyo_df.loc[i]['사장님자체할인']
    try:
        order_gu = re.findall('[가-힣]{1,3}구', yogiyo_df.loc[i]['배달주소1'])[0]
        order_dong = re.findall('\((.+동)\)', yogiyo_df.loc[i]['배달주소1'])[0]
    except:
        order_gu = '요기요포장'
        order_dong = '요기요포장'
    data.append([order_num, '요기요', '', order_date, order_time, order_week, order_price, order_marketing, order_gu, order_dong])

df_temp = pd.read_csv('./TEMP/yogiyo_order.csv',encoding='utf-8') # 요기요 주문 데이터 불러오기
for i in range(len(df_temp)):
    data.append(df_temp.loc[i].to_list())
    
############################################################################
############################################################################

df = pd.DataFrame(data, columns=['주문번호', '플랫폼', '기타', '주문날짜', '주문시간', '주문요일', '주문금액', '매장부담금액', '지역(구)', '지역(동)',
                                 '지방', '단백', '황금', '세트250', '고기250', '고기500', '추가100', '추가200',
                                 '쌈장', '와사비', '말돈소금', '명이나물', '쌈무', '김치', '된장찌개', '편마늘', '고추', '공기밥', '계란찜', 
                                 '사이다500', '콜라355', '콜라500', '제로콜라355', '제로콜라500'])

df = df.drop_duplicates(subset=['주문번호'],keep='last') 
df = df.reset_index(drop=True)
df.to_csv('./order_data.csv', encoding='utf-8', index=False)
print(df)