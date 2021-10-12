import datetime
import wget
import os 

date = datetime.date.today()
date = str(date)

filename = 'data-esp8266-12776407-'+ date + '.csv'
os.remove(filename) # if exist, remove it 
wget.download('https://api-rrd.madavi.de/data_csv/csv-files/'+ date + '/data-esp8266-12776407-'+ date + '.csv')