from selenium import webdriver #載入 webdriver 模組
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time
from lxml import etree
import math


def booking_plan1(place,cidate,codate,human,choose,lastname,firstname,email,city,address,phonenum,cardnumber1,cardnumber2,cardnumber3,cardnumber4,ccmonth,ccyear,cvc):
    print("enter booking")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36 ')
    browser=webdriver.Chrome(chrome_options=options) 
    browser.get("https://www.booking.com/index.zh-tw.html?aid=376396;label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255:pl:ta:p1:p22,563,000:ac:ap:neg:fi:tikwd-65526620:lp1012810:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms;ws=&gclid=Cj0KCQjw0PWRBhDKARIsAPKHFGg_wMVulQXzASfYYQj__lleQ8K8i98whx2SgMbFKejYrilc3dRYI7oaAhpvEALw_wcB")
    browser.find_element_by_id("ss").send_keys(place)
    date  = browser.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[1]/div[2]/div/div/div/div/span').click()
    date  = browser.find_elements_by_class_name('bui-calendar__date')
    for d in date:
        val =d.get_attribute('data-date')
        if val == cidate:
            d.click()
            break
    date2  = browser.find_elements_by_class_name('bui-calendar__date')
    for d2 in date2:
        val =d2.get_attribute('data-date')
        if val == codate:
            d2.click()
            break
    time.sleep(3)
    browser.find_element_by_id('xp__guests__toggle').click()
    print("斷點一")
    people = browser.find_element_by_class_name('bui-stepper__add-button')
    people2 = browser.find_element_by_class_name('bui-stepper__subtract-button') 
    if human == '2':
        pass
    elif human == '3':
        people.click()
    elif human == '4':
        people.click()
        people.click()
    elif human == '5':
        people.click()
        people.click()
        people.click()
    elif human == '6':
        people.click()
        people.click()
        people.click()
        people.click()
    else:
        people2.click()
    browser.find_element_by_class_name("sb-searchbox__button").click()
    try:
        browser.find_element_by_xpath('//*[@id="ajaxsrwrap"]/div[1]/div/div/div[2]/ul/li[4]').click()
    except:
        browser.find_element_by_xpath('//*[@id="right"]/div[1]/div/div/div/span/button').click() 
        browser.find_elements_by_class_name('a1b3f50dcd.b2fe1a41c3.e6f05e293e.db7f07f643.d19ba76520')[3].click()
    time.sleep(5)
    browser.find_elements_by_class_name('bbdb949247')[0].click()
    time.sleep(3)
    extraneed = browser.find_elements_by_class_name('db29ecfbe2.cb475f8063')
    for e in extraneed:
        var= e.text
        if var in ["飯店","汽車旅館","民宿"]:
            e.click()
            break
    time.sleep(6)
    specialneed = browser.find_elements_by_class_name('db29ecfbe2.cb475f8063')
    for s in specialneed:
        var= s.text
        if var in choose:
            s.click()
            break
    print("斷點二")
    time.sleep(5)   
    browser.find_elements_by_class_name('e57ffa4eb5')[1].click()
    time.sleep(3)
    browser.switch_to.window(browser.window_handles[1])
    soup = BeautifulSoup(browser.page_source,'lxml')
    hotelname = soup.find_all('h2',class_='hp__hotel-name')[0].text
    Select(browser.find_elements_by_class_name('hprt-nos-select')[0]).select_by_value("1")
    roomname = soup.find('a',class_='hprt-roomtype-link').text
    count = 0
    print("斷點三")
    while True:
        x = len(soup.find_all('select',class_='hprt-nos-select')[count].find_all('option'))-1
        peoplePerRoom = len(soup.find_all('span',class_='c-occupancy-icons__adults')[count+1].find_all('i'))
        rooms= math.ceil(int(human)/ peoplePerRoom)
        if rooms > x :
            count+=1
            continue
        else:
            break
    roomCostPerNight = soup.find('span',class_='prco-valign-middle-helper').text
    time.sleep(5)
    try:
        browser.find_element_by_class_name('hprt-reservation-cta').click()
    
    except:
        browser.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[1]/div[1]/div/div[6]/div[2]/div[4]/div[3]/div/form/div[12]/div[2]/div[4]/div[6]').click()
    browser.switch_to.window(browser.window_handles[-1]) 
    time.sleep(13)
    checkInTime = browser.find_elements_by_class_name('bui-date__subtitle')[0].text
    checkOutTime =browser.find_elements_by_class_name('bui-date__subtitle')[1].text 
    browser.find_element_by_xpath('//*[@id="retain-leaving-users__modal"]/div/div/footer/div/div[1]/button').click()
    time.sleep(2)
    try:
        browser.find_element_by_id('lastname').send_keys(lastname)  
    except:
         browser.find_element_by_xpath('//*[@id="lastname"]').send_keys(lastname) 
        
    browser.find_element_by_name('firstname').send_keys(firstname) 
    browser.find_element_by_name('email').send_keys(email) 
    time.sleep(2)
    browser.find_element_by_id('email_confirm').send_keys(email) 
    try:
        browser.find_element_by_xpath('//*[@id="bookForm"]/div[3]/div/div[2]/button').click() 
    except:
        browser.find_element_by_name('book').click() 
    
    browser.switch_to.window(browser.window_handles[-1]) 
    time.sleep(12)
    browser.find_element_by_xpath('//*[@id="retain-leaving-users__modal"]/div/div/footer/div/div[1]/button').click()
    try:
        browser.find_element_by_id('city').send_keys(city)
    except:
        pass
    try:
        browser.find_element_by_name('address1').send_keys(address)
    except:
        pass
    time.sleep(6)
    browser.find_element_by_name('phone').send_keys(phonenum)
    print("斷點四")
    try:
        Select(browser.find_element_by_id('cc_type')).select_by_value("Visa")
        browser.find_element_by_name('cc_number').send_keys(cardnumber1)
        time.sleep(3)
        browser.find_element_by_name('cc_number').send_keys(cardnumber2)
        time.sleep(3)
        browser.find_element_by_name('cc_number').send_keys(cardnumber3)
        time.sleep(3)
        browser.find_element_by_name('cc_number').send_keys(cardnumber4)
        time.sleep(3)
        Select(browser.find_element_by_name('cc_month')).select_by_value(ccmonth)
        Select(browser.find_element_by_name('cc_year')).select_by_value(ccyear)
        browser.find_element_by_name('cc_cvc').send_keys(cvc)
    except:
        pass
    
    dict1 ={
        "hotel_name": hotelname,
        "check_in_date": cidate,
        "check_out_date":codate,
        "check_in_time" :checkInTime,
        "check_out_time":checkOutTime,
        "people": human ,
        "howManyRooms": rooms,
        "room_name": roomname,
        "roomCostPerNight":roomCostPerNight,
        "peoplePerRoom": peoplePerRoom
        } 
    print("exit booking")
    return dict1