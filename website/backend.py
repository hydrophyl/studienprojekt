import datetime
from datetime import timedelta
import os
import wget
import pandas as pd
import urllib.request
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import shutil
import glob
import requests_html 
from zipfile import ZipFile 

#define sensor_id here
sensor_id = "12776407"

today = datetime.date.today()
yesterday = today - timedelta(days = 1)
today = str(today)

#check if todays data already downloaded
def check():  
    filename = 'data-esp8266-'+sensor_id+'-'+today+'.csv'
    files = os.listdir()
    for file in files:
        if str(file) == str(filename):
            os.remove(filename) # if exist, remove it 
    return

#convert Time string to datetime type
format = "%Y/%m/%d %H:%M:%S"
def convert_datetime(dt_string):
    dt_object = datetime.datetime.strptime(dt_string, format)
    return dt_object
    
def checkfolder(folder):
    path = './' + folder
    isdir = os.path.isdir(path)
    if isdir == True:
        shutil.rmtree(path)
        print("% s removed successfully" % path + "\n")
    else:
        print("Creating " + folder + "\n")

#download weekly datas
def download_datas(folder,timeinterval):
    path = './' + folder + ''
    os.mkdir(folder)
    for date in timeinterval:
        date=str(date)
        link = 'https://api-rrd.madavi.de/data_csv/csv-files/'+ date + '/data-esp8266-'+sensor_id+'-'+ date + '.csv'
        wget.download(link, path)
        
def join_csvfiles(folder):
    path = './' + folder + ''
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=';') for f in all_files)
    df_merged   = pd.concat(df_from_each_file, ignore_index=True)
    df_merged.to_csv("./"+folder+"/merged.csv")
    
def filename():
  return filename

#plotting latest data of one day in plotly
def plotting(df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df['Time'], y=df['SDS_P1'], name="PM2.5", line=dict(color='#7355A3')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['Time'], y=df['SDS_P2'], name="PM10", line=dict(color='#E47988')),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="PM2.5 & PM10",
        height=600
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")

    # Set y-axes titles
    fig.update_yaxes(title_text="PM2.5", secondary_y=False)
    fig.update_yaxes(title_text="PM10", secondary_y=True)
    return fig 

#Main program
daysinmonth = int(str(today)[-2:])
if daysinmonth < 7:
    daysinweek = daysinmonth
else:
    daysinweek = 7
#convert to string for managing files
yesterday = str(yesterday)
today = str(today)

# check if todays data is available or not, if not then download latest data of yesterday
link = 'https://api-rrd.madavi.de/data_csv/csv-files/'+ today + '/data-esp8266-'+sensor_id+'-'+ today + '.csv'
req = urllib.request.Request(link)
try: 
    urllib.request.urlopen(req)
    check()
    filename = 'data-esp8266-'+sensor_id+'-'+today+'.csv'
    print("Todays data will be downloaded!\n")
    wget.download(link)
except urllib.error.URLError as e:
    print(e.reason + "\n")
    print("Todays data isn't updated on server\n")
    print("Downloading yesterdays data\n")
    today = yesterday
    filename = 'data-esp8266-'+sensor_id+'-'+today+'.csv'
    check()
    link = 'https://api-rrd.madavi.de/data_csv/csv-files/'+ today + '/data-esp8266-'+sensor_id+'-'+ today + '.csv'
    wget.download(link)

#create list that contains 7 days since today
dayformat = "%Y-%m-%d"
today = datetime.datetime.strptime(today, dayformat)
week = []
for i in range(daysinweek):
    week.append(today - timedelta(days = i))
    week[i] = str(week[i])[:10]

#create list that contains 30 days since today
month = []
for i in range(daysinmonth):
    day = today - timedelta(days=i)
    day = day.strftime('%Y-%m-%d')
    stoday = today.strftime('%Y-%m-%d')
    if int(day[5:7]) < int(stoday[5:7]):
        break
    month.append(day)
    month[i] = str(month[i])[:10]

yesterday = str(yesterday)[:10]
today = str(today)[:10]

#read dataframe of today
def get_df_today():
  df = pd.read_csv(filename,sep=';')
  df['Time'] = df['Time'].apply(convert_datetime)
  return df

#WEEKLY and MONTHLY datas fetching
checkfolder("week")      
download_datas("week",week)    
join_csvfiles("week")
def get_df_week():
  df_week = pd.read_csv("./week/merged.csv",sep=",")
  df_week['Time'] = df_week['Time'].apply(convert_datetime)
  return df_week

#fetch and plot data of one month
checkfolder("month")
download_datas("month", month)
join_csvfiles("month")
def get_df_month():
  df_month = pd.read_csv("./month/merged.csv",sep=",")
  df_month['Time'] = df_month['Time'].apply(convert_datetime)
  return df_month

#find last month and export to string
last_month = int(str(today)[5:7]) #10
last_month = 12 if last_month == 1 else last_month-1
if len(str(last_month)) == 1:
    last_month = "0" + str(last_month) #09

#download data of last month
last_month_link = "https://api-rrd.madavi.de/data_csv/2021/"+last_month+"/data-esp8266-"+sensor_id+"-2021-"+last_month+".zip"
checkfolder(last_month)
path = './'+last_month
os.mkdir(last_month)
wget.download(last_month_link, path)

dir = os.listdir(path)
file = dir[0]
path = path+"/"+file
# open the zip file in read mode
with ZipFile(path, 'r') as zip: 
    # extract all files to directory
    zip.extractall(last_month)
os.remove(path) #delete zip file
join_csvfiles(last_month)
def get_df_lastmonth():
  df_last_month = pd.read_csv("./"+last_month+"/merged.csv",sep=",",low_memory=False)
  df_last_month['Time'] = pd.to_datetime(df_last_month['Time'], errors='coerce')
  return df_last_month
months = []
with requests_html.HTMLSession() as s:
    try:
        r = s.get('https://api-rrd.madavi.de/csvfiles.php?sensor=esp8266-'+sensor_id)
        links = r.html.links
        for link in links:
            if link[-3:] == "zip":
                months.append(link)
    except:
        pass
        
#download all zip files of past months
checkfolder("all")
path = './all'
os.mkdir("all")
for link in months:
    download_link = "https://api-rrd.madavi.de/"+link
    wget.download(download_link, path)
    
#extract zip files
days = os.listdir("./all")
for day in days:
    path="./all/"+day
    with ZipFile(path, 'r') as zip: 
        # extract all files to directory
        zip.extractall("all")
    os.remove(path)

#download datas of this month to the all-folder
for date in month:
    path = './all'
    date=str(date)
    link = 'https://api-rrd.madavi.de/data_csv/csv-files/'+ date + '/data-esp8266-'+sensor_id+'-'+ date + '.csv'
    wget.download(link, path)

join_csvfiles("all")
def get_df_all():
  df_all = pd.read_csv("./all/merged.csv",sep=",")
  df_all['Time'] = df_all['Time'].apply(convert_datetime)
  return df_all
