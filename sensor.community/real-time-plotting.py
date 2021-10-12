#setting up packages
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.express as px
import datetime
import wget
import os 

date = datetime.date.today()
date = str(date)
filename = 'data-esp8266-12776407-'+ date + '.csv'

#Empty arrays for plotting in real-time
x_vals = []
y1_vals = []
y2_vals = []

files = os.listdir()
wget.download('https://api-rrd.madavi.de/data_csv/csv-files/'+ date + '/data-esp8266-12776407-'+ date + '.csv')

def animate(i):
    os.remove(filename)
    wget.download('https://api-rrd.madavi.de/data_csv/csv-files/'+ date + '/data-esp8266-12776407-'+ date + '.csv')
    feinstaub = pd.read_csv("data-esp8266-12776407-" + date + ".csv", sep=";")
    x_vals=feinstaub['Time']
    y1_vals=feinstaub['SDS_P1']
    y2_vals=feinstaub['SDS_P2']
    plt.cla()
    plt.plot(x_vals, y1_vals, label='PM2.5')
    plt.plot(x_vals, y2_vals, label='PM10.0')
    plt.xticks([])
    plt.legend(loc='upper right')
    plt.tight_layout()
  
if __name__ == "__main__":
  ani = FuncAnimation(plt.gcf(), animate, interval=1000)
  plt.show()

#try using plotly and dash