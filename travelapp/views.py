from django.shortcuts import redirect, render
from travelapp import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from random import randint
import datetime
from django.db.utils import IntegrityError
from travelapp.models import Member
from travelapp.py.tra import railway
from travelapp.py.bookingcom import bookingCheap, bookingCP, bookingRich
from travelapp.py.thsr import THSR_SearchTicketes
# Create your views here.
def index(request):
    return render(request,'index.html',locals())

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('/checkout/')
                else:
                    message = "帳號尚未啟用！"
                    errornum = 1
            else:
                message="密碼錯誤！"
                errornum = 1
        except:
            message = "帳號不存在！"
            errornum = 1
    else:
        message = "請填入帳號密碼"
        errornum = 0 
    return render(request,'login.html',locals())

def logout(request):
    auth.logout(request)
    return redirect('/index/')

def register(request):
    users = User.objects.all()
    userslist = [u.username for u in users]
    creditmonthlist=[m for m in range(1,13)] # 給信用卡月份用
    credityearlist=[i for i in range(2022,2053)] # 給信用卡註冊用
    if request.method == "POST":
        try:
            # 把資料寫進 Member 資料表
            mName = request.POST['mName']
            mLast = request.POST['mLast']
            mFirst = request.POST['mFirst']
            mPersonid = request.POST['mPersonid']
            mPhone = request.POST['mPhone']
            mBirthday = '-'.join(request.POST['mBirthday'].split("/"))
            mSex = request.POST['mSex']
            mEmail = request.POST['mEmail']
            if User.objects.filter(email=mEmail).exists():
                raise Exception("此信箱已經註冊")
            mPassword = request.POST['mPassword']
            mCard = request.POST['mCard']
            mSafe = request.POST['mSafe']
            creditmonth = request.POST['creditmonth']
            credityear = request.POST['credityear']
            creditName = request.POST['creditName']
            postalCode = request.POST['postalCode']
            mAddress = request.POST['mAddress']
            mCity = request.POST['mCity']
            nickname = request.POST['nickname']
            unit = models.Member.objects.create(
                mName = mName, mLast = mLast, mFirst = mFirst,nickname=nickname,
                mPersonid = mPersonid, mPhone = mPhone, mBirthday = mBirthday,
                mSex = mSex, mEmail = mEmail, mPassword = mPassword, mSafe = mSafe,
                mCard = mCard, creditmonth = creditmonth, credityear = credityear,
                creditName = creditName, postalCode = postalCode, mAddress=mAddress, mCity = mCity
            )
            unit.save()
            # 把資料寫進 User 資料表
            user = User.objects.create_user(username=nickname,email=mEmail,password=mPassword)
            user.first_name = mFirst
            user.last_name = mLast
            user.is_staff = False
            user.save()
            return redirect('/login/')
        except IntegrityError:
            message = "使用者暱稱已有人使用，請重新輸入!"
        except Exception as e:
            messages = str(e)
            print(messages)
    return render(request,'register.html',locals())

def checkout(request):
    creditmonthlist=[m for m in range(1,13)] # 給信用卡月份用
    credityearlist=[i for i in range(2022,2053)] # 給信用卡註冊用
    traincities = ["基隆市","新北市","臺北市","桃園市","新竹縣","新竹市","苗栗縣","臺中市","彰化縣","雲林縣","嘉義縣","嘉義市",
            "嘉義市","臺南市","高雄市","屏東縣","臺東縣","花蓮縣","宜蘭縣"]
    plans = [
        "1) 小資輕旅:台鐵單程票乙張+可接受青旅★價格最低★",
        "2) 高CP首選:台鐵單程票乙張+3星級飯店以上★性價比最高★",
        "3) 豪華極享:高鐵單程票乙張+5星級飯店★最高品質★",
        "4) 台鐵車票乙張，不包含住宿"
    ]
    stayDays=[
        "2 天 1 夜",
        "3 天 2 夜",
        "4 天 3 夜",
        "5 天 4 夜",
    ]
    distanceFromHotel = [
        "1 公里內",
        "3 公里內",
        "5 公里內",
    ]
    specialNeeds = { 
    "handicap":"無障礙空間",
    "wifi":"免費無線網路",
    "nosmoke":"禁菸客房",
    "breakfast":"必須含早餐",
    }
    paymentMethods = [
        "網路付款(VISA、MasterCard、JCB)",
        "車站窗口/超商/郵局 付款",
    ]
    random1 = str(randint(0,99)).zfill(2)
    random2 = str(randint(0,9999)).zfill(4)
    random3 = str(randint(0,9999999)).zfill(7)
    random4 = str(randint(0,9999)).zfill(4)
    barcode = str(random3)+str(random4)+str(random1)
    memberuser = Member.objects.get(mEmail=request.user.email)
    if request.method=="POST":
        errornum = 0
        message = ''
        # try:
        chosenplan = request.POST["chosenplan"]
        adults = request.POST['adults']
        children = request.POST['children']
        seniors = request.POST['seniors']
        totalpeople = int(adults) + int(children) + int(seniors)
        trainStartCity = request.POST['trainStartCity']
        trainStartStation = request.POST['trainStartStation']
        trainStartTime = request.POST['trainStartTime']
        trainEndCity = request.POST['trainEndCity']
        trainEndStation = request.POST['trainEndStation']
        trainPayMethod = request.POST['trainPayMethod']
        ''' 以下處理火車出發時刻 '''
        startdate = "".join(str(trainStartTime).split("T")[0].split("-"))

        starttime = [int(i) for i in str(trainStartTime).split("T")[1].split(":")]
        if (starttime[1]==0 or starttime[1]==30):
            starttime[0] == str(starttime[0])
            starttime[1] == str(starttime[1])
        elif (starttime[1] > 0 and starttime[1] < 30):
            starttime[1] = "30"
            starttime[0] = str(starttime[0]).zfill(2)
        elif (starttime[1] > 30 and starttime[1] < 60):
            starttime[1] = "00"
            starttime[0] = str(starttime[0]+1).zfill(2)
        starttime = ":".join(starttime)
        ''' 以上處理火車出發時刻 '''
        if trainPayMethod == "0":
            mCard = request.POST['mCard']
            mSafe = request.POST['mSafe']
            creditName = request.POST['creditName']
            creditmonth = request.POST['creditmonth']
            credityear= request.POST['credityear']
            mCard = "".join(mCard.split("-"))
            creditmonth = creditmonth.zfill(2)
        elif trainPayMethod == "1":
            pass
        if chosenplan in ["1","2","3"]:
            ''' 以下資訊只會飯店用到 '''
            hotelNeeds = []
            handicap = request.POST.get("handicap",False)
            wifi = request.POST.get("wifi",False)
            nosmoke = request.POST.get("nosmoke",False)
            breakfast = request.POST.get("breakfast",False)
            if handicap:
                hotelNeeds.append(specialNeeds["handicap"])
            if wifi:
                hotelNeeds.append(specialNeeds["wifi"])
            if nosmoke:
                hotelNeeds.append(specialNeeds["nosmoke"])
            if breakfast:
                hotelNeeds.append("含早餐")
            staydays = request.POST['staydays']
            date_1 = datetime.datetime.strptime(startdate, "%Y%m%d").date()
            end_date = date_1 + datetime.timedelta(days=int(staydays))
            distanceFromStation = request.POST['distanceFromStation']
            mCardSeparate = request.POST['mCard'].split("-")
            ''' 以上資訊只會飯店用到 '''
            if chosenplan == "1":
                print("進入小資")
#以下台鐵訂票（小資方案)
                tra = railway.trainfilter(generation = memberuser.mPersonid,
                                        startStation = trainStartStation,
                                        endStation = trainEndStation,
                                        rideDate = startdate,
                                        startTime = starttime,
                                        adult = adults,
                                        child = children,
                                        old = seniors,
                                        mCard = mCard,mSafe = mSafe,
                                        emonth = creditmonth,eyear = credityear,
                                        paymentMethod=trainPayMethod)
                now = datetime.datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                journey = " ".join(tra['journey'])
                journey_info = tra['journey_info'][0].split(" ")
                trainname = journey_info[0]
                trainnumber = journey_info[1]
                ticketid = tra['ticketid'][0]
                seats = tra['seats']
                for index,seat in enumerate(seats):
                    car = seat[0]
                    num = seat[seat.find("車")+1:-1]
                    dict1 = {"car":car,"num":num}
                    seats[index] = dict1
                fullprice = 0
                childprice = 0
                seniorprice = 0
                tip = 15
                for t,p in zip(tra["type"],tra["price"]):
                    if t == "全票":
                        fullprice += int(p.split(" ")[0])
                    elif t == "孩童":
                        childprice += int(p.split(" ")[0])
                    elif t == "敬老":
                        seniorprice += int(p.split(" ")[0])
                totalprice = int(tra["total"][0])
                totalplustip = totalprice + tip
                adults = int(adults)
                children = int(children)
                seniors = int(seniors)
                mCardLast4 = mCard[-4:]
                # 以上台鐵訂票（小資方案）
                ''' 以下booking訂票（小資方案）'''
                book = bookingCheap.booking_plan1(trainEndCity,str(date_1),str(end_date),str(totalpeople),hotelNeeds,
                                                    memberuser.mLast,memberuser.mLast,memberuser.mEmail,
                                                    memberuser.mCity,memberuser.mAddress,memberuser.mPhone,
                                                    mCardSeparate[0],mCardSeparate[1],mCardSeparate[2],mCardSeparate[3],
                                                    creditmonth,credityear,memberuser.mSafe)
                hotelNameType = book["hotel_name"].split("\n")
                hotelname = hotelNameType[2]
                hoteltype = hotelNameType[1]

                checkindate = book['check_in_date']
                checkoutdate = book['check_out_date']
                checkintime = book['check_in_time']
                checkouttime = book['check_out_time']

                roomtype = book['room_name'].replace("\\n","")
                howManyRooms = book["howManyRooms"]
                peoplePerRoom = book["peoplePerRoom"]
                people = book["people"]
                price = book["roomCostPerNight"].replace('\nTWD\xa0','')
                price = price.replace("\n",'')
                ''' 以下booking訂票（小資方案）'''
                return render(request,'receipt.html',locals())
            elif chosenplan == "2":
                print("進入高cp")
# 以下台鐵訂票（高cp方案)
                tra = railway.trainfilter(generation = memberuser.mPersonid,
                                        startStation = trainStartStation,
                                        endStation = trainEndStation,
                                        rideDate = startdate,
                                        startTime = starttime,
                                        adult = adults,
                                        child = children,
                                        old = seniors,
                                        mCard = mCard,mSafe = mSafe,
                                        emonth = creditmonth,eyear = credityear,
                                        paymentMethod=trainPayMethod)
                now = datetime.datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                journey = " ".join(tra['journey'])
                journey_info = tra['journey_info'][0].split(" ")
                trainname = journey_info[0]
                trainnumber = journey_info[1]
                ticketid = tra['ticketid'][0]
                seats = tra['seats']
                for index,seat in enumerate(seats):
                    car = seat[0]
                    num = seat[seat.find("車")+1:-1]
                    dict1 = {"car":car,"num":num}
                    seats[index] = dict1
                fullprice = 0
                childprice = 0
                seniorprice = 0
                tip = 15
                for t,p in zip(tra["type"],tra["price"]):
                    if t == "全票":
                        fullprice += int(p.split(" ")[0])
                    elif t == "孩童":
                        childprice += int(p.split(" ")[0])
                    elif t == "敬老":
                        seniorprice += int(p.split(" ")[0])
                totalprice = int(tra["total"][0])
                totalplustip = totalprice + tip
                adults = int(adults)
                children = int(children)
                seniors = int(seniors)
                mCardLast4 = mCard[-4:]
                ''' 以上台鐵訂票（高cp方案）'''
                ''' 以下booking訂票（高cp方案）'''
                book = bookingCP.booking_plan2(trainEndCity,str(date_1),str(end_date),str(totalpeople),hotelNeeds,
                                                    memberuser.mLast,memberuser.mLast,memberuser.mEmail,
                                                    memberuser.mCity,memberuser.mAddress,memberuser.mPhone,
                                                    mCardSeparate[0],mCardSeparate[1],mCardSeparate[2],mCardSeparate[3],
                                                    creditmonth,credityear,memberuser.mSafe)
                hotelNameType = book["hotel_name"].split("\n")
                hotelname = hotelNameType[2]
                hoteltype = hotelNameType[1]

                checkindate = book['check_in_date']
                checkoutdate = book['check_out_date']
                checkintime = book['check_in_time']
                checkouttime = book['check_out_time']

                roomtype = book['room_name'].replace("\\n","")
                howManyRooms = book["howManyRooms"]
                peoplePerRoom = book["peoplePerRoom"]
                people = book["people"]
                price = book["roomCostPerNight"].replace('\nTWD\xa0','')
                price = price.replace("\n",'')
                ''' 以上booking訂票（高cp方案）'''
                return render(request,'receipt.html',locals())
            elif chosenplan == "3":
                print("進入豪華")
# 以下高鐵訂票        
                childrenPlusSeniors = int(children) + int(seniors)
                thsrdate = request.POST['trainStartTime'].split("T")[0].replace("-",".")
                print(trainStartStation,trainEndStation,
                                                thsrdate,starttime,int(adults),childrenPlusSeniors)
                thsr = THSR_SearchTicketes.main(trainStartStation,trainEndStation,
                                                thsrdate,starttime,int(adults),childrenPlusSeniors)
                thsrname = request.POST['trainStartTime'].split("T")[0] + " " + starttime+" " + trainStartStation+" 到 "+thsr["ArrivalTime"]+" "+ trainEndStation
                trainnumber = thsr["TrainNumber"]
                childrenPlusSeniorsprice = (int(seniors)+int(children)) * int(thsr["PreferentialTicketPrice"])
                adultPrice = int(adults) * int(thsr["AudltTicketPrice"])
                adults = int(adults)
                children = int(children)
                seniors = int(seniors)
                tip = 15
                totalplustip = adultPrice + childrenPlusSeniorsprice + tip
                now = datetime.datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                ''' 以上高鐵訂票'''
                ''' 以下booking訂票（豪華方案）'''
                book = bookingRich.booking_plan3(trainEndCity,str(date_1),str(end_date),str(totalpeople),hotelNeeds,
                                                    memberuser.mLast,memberuser.mLast,memberuser.mEmail,
                                                    memberuser.mCity,memberuser.mAddress,memberuser.mPhone,
                                                    mCardSeparate[0],mCardSeparate[1],mCardSeparate[2],mCardSeparate[3],
                                                    creditmonth,credityear,memberuser.mSafe)
                hotelNameType = book["hotel_name"].split("\n")
                hotelname = hotelNameType[2]
                hoteltype = hotelNameType[1]

                checkindate = book['check_in_date']
                checkoutdate = book['check_out_date']
                checkintime = book['check_in_time']
                checkouttime = book['check_out_time']

                roomtype = book['room_name'].replace("\\n","")
                howManyRooms = book["howManyRooms"]
                peoplePerRoom = book["peoplePerRoom"]
                people = book["people"]
                price = book["roomCostPerNight"].replace('\nTWD\xa0','')
                price = price.replace("\n",'')
                ''' 以上booking訂票（豪華方案）'''
                return render(request,'receipt.html',locals())
        elif chosenplan == "4":
            print("進入只訂票")
# 以下台鐵訂票（只訂票）
            tra = railway.trainfilter(generation = memberuser.mPersonid,
                                startStation = trainStartStation,
                                endStation = trainEndStation,
                                rideDate = startdate,
                                startTime = starttime,
                                adult = adults,
                                child = children,
                                old = seniors,
                                mCard = mCard,mSafe = mSafe,
                                emonth = creditmonth,eyear = credityear,
                                paymentMethod=trainPayMethod)
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            journey = " ".join(tra['journey'])
            journey_info = tra['journey_info'][0].split(" ")
            trainname = journey_info[0]
            trainnumber = journey_info[1]
            ticketid = tra['ticketid'][0]
            seats = tra['seats']
            for index,seat in enumerate(seats):
                car = seat[0]
                num = seat[seat.find("車")+1:-1]
                dict1 = {"car":car,"num":num}
                seats[index] = dict1
            fullprice = 0
            childprice = 0
            seniorprice = 0
            tip = 15
            for t,p in zip(tra["type"],tra["price"]):
                if t == "全票":
                    fullprice += int(p.split(" ")[0])
                elif t == "孩童":
                    childprice += int(p.split(" ")[0])
                elif t == "敬老":
                    seniorprice += int(p.split(" ")[0])
            totalprice = int(tra["total"][0])
            totalplustip = totalprice + tip
            adults = int(adults)
            children = int(children)
            seniors = int(seniors)
            mCardLast4 = mCard[-4:]
            ''' 以上台鐵訂票（只訂票）'''
            return render(request,'receipt.html',locals())
        # except Exception as e:
        #     errornum = 1
        #     print(e)
        #     message = e
        
    return render(request,'checkout.html',locals())
