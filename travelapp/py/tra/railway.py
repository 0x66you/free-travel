# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from travelapp.py.tra.railway1 import railway1
from selenium.webdriver.common.by import By
def gather(traintype,browser):
    u1 = browser.find_elements_by_class_name("trip-column")
    time = []
    abc = []
    for x in u1:    
        if x.find_elements_by_partial_link_text(traintype):
            time.append(x)
    for i,t in enumerate(time):
        y = t.find_elements(by=By.TAG_NAME,value='td')[2]
        time[i] = y.text 
        
    plist = browser.find_elements(by=By.PARTIAL_LINK_TEXT,value=traintype)
    for i,p in enumerate(plist):
        plist[i] = p.text.split(" ")[-1]
    for t,p in zip(time,plist):
        j = p + ":" + t
        abc.append(j)
    return abc
def trainsort(tlist):    
    sort_number = []
    for h in range(0,23): 
        for m in range(0,59): 
            for x in tlist:
                if h == int(x.split(':')[1]) and m == int(x.split(':')[2]):
                    sort_number.append(x.split(':')[0])
    return sort_number
def trainfilter(generation,startStation,endStation,rideDate,startTime,adult,child,old,mCard,mSafe,emonth,eyear,paymentMethod):
    print("enter trainfilter")
    number_of_people = int(adult) + int(child) + int(old)
    startTime = "11:00"
    endTime1 = int(startTime.split(":")[0]) + 3
    endTime2 = startTime.split(":")[1]
    endTime = str(endTime1)+":"+endTime2
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser=webdriver.Chrome(chrome_options=options) 
    # browser = webdriver.Chrome()
    browser.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")
    
    browser.find_element_by_id("startStation").send_keys(startStation)
    browser.find_element_by_id("endStation").send_keys(endStation)
    browser.find_element_by_id("rideDate").clear()
    browser.find_element_by_id("rideDate").send_keys(rideDate)
    s1 = Select(browser.find_element_by_id("startTime"))
    s1.select_by_value(startTime)
    s2 = Select(browser.find_element_by_id("endTime"))
    s2.select_by_value(endTime)
    browser.find_element_by_name("query").click()
    taroko = gather('太魯閣',browser)
    gchin = gather('自強',browser)
    puyuma = gather('普悠瑪',browser)
    number = taroko + gchin + puyuma
    browser.quit()
    x = railway1(trainsort(number),generation,startStation,endStation,rideDate,number_of_people,adult,child,old,mCard,mSafe,emonth,eyear,paymentMethod)
    print("exit trainfilter")
    return x