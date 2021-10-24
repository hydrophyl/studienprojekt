import datetime
from datetime import timedelta
import os
import wget
import pandas as pd
import urllib.request
from utils import *

# define sensor_id here
sensor_id = "12776407"

# Main program
today = datetime.date.today()
yesterday = today - timedelta(days=1)
today = str(today)
daysinmonth = int(str(today)[-2:])
if daysinmonth < 7:
    daysinweek = daysinmonth
else:
    daysinweek = 7
# convert to string for managing files
yesterday = str(yesterday)
today = str(today)

# check if todays data is available or not, if not then download latest data of yesterday
link = (
    "https://api-rrd.madavi.de/data_csv/csv-files/"
    + today
    + "/data-esp8266-"
    + sensor_id
    + "-"
    + today
    + ".csv"
)
req = urllib.request.Request(link)

# create list that contains 7 days since today
dayformat = "%Y-%m-%d"
today = datetime.datetime.strptime(today, dayformat)
week = []
for i in range(daysinweek):
    week.append(today - timedelta(days=i))
    week[i] = str(week[i])[:10]

# create list that contains 30 days since today
month = []
for i in range(daysinmonth):
    day = today - timedelta(days=i)
    day = day.strftime("%Y-%m-%d")
    stoday = today.strftime("%Y-%m-%d")
    if int(day[5:7]) < int(stoday[5:7]):
        break
    month.append(day)
    month[i] = str(month[i])[:10]

yesterday = str(yesterday)[:10]
today = str(today)[:10]
# find last month and export to string
last_month = int(str(today)[5:7])  # 10
last_month = 12 if last_month == 1 else last_month - 1
if len(str(last_month)) == 1:
    last_month = "0" + str(last_month)  # 09
# delete_junk_csv(last_month)

try:
    urllib.request.urlopen(req)
    filename = "data-esp8266-" + sensor_id + "-" + today + ".csv"
    files = os.listdir()
    for file in files:
        if str(file) == str(filename):
            oldsize = os.stat(filename).st_size
    check(sensor_id, today)
    print("\nTodays data will be downloaded!\n")
    wget.download(link)
    size = os.stat(filename).st_size
    path = "./month"
    isdir = os.path.isdir(path)
    if oldsize > 0 and size == oldsize and isdir == True:
        print("\nlatest data is already downloaded!")
    else:
        try:
            fetch_datas(sensor_id, week, month, last_month)
        except urllib.error.URLError as e:
            print(e)
except urllib.error.URLError as e:
    print(e.reason + "\n")
    print("\nTodays data isn't updated on server\n")
    print("\nDownloading yesterdays data\n")
    today = yesterday
    filename = "data-esp8266-" + sensor_id + "-" + today + ".csv"
    files = os.listdir()
    for file in files:
        if str(file) == str(filename):
            oldsize = os.stat(filename).st_size
    check(sensor_id, today)
    link = (
        "https://api-rrd.madavi.de/data_csv/csv-files/"
        + today
        + "/data-esp8266-"
        + sensor_id
        + "-"
        + today
        + ".csv"
    )
    wget.download(link)
    size = os.stat(filename).st_size
    path = "./month"
    isdir = os.path.isdir(path)
    if oldsize > 0 and size == oldsize and isdir == True:
        print("\nlatest data is already downloaded!")
    else:
        try:
            fetch_datas(sensor_id, week, month, last_month)
        except urllib.error.URLError as e:
            print(e)


def get_df_all():
    df_all = pd.read_csv("./all/merged.csv", sep=",")
    df_all["Time"] = df_all["Time"].apply(convert_datetime)
    return df_all


def get_df_today():
    df = pd.read_csv(filename, sep=";")
    df["Time"] = df["Time"].apply(convert_datetime)
    return df


def get_df_lastmonth():
    df_last_month = pd.read_csv(
        "./" + last_month + "/merged.csv", sep=",", low_memory=False
    )
    df_last_month["Time"] = pd.to_datetime(df_last_month["Time"], errors="coerce")
    return df_last_month


def get_df_month():
    df_month = pd.read_csv("./month/merged.csv", sep=",")
    df_month["Time"] = df_month["Time"].apply(convert_datetime)
    return df_month


def get_df_week():
    df_week = pd.read_csv("./week/merged.csv", sep=",")
    df_week["Time"] = df_week["Time"].apply(convert_datetime)
    return df_week
