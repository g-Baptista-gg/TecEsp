#%%

'''Imports packages used for the algorithm'''

#%matplotlib qt

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RangeSlider, TextBox, CheckButtons, RadioButtons
import pybaselines
import tkinter as tk
from tkinter import filedialog
import pandas as pd

#%%

'''Sets up the program'''

si = 0
ci = 0
cf = 1
area = 0
mhw = 10
shw = 3
cintg = []

root = tk.Tk()
root.withdraw()
filein = filedialog.askopenfilename()

data = np.array(pd.read_csv(filein))

for i in range(len(data)):
    if data[i,0]>=0:
        _=i
        break
data=data[_:]

#datavec = np.reshape(data, -1)
datavec = data

size = len(datavec[:, 1])
sf = size - 1

bkg = pybaselines.smooth.snip(datavec[si:sf, 1], max_half_window = mhw, decreasing = False, smooth_half_window = shw)[0]
df = (datavec[si:sf, 1] - bkg).astype(int)
X = np.linspace(0, size - 1, size)

#%%

'''Definition of needed functions'''

def update(*args):
    '''Updates the graph everytime a variable is changed'''
    
    global si
    global sf
    global ci
    global cf
    global bkg
    global df
    
    si = sint.val[0]
    sf = sint.val[1]
    ci = cint.val[0]
    cf = cint.val[1]
    mhw = smhw.val
    shw = sshw.val
    c = cb.get_status()
    
    bkg = pybaselines.smooth.snip(datavec[si:sf, 1], max_half_window = mhw, decreasing = False, smooth_half_window = shw)[0]
    df = (datavec[si:sf, 1] - bkg).astype(int)
    
    if len(cintg):
        for i in cintg:
            try:
                i.remove()
            except ValueError:
                continue
    cintg.append(a.axvspan(ci, cf, alpha = 0.5, color = 'red'))
    
    if c[0] == True:
        wob.set_data(datavec[si:sf, 0], df)
        s.set_data(datavec[si:sf, 0], bkg)
    else:
        wob.set_data([], [])
        s.set_data([], [])
    fig.canvas.draw_idle()

def open_spectrum(*args):
    '''Opens and plots a new spectrum'''
    
    global datavec

    
    filein = filedialog.askopenfilename()

    data = np.array(pd.read_csv(filein))
    for i in range(len(data)):
        if data[i,0]>=0:
            _=i
            break
    data=data[_:]
    
    #datavec = np.reshape(data, -1)
    datavec = data

    size = len(datavec[:, 0])
    X = np.linspace(0, size - 1, size)
    
    o.set_data(datavec[:, 0], datavec[:, 1])
    a.set_title(filein)
    a.set_ylim(0, datavec[:, 1].max() * 1.1)
    a.set_xlim(0, datavec[:, 0].max())
    update()

def save(*args):
    '''Saves current spectrum after applying the SNIP algorithm'''
    
    fileout = filedialog.asksaveasfilename(defaultextension='.dat')
    
    #datasave = np.zeros(size, dtype = int)
    #datasave[si:sf] = df
    
    #np.savetxt(fileout, datasave, fmt = '%6d')
    DF=pd.DataFrame()
    DF['en']=datavec[si:sf, 0]
    DF['counts'] = pd.DataFrame(df)
    
    DF.to_csv(fileout,index=False)




def reset(*args):
    '''Resets the range sliders regarding Count and SNIP intervals'''
    
    cint.valmax = 1023    
    cint.set_val([0, 1])
    cint.ax.set_xlim(0, cint.valmax)
    sint.valmax = 1023
    sint.set_val([0, 1023])
    sint.ax.set_xlim(0, sint.valmax)

def count(*args):
    '''Gives the area of the region of interest (ROI), with or without SNIP according to checkbox value'''
    
    area = 0
    c = cb.get_status()
    
    if c[1] == True:
        for j in range(ci, cf, 1):
            area = area + df[j - si]
    else:
        for j in range(ci, cf, 1):
            area = area + datavec[j]
    tb.set_val(int(area))

def close(*args):
    '''Closes the program'''
    
    plt.close()
    
def newmax(*args):
    '''Sets new maximum value for the range sliders of Count and SNIP intervals'''
    
    if cint.val[1] > int(tb2.text):
        cint.set_val((0, int(tb2.text)))
    if sint.val[1] > int(tb2.text):
        sint.set_val((0, int(tb2.text)))
    cint.valmax = int(tb2.text)
    cint.ax.set_xlim(0, cint.valmax)
    sint.valmax = int(tb2.text)
    sint.ax.set_xlim(0, sint.valmax)
    

#%%

'''MatPlotLib Figure Configuration'''

fig = plt.figure(figsize = (12, 7))
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
a = plt.axes([0.15, 0.3, 0.7, 0.6])
o, = plt.plot(datavec[:, 0], datavec[:, 1], color = "red", label = 'Original')
wob, = plt.plot(datavec[si:sf, 0], df, color = "blue", label = 'W/o Baseline')
s, = plt.plot(datavec[si:sf, 0], bkg, '--', color = 'orange', label ='SNIP')

plt.title(filein)
cintg.append(a.axvspan(ci, cf, alpha = 0.5, color='red'))
plt.xlim(datavec[:, 0].min(), datavec[:, 0].max())
plt.ylim(0, datavec[:, 1].max() * 1.1)
plt.xlabel('Channel')
plt.ylabel('Counts')
plt.legend()

#Used axes colors
buttoncolor = 'aquamarine'
buttoncolor2 = 'paleturquoise'
tbcolor = 'lightcyan'
slidercolor = 'royalblue'
slidercolor2 = 'lavender'

caxes = plt.axes([0.1, 0.18, 0.35, 0.03], facecolor = slidercolor2)
cint = RangeSlider(caxes, 'Count Interval', 0, X.max(), valinit = [ci, cf], valstep = 1, color = slidercolor)

snaxes = plt.axes([0.1, 0.13, 0.35, 0.03], facecolor = slidercolor2)
sint = RangeSlider(snaxes, 'SNIP Interval', 0, size - 1, valinit = [si, sf], valstep = 1, color = slidercolor)

maxes = plt.axes([0.6, 0.18, 0.35, 0.03], facecolor = slidercolor2)
smhw = Slider(maxes, 'MHW', 2, 100, valinit = mhw, valstep = 1, color = slidercolor)

saxes = plt.axes([0.6, 0.13, 0.35, 0.03], facecolor = slidercolor2)
sshw = Slider(saxes, 'Smooth', 0, 10, valinit = shw, valstep = 1, color = slidercolor)

tbax = plt.axes([0.9, 0.65, 0.05, 0.03])
tb = TextBox(tbax, '', initial = '0', color = tbcolor, hovercolor = tbcolor)

tbax2 = plt.axes([0.21, 0.05, 0.05, 0.03])
tb2 = TextBox(tbax2, '', initial = '0', color = tbcolor, hovercolor = tbcolor)

cbaxes = plt.axes([0.875, 0.43, 0.1, 0.14], facecolor = tbcolor)
cb = CheckButtons(cbaxes, ['SNIP Graph', 'SNIP Count'], [True, False])

bax1 = plt.axes([0.9, 0.85, 0.05, 0.03])
button1 = Button(bax1, 'Open', color = buttoncolor, hovercolor = buttoncolor2)
button1.on_clicked(open_spectrum)
  
bax2 = plt.axes([0.9, 0.7, 0.05, 0.03])
button2 = Button(bax2, 'Count', color = buttoncolor, hovercolor = buttoncolor2)
button2.on_clicked(count)

bax3 = plt.axes([0.9, 0.8, 0.05, 0.03])
button3 = Button(bax3, 'Save', color = buttoncolor, hovercolor = buttoncolor2)
button3.on_clicked(save)
  
bax4 = plt.axes([0.9, 0.6, 0.05, 0.03])
button4 = Button(bax4, 'Quit', color = buttoncolor, hovercolor = buttoncolor2)
button4.on_clicked(close)

bax5 = plt.axes([0.9, 0.75, 0.05, 0.03])
button5 = Button(bax5, 'Reset', color = buttoncolor, hovercolor = buttoncolor2)
button5.on_clicked(reset)

bax6 = plt.axes([0.1, 0.05, 0.1, 0.03])
button6 = Button(bax6, 'New Max Value', color = buttoncolor, hovercolor = buttoncolor2)
button6.on_clicked(newmax)

#Updates Plot
cint.on_changed(update)
sint.on_changed(update)
smhw.on_changed(update)
sshw.on_changed(update)
cb.on_clicked(update)

plt.show()