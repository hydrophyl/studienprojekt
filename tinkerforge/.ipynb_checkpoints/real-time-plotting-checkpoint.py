#setting up packages
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.express as px
import datetime
from time import strftime,localtime

date_local = strftime("%d%b%Y", localtime())
#Empty arrays for plotting in real-time
x_vals = []
y1_vals = []
y2_vals = []
y3_vals = []

def animate(i):
    feinstaub = pd.read_csv(date_local + '.csv')
    x_vals=feinstaub['Zeit']
    y1_vals=feinstaub['PM10']
    y2_vals=feinstaub['PM25']
    y3_vals=feinstaub['PM100']
    plt.cla()
    plt.plot(x_vals, y1_vals, label='PM1.0')
    plt.plot(x_vals, y2_vals, label='PM2.5')
    plt.plot(x_vals, y3_vals, label='PM10.0')
    plt.xticks([])
    plt.legend(loc='upper right')
    plt.tight_layout()
  
if __name__ == "__main__":
  ani = FuncAnimation(plt.gcf(), animate, interval=1000)
  plt.show()

#try using plotly and dash