
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from time import sleep
import ast
import re

delay = 3

def setStartStation(start_station,browser):
    #起站
    stations = {'南港':'NanGang',
               '台北':'TaiPei',
               '板橋':'BanQiao',
               '桃園':'TaoYuan',
               '新竹':'XinZhu',
               '苗栗':'MiaoLi',
               '台中':'TaiZhong',
               '彰化':'ZhangHua',
               '雲林':'YunLin',
               '嘉義':'JiaYi',
               '台南':'TaiNan',
               '左營':'ZuoYing'}
    
    start_station = stations.get(start_station)
    
    select = Select(browser.find_element_by_id('select_location01'))
    select.select_by_value(start_station)
    
def setArrivalStation(arrival_station,browser):
    #終站
    stations = {'南港':'NanGang',
               '台北':'TaiPei',
               '板橋':'BanQiao',
               '桃園':'TaoYuan',
               '新竹':'XinZhu',
               '苗栗':'MiaoLi',
               '台中':'TaiZhong',
               '彰化':'ZhangHua',
               '雲林':'YunLin',
               '嘉義':'JiaYi',
               '台南':'TaiNan',
               '左營':'ZuoYing'}
    
    arrival_station = stations.get(arrival_station)
    
    select = Select(browser.find_element_by_id('select_location02'))
    select.select_by_value(arrival_station)
    
def setTicketType(ticket_type,browser):
    ticket_types = {"單程":"tot-1",
                    "去回程":"tot-2"}
    
    ticket_type = ticket_types.get(ticket_type)
    
    select = Select(browser.find_element_by_id('typesofticket'))
    select.select_by_value(ticket_type)

def setStartDate(start_date,browser):
    browser.execute_script('document.getElementById("Departdate03").removeAttribute("onkeydown")')
    ActionChains(browser).click(browser.find_element_by_id("Departdate03")).perform()
    ActionChains(browser).release()
    browser.execute_script('document.getElementById("Departdate03").value=arguments[0];',start_date)
    
def setStartTime(start_time,browser):
    browser.execute_script('document.getElementById("outWardTime").removeAttribute("onkeydown")')
    ActionChains(browser).click(browser.find_element_by_id("outWardTime")).perform()
    ActionChains(browser).release()
    browser.execute_script('document.getElementById("outWardTime").value=arguments[0];',start_time)
    
def setReturnDate(return_date,browser):
    browser.execute_script('document.getElementById("Returndate03").removeAttribute("onkeydown")')
    ActionChains(browser).click(browser.find_element_by_id("Returndate03")).perform()
    ActionChains(browser).release()
    browser.execute_script('document.getElementById("Returndate03").value=arguments[0];',return_date)

def setReturnTime(return_time,browser):
    browser.execute_script('document.getElementById("returnTime").removeAttribute("onkeydown")')
    ActionChains(browser).click(browser.find_element_by_id("returnTime")).perform()
    ActionChains(browser).release()
    browser.execute_script('document.getElementById("returnTime").value=arguments[0];',return_time)

    
def getArrivalStation(browser):
    arrival_station = browser.find_element_by_xpath('//*[@id="ttab-01"]/div[1]/div[1]/div[3]')
    return arrival_station


def getArrivalTime(browser):
    arrival_time = browser.find_element_by_xpath('//*[@id="timeTableTrain_S"]/a[1]/div[3]/span')
    return arrival_time

def getTrainNumber(browser):
    train_number = browser.find_element_by_xpath('//*[@id="timeTableTrain_S"]/a[1]/div[4]')
    return train_number

def getDiscount(browser):
    discount = browser.find_element_by_xpath('//*[@id="timeTableTrain_S"]/a[1]/div[6]/p/span').text
    if not discount.replace(" ", ""):
        return 1
    else:
        discount = ast.literal_eval(discount)
        return discount

def getAudltTicketPrice(browser):
    audlt_ticket_price = browser.find_element_by_xpath('//*[@id="priceTable"]/tbody/tr[1]/td[1]')
    list_atp = re.findall(r"(\d+)", audlt_ticket_price.text)
    return list_atp[0]
    
    
def getPreferentialTicketPrice(browser):
    preferential_ticket_price = browser.find_element_by_xpath('//*[@id="priceTable"]/tbody/tr[1]/td[2]')
    list_ptp = re.findall(r"(\d+)", preferential_ticket_price.text)
    return list_ptp[0]

def one_trip(ss_, as_, tot_, sd_, st_, noat_, nopt_,browser):
    setStartStation(ss_,browser)
    setArrivalStation(as_,browser)
    setTicketType(tot_,browser)
    setStartDate(sd_,browser)
    setStartTime(st_,browser)
    

    browser.find_element_by_class_name("btn.btn-orange.btn-full.inlineM.mt-3").click() 
    sleep(5)
    gat_ = getArrivalTime(browser)
    gtn_ = getTrainNumber(browser)
    
    gatp_ = getAudltTicketPrice(browser)
    gptp_ = getPreferentialTicketPrice(browser)
    
    Data_tot1 = {
                 "ArrivalTime": gat_.text,
                 "TrainNumber": gtn_.text,
                 "AudltTicketPrice": str(gatp_),
                 "PreferentialTicketPrice": str(gptp_),}
    
    print("Data_tot1: ", Data_tot1) 
    return Data_tot1
def main(startstation, endstation, startdate, starttime, adults, special):
    print("enter thsr")
    url="https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c"
    browser=webdriver.Chrome() 
    browser.get(url)

    browser.find_element_by_class_name("swal2-confirm.swal2-styled").click() 

    sleep(delay)

    x = one_trip(startstation, endstation, '單程', startdate, starttime, adults, special,browser)

    

    sleep(delay)

    browser.quit()
    print("exit thsr")
    return x