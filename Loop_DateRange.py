
import datetime
import calendar

today = datetime.datetime(2022,12,1, 1,1,1,1) #Start Date 
month_end = datetime.datetime(2022,12,1, 1,1,1,1)#End Date

# today = datetime.datetime.now()
# month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1])

for i in range((month_end - today).days + 1):
    D = today + datetime.timedelta(i)
    date_object = datetime.datetime.strptime(str(D), "%Y-%m-%d %H:%M:%S.%f")
    DATE = date_object.strftime("%Y-%m-%d")
    print(DATE)