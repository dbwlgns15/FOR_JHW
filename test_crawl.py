import pandas as pd
import time
import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver

data = []

id_pw = open('id_pw.txt')
bm_id = str(id_pw.readline()).strip()
bm_pw = str(id_pw.readline()).strip()
cp_id = str(id_pw.readline()).strip()
cp_pw = str(id_pw.readline()).strip()

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
time.sleep(5)

try: # 광고가 뜨면 하고 아니면 패스
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[3]/div/div/div/div[3]/div[2]/button[1]').click() # 광고 프로모션 동의안함
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[3]/div/div/div/div[3]/button[2]').click() # 확인
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[3]/div/div/div/div[2]/button').click() # 확인
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-onboarding-body"]/div[2]/div/div/div/button').click() # 일주일간 보지않기
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/header/a/img').click() # 메뉴
    time.sleep(0.5)
    driver.find_element("xpath", '//*[@id="merchant-management"]/div/nav/div[2]/ul/li[3]/a').click() # 매출관리
    time.sleep(0.5)
except:
    pass

driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[1]').click() # 기간선택 버튼 클릭
time.sleep(0.2)
driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[6]/div/label').click() # 1년 버튼 클릭
time.sleep(0.2)
driver.find_element("xpath", '//*[@id="merchant-management"]/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/button').click() # 조회 버튼 클릭
time.sleep(2)

html = driver.page_source
bs = BeautifulSoup(html, 'html.parser')
table = bs.findAll('li',{'class':'col-12'})

print(table)