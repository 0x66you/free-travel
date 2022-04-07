from django.db import models
from datetime import date
from random import random
# Create your models here.
class Member(models.Model):
    mName = models.CharField(max_length=20,null=False) # 中文姓名
    mLast = models.CharField(max_length=20,null=False) # 英文姓氏
    mFirst = models.CharField(max_length=20,null=False) # 英文名字
    mPersonid = models.CharField(max_length=20,null=False) # 身分證字號
    mPhone = models.CharField(max_length=50,null=False) # 手機
    mCity = models.CharField(max_length=20,null=False,default='') # 城市
    mAddress = models.CharField(max_length=50,null=False,default='') # 地址
    postalCode = models.CharField(max_length=10,default='',blank=True) # 郵遞區號
    mBirthday = models.DateField(null=False,default=date.today().strftime("%Y/%m/%d")) # 生日
    mSex = models.CharField(max_length=2,default='M',null=False) # 性別
    mEmail = models.EmailField(max_length=100,null=False) # 信箱
    mPassword = models.CharField(max_length=50,null=False) # 密碼
    mCard = models.CharField(max_length=20,null=False) # 信用卡卡號
    mSafe = models.CharField(max_length=5,null=False) # 安全碼
    creditmonth = models.IntegerField(null=False) # 卡片有效日期(月份)
    credityear = models.IntegerField(null=False) # 卡片有效日期(年份)
    creditName = models.CharField(max_length=20,null=False) # 持卡人姓名
    nickname = models.CharField(max_length=20,null=False,default=random())
    def __str__(self):
        return self.mName
    