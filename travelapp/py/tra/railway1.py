from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from travelapp.py.tra.solveRecaptcha import solveRecaptcha
import time
from selenium.webdriver.support.ui import Select

def railway1(number_ticket,generation,startStation,endStation,rideDate,number_of_people,adult,child,old,mCard,mSafe,emonth,eyear,paymentMethod):
    print("enter railway1")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser=webdriver.Chrome(chrome_options=options) 
    # browser = webdriver.Chrome()
    browser.get('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query')
    for i in number_ticket:
        
        
        browser.find_element_by_id("pid").send_keys(generation)
        browser.find_element_by_id("startStation").send_keys(startStation)
        browser.find_element_by_id("endStation").send_keys(endStation)
        browser.find_element_by_id("rideDate1").clear()
        browser.find_element_by_id("rideDate1").send_keys(rideDate)
        for x in range(int(number_of_people)-1):
            browser.find_element_by_xpath('//*[@id="queryForm"]/div[1]/div[2]/div[1]/div[2]/button[2]').click()
        
        browser.find_element_by_id("trainNoList1").send_keys(i)
        result = solveRecaptcha(
            "6LdHYnAcAAAAAI26IgbIFgC-gJr-zKcQqP1ineoz",
            "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
        )
        code = result["code"]
        # print(code)
        print("取得code")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID,'g-recaptcha-response'))
        )
        browser.execute_script(
            "document.getElementById('g-recaptcha-response').innerHTML = " + "'"+ code +"'")
        browser.find_element(By.XPATH, '//*[@id="queryForm"]/div[4]/input[2]').click()
        browser.implicitly_wait(20)
        time.sleep(1)
        try:
            for x in range(int(child)):
                Select(browser.find_element_by_name("orderMap['0'].ticketList[{}].ticketTypeCode".format(x))).select_by_value("2")

            for y in range(int(child),int(child)+int(old)):
                Select(browser.find_element_by_name("orderMap['0'].ticketList[{}].ticketTypeCode".format(y))).select_by_value("3")
            time.sleep(1)
            element = browser.find_element(By.XPATH, '//*[@id="order"]/div[3]/button')
            browser.execute_script("arguments[0].click();", element)
            break
        except Exception:
            pass
    print("取得班次結束for")
    browser.implicitly_wait(20)
    time.sleep(1)
    journey = []
    Itinerary_information = []
    votes = []
    amount = []
    booking_code = []
    seat = []
    ticket_type = []
    subtotal = []
    date = browser.find_element_by_class_name("date")
    journey.append(date.text)
    time1 = browser.find_element(By.XPATH, '//*[@id="content"]/div[3]/div/table/tbody/tr[2]/td[1]/ul/li[1]/span[2]')
    journey.append(time1.text)
    from_ = browser.find_element_by_class_name("from")
    journey.append(from_.text)
    icon = browser.find_element_by_class_name("icon.icon-to")
    journey.append(icon.text)
    time2 = browser.find_element(By.XPATH, '//*[@id="content"]/div[3]/div/table/tbody/tr[2]/td[1]/ul/li[2]/span[3]')
    journey.append(time2.text)
    to = browser.find_element_by_class_name("to")
    journey.append(to.text)
    tzechiang = browser.find_element_by_class_name("links.icon-fa.icon-train")
    Itinerary_information.append(tzechiang.text)
    table = browser.find_element(By.XPATH, '//*[@id="content"]/div[3]/div/table/tbody/tr[2]/td[3]')
    votes.append(table.text) 
    orderSum = browser.find_element_by_class_name("orderSum")
    amount.append(orderSum.text)
    font18 = browser.find_element_by_class_name("font18")
    booking_code.append(font18.text)
    seat1 = browser.find_elements_by_class_name("seat")
    for value1 in seat1:
            seat.append(value1.text)
    try:
        z1 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[2]/td[3]/div/div')
        ticket_type.append(z1.text)       
        z2 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[3]/td[3]/div/div')
        ticket_type.append(z2.text)       
        z3 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[4]/td[3]/div/div')
        ticket_type.append(z3.text)       
        z4 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[5]/td[3]/div/div')
        ticket_type.append(z4.text)       
        z5 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[6]/td[3]/div/div')
        ticket_type.append(z5.text)        
        z6 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[7]/td[3]/div/div')
        ticket_type.append(z6.text)            
        pass
    except Exception:
        pass
    try:
        s1 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[2]/td[5]')
        subtotal.append(s1.text)
        s2 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[3]/td[5]')
        subtotal.append(s2.text)
        s3 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[4]/td[5]')
        subtotal.append(s3.text)
        s4 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[5]/th[5]')
        subtotal.append(s4.text)
        s5 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[6]/th[5]')
        subtotal.append(s5.text)
        s6 = browser.find_element(By.XPATH, '//*[@id="order"]/div[1]/div[2]/table/tbody/tr[7]/th[5]')                      
        subtotal.append(s6.text)
        pass
    except Exception:
        pass 
    railwayTicket = {"journey":journey,
                      "journey_info":Itinerary_information,
                      "票數":votes,
                      "total":amount,
                      "ticketid":booking_code,
                      "seats":seat,
                      "type":ticket_type,
                      "price":subtotal
    }
    if paymentMethod == "1":
        Select(browser.find_element_by_id("paymentMethod")).select_by_value("ONSITE")
    elif paymentMethod == "0":
        Select(browser.find_element_by_id("paymentMethod")).select_by_value("ONLINE") 
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="order"]/div[3]/button[2]').click()
        browser.implicitly_wait(20)
        time.sleep(1)
        browser.find_element_by_id("pan_num").send_keys(mCard) 
        browser.find_element_by_id("cvc2").send_keys(mSafe)
        select_month = Select(browser.find_element_by_name("expire_month"))
        select_month.select_by_value(emonth)
        select_year = Select(browser.find_element_by_name("expire_year"))
        select_year.select_by_value(eyear)
    browser.quit()
    print("exit railway1")
    return railwayTicket