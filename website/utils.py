import datetime
import os
import wget
import requests_html
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import shutil
import glob
from zipfile import ZipFile


def check(sensor_id, today):
    filename = "data-esp8266-" + sensor_id + "-" + today + ".csv"
    files = os.listdir()
    for file in files:
        if str(file) == str(filename):
            os.remove(filename)  # if exist, remove it
    return


# convert Time string to datetime type
def convert_datetime(dt_string):
    format = "%Y/%m/%d %H:%M:%S"
    dt_object = datetime.datetime.strptime(dt_string, format)
    return dt_object


def checkfolder(folder):
    path = "./" + folder
    isdir = os.path.isdir(path)
    if isdir == True:
        shutil.rmtree(path)
        print("% s removed successfully" % path + "\n")
    else:
        print("Creating " + folder + "\n")


# download weekly datas
def download_datas(sensor_id, folder, timeinterval):
    path = "./" + folder + ""
    os.mkdir(folder)
    for date in timeinterval:
        date = str(date)
        link = (
            "https://api-rrd.madavi.de/data_csv/csv-files/"
            + date
            + "/data-esp8266-"
            + sensor_id
            + "-"
            + date
            + ".csv"
        )
        wget.download(link, path)


def join_csvfiles(folder):
    path = "./" + folder + ""
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=";") for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)
    df_merged.to_csv("./" + folder + "/merged.csv")


# plotting latest data of one day in plotly
def plotting(df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df["Time"], y=df["SDS_P1"], name="PM2.5", line=dict(color="#7355A3")
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Time"], y=df["SDS_P2"], name="PM10", line=dict(color="#E47988")
        ),
        secondary_y=True,
    )
    # Add figure title
    fig.update_layout(title_text="PM2.5 & PM10", height=600)
    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    # Set y-axes titles
    fig.update_yaxes(title_text="PM2.5", secondary_y=False)
    fig.update_yaxes(title_text="PM10", secondary_y=True)
    return fig


def plotting_temperature_humidity(df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df["Time"], y=df["Temp"], name="Temperatur", line=dict(color="#E47988")
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Time"],
            y=df["Humidity"],
            name="Luftfeuchtigkeit",
            line=dict(color="#53a7fc"),
        ),
        secondary_y=True,
    )
    # Add figure title
    fig.update_layout(title_text="Temperatur und Luftfeuchtigkeit", height=600)
    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    # Set y-axes titles
    fig.update_yaxes(title_text="Temperatur [°C]", secondary_y=False)
    fig.update_yaxes(title_text="Luftfeuchtigkeit [%]", secondary_y=True)
    return fig


# fetch all datas (weekly, monthly, lastmonth, alltime)
def fetch_datas(sensor_id, week, month, last_month):
    # WEEKLY and MONTHLY datas fetching
    checkfolder("week")
    download_datas(sensor_id, "week", week)
    join_csvfiles("week")

    # fetch and plot data of one month
    checkfolder("month")
    download_datas(sensor_id, "month", month)
    join_csvfiles("month")

    # download data of last month
    last_month_link = (
        "https://api-rrd.madavi.de/data_csv/2021/"
        + last_month
        + "/data-esp8266-"
        + sensor_id
        + "-2021-"
        + last_month
        + ".zip"
    )
    checkfolder(last_month)
    path = "./" + last_month
    os.mkdir(last_month)
    wget.download(last_month_link, path)

    dir = os.listdir(path)
    file = dir[0]
    path = path + "/" + file
    # open the zip file in read mode
    with ZipFile(path, "r") as zip:
        # extract all files to directory
        zip.extractall(last_month)
    os.remove(path)  # delete zip file
    join_csvfiles(last_month)

    # Find links of zip datas from api
    months = []
    with requests_html.HTMLSession() as s:
        try:
            r = s.get(
                "https://api-rrd.madavi.de/csvfiles.php?sensor=esp8266-" + sensor_id
            )
            links = r.html.links
            for link in links:
                if link[-3:] == "zip":
                    months.append(link)
        except:
            pass

    # download all zip files of past months
    checkfolder("all")
    path = "./all"
    os.mkdir("all")
    for link in months:
        download_link = "https://api-rrd.madavi.de/" + link
        wget.download(download_link, path)

    # extract zip files
    days = os.listdir("./all")
    for day in days:
        path = "./all/" + day
        with ZipFile(path, "r") as zip:
            # extract all files to directory
            zip.extractall("all")
        os.remove(path)

    # download datas of this month to the all-folder
    for date in month:
        path = "./all"
        date = str(date)
        link = (
            "https://api-rrd.madavi.de/data_csv/csv-files/"
            + date
            + "/data-esp8266-"
            + sensor_id
            + "-"
            + date
            + ".csv"
        )
        wget.download(link, path)
    join_csvfiles("all")
