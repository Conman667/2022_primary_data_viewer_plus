from cProfile import run
from tkinter import *
from unicodedata import numeric
import requests
from contextlib import closing
import csv
import json
import time
import datetime
from colorama import init
from colorama import Fore, Back, Style
import tkinter
import logging

def gt():
    now = datetime.datetime.now()
    string = '(' + now.strftime('%d/%m_%H:%M:%S') + ') '

    return string

logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG)

init()

logging.debug(' \n ')
logging.debug(gt() + 'program started')
print("start")

logging.debug(gt() + 'setting filter time params')
grabEnd = datetime.datetime.now()
grabStart = datetime.datetime.today() - datetime.timedelta(days=30)
logging.debug(gt() + 'grabEnd = ' + grabEnd.strftime('%d/%m/%y'))
logging.debug(gt() + 'grabStart = ' + grabStart.strftime('%d/%m/%y'))

def read(url):
    logging.debug(gt() + 'read function')
    with closing(requests.get(url, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        data = csv.reader(f, delimiter=',', quotechar='"')
        result = list(data)
        logging.debug(gt() + 'data read')
        return result

def fd(d):
    logging.debug(gt() + 'sort function')
    logging.debug(gt() + 'sort begin = ' + str(len(d)))
    count = 0
    while count < len(d):
        if count > 0:
            temp = datetime.datetime.strptime(d[count][12], '%m/%d/%y')
            if grabEnd >= temp >= grabStart:
                count += 1
            elif temp < grabStart:
                d.remove(d[count])
        else:
            logging.debug(gt() + 'skipping lables')
            count += 1
    logging.debug(gt() + 'sort end = ' + str(len(d)))
    return d


def ptd(d):
    numd = 0.0
    numr = 0.0
    for row in d:
        if (row[37].__eq__("DEM")):
            numd += float(row[41])
        elif row[37].__eq__("REP"):
            numr = float(row[41]) + numr
    total = numd + numr
    return float(numd / total)

def rgb_hex(rgb):
    return '%02x%02x%02x' % rgb

logging.debug(gt() + 'starting url read of senate') # + f'{senate=}'.split('=')[0]
senate = read('https://projects.fivethirtyeight.com/polls-page/data/senate_polls.csv')
logging.debug(gt() + 'starting url read of house')
house = read('https://projects.fivethirtyeight.com/polls-page/data/house_polls.csv')
logging.debug(gt() + 'starting url read of governor')
governor = read('https://projects.fivethirtyeight.com/polls-page/data/governor_polls.csv')

logging.debug(gt() + 'starting sort of senate')
senate = fd(senate)
logging.debug(gt() + 'starting sort of house')
house = fd(house)
logging.debug(gt() + 'starting sort of governor')
governor = fd(governor)

logging.debug(gt() + 'setting color values')
colorB = int(((ptd(senate) + ptd(house) + ptd(governor))/3)*255)
colorR = 255 - colorB
logging.debug(gt() + 'blue = ' + str(colorB) + ' (' + str(float(colorB / 255)) + '%)')
logging.debug(gt() + 'red = ' + str(colorR) + ' (' + str(float(colorR / 255)) + '%)')

rgb = (colorB, 0, colorR)
logging.debug(gt() + 'formatting to rgb: ' + str(rgb))

logging.debug(gt() + 'setting window')
Window = Tk()

Window.title("Election Data Viewer")

Window.configure(width=500, height=500)

logging.debug(gt() + 'applying color values')
Window.configure(bg='#' + rgb_hex(rgb))

menubar = tkinter.Menu(Window)

Window.config(menu=menubar)

file_menu = Menu(menubar, tearoff=False)

file_menu.add_command(label='Governor')
file_menu.add_command(label='House')
file_menu.add_command(label='Senate')
file_menu.add_command(label='Exit', command = Window.destroy)

menubar.add_cascade(label="File", menu=file_menu)

logging.debug(gt() + 'opening window')
Window.mainloop()