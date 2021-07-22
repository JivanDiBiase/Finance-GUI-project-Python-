# Libraries and useful imports:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# - Dataframe manipulation libraries
import pandas as pd

# - GUI building libraries
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# - Data extraction libraries
import requests

# - Data plots libraries
import mplfinance as mplf
import matplotlib.pyplot as plt

# Storage and preliminary variables:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
API_key = 'XXXXX' #Free API key available at: https://www.alphavantage.co/support/#api-key

 # - File paths to all images used by the interface. Images included in the zip file downloaded, please change the file paths stored in the variables below and put in the variables the file paths shown specifically by your computer:
Image_directory_bg = r"XXXXX"
Image_directory_bl = r"XXXXX"


# Defined functions:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_df():
    # *This function requests stock price data from the API in JSON format and arranges the data recieved into a readable dataframe*.
    
    # - Extracting data from the API:
    ticker_input = input_txt_box.get()
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker_input + '&apikey=' + API_key
    r = requests.get(url)
    price_df = r.json()
    
    # - Extracting prices data from JSON list provvided by API:
    price_df_tr = price_df['Time Series (Daily)']
    
    # - Treeview building:
    tree = ttk.Treeview(bottom_frame)
    tree['columns'] = ('Date', 'Open', 'High', 'Low', 'Close', 'Volume')
    
    tree.column('#0', width = 1, minwidth = 1)
    tree.column('Date', anchor = dt_anchor, width = dt_width)
    tree.column('Open', anchor = opn_anchor, width = opn_width)
    tree.column('High', anchor = high_anchor, width = high_width)
    tree.column('Low', anchor = lw_anchor, width = lw_width)
    tree.column('Close', anchor = cls_anchor, width = cls_width)
    tree.column('Volume', anchor = vol_anchor, width = vol_width)
        
    tree.heading('#0', text = ' ', anchor = "w")
    tree.heading('Date', text = dt_head, anchor = dt_anchor)
    tree.heading('Open', text = opn_head, anchor = opn_anchor)
    tree.heading('High', text = high_head, anchor = high_anchor)
    tree.heading('Low', text = lw_head, anchor = lw_anchor)
    tree.heading('Close', text = cls_head, anchor = cls_anchor)
    tree.heading('Volume', text = vol_head, anchor = vol_anchor)
    
    # - For loop itterates trough every line of JSON dictionary and extracts for each date, its respective stock prices:
    for dates in price_df_tr:
        date = dates
        opn = price_df_tr[str(dates)]['1. open']
        high = price_df_tr[str(dates)]['2. high']
        lw = price_df_tr[str(dates)]['3. low']
        close = price_df_tr[str(dates)]['4. close']
        vol = price_df_tr[str(dates)]['5. volume']
        
        # - For each itteration of the for loop, this line generates its resepctive output row to put in the treeview to show as dataframe in the interface:
        tree.insert(parent = '', index = 'end', text = '-', values = (date, opn, high, lw, close, vol))
    
    # - Placing the treeview on the interface:
    tree.place(relwidth = 1, relheight = 1)        

    return None

def get_graph():
    # *This function requests stock price data from the API in JSON format, aranges it into a dataframe that is readable by the mplfinance function and plots the candlestick graph for the user to see.*
    
    # - Extracting data from the API:
    ticker_input = input_txt_box.get()
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker_input + '&apikey=' + API_key
    r = requests.get(url)
    price_df = r.json()
    
    # - Extracting prices data from JSON list:
    price_df_tr = price_df['Time Series (Daily)']
    
    # - These lists contain the data that make up the dataframe columns:
    date_rev = []
    open_rev = []
    high_rev = []
    low_rev = []
    close_rev = []
    volume_rev = []
    
    
    # - For loop itterates trough every line of JSON dictionary and extracts for each date the respective stock prices:
    for dates in price_df_tr:
        opn = price_df_tr[str(dates)]['1. open']
        high = price_df_tr[str(dates)]['2. high']
        lw = price_df_tr[str(dates)]['3. low']
        close = price_df_tr[str(dates)]['4. close']
        vol = price_df_tr[str(dates)]['5. volume']
        
        # - In this step, each figure extracted by the for loop is converted into float format to make it compatible to the mplfinance function:
        date_rev.append(dates)
        open_rev.append(float(opn))
        high_rev.append(float(high))
        low_rev.append(float(lw))
        close_rev.append(float(close))
        volume_rev.append(float(vol))
    
    # - In this step, the data contained by the "_rev" lists is reversed in order and stored in separate lists:
    Date = date_rev[::-1]
    Open = open_rev[::-1]
    High = high_rev[::-1]
    Low = low_rev[::-1]
    Close = close_rev[::-1]
    Volume = volume_rev[::-1] 
    
    # - In this step the data contained in the above mentioned lists is arranged together to create a pandas-formatted dataframe with column names that are readable by the mplfinance function:
    plot_list = list(zip(Date, Open, High, Low, Close, Volume))
    cols = ['Date','Open', 'High', 'Low', 'Close', 'Volume']
    plot_df = pd.DataFrame(plot_list, columns = cols)

    # - Plotting the candlestick graph:
    plot_df_final = plot_df.set_index(pd.DatetimeIndex(plot_df['Date']))

    mplf.plot(plot_df_final, type = 'candle', volume = True)
    plt.show()    
    
    return None

# GUI dimensions:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# - Canvas:
canvas_height = 700
canvas_width = 800

# - Background immage label:
bg_im_relx = 0
bg_im_rely = 0
bg_im_rel_h = 1
bg_im_rel_w = 1

# - Input frame:
Inp_f_bg_colour = '#0000ff'
Inp_f_border_dim = 5
Inp_f_relx = 0.7
Inp_f_rely = 0.07
Inp_f_rel_h = 0.14
Inp_f_rel_w = 0.35
Inp_f_anchor = 'n'

# - Intro frame:
int_f_bg_colour = '#0000ff'
int_f_border_dim = 5
int_f_relx = 0.125
int_f_rely = 0.07
int_f_rel_h = 0.14
int_f_rel_w = 0.4
int_f_anchor = 'n'

# - Intro label 1:
txt_intro_lbl = 'Welcome to Jeevan\'s stock query application! Input the ticker of any NYSE company and get its past 100 days daily stock prices (Per unit of 1$).'
int_lbl_relx = 0
int_lbl_rely = 0
int_lbl_rel_h = 1
int_lbl_rel_w = 1
int_lbl_wl = 300
int_lbl_fnt = 40

# - Input text box:
txt_b_font = 40
txt_b_rel_w = 1
txt_b__rel_h = 0.4
txt_b_relx = 0
txt_b_rely = 0

# - Numerical data button:
bt_num_rel_fnt = 20
bt_num_rel_h = 0.5
bt_num_rel_w = 0.5
bt_num_relx = 0
bt_num_rely = 0.5
output2user_num = 'Get data frame'

# - Data plot button:
bt_plt_rel_fnt = 20
bt_plt_rel_h = 0.5
bt_plt_rel_w = 0.5
bt_plt_relx = 0.5
bt_plt_rely = 0.5
output2user_plt = 'Get data plot'

# - Bottom frame:
bf_bg_colour = '#0000ff'
bf_border_dim = 5
bf_relx = 0.5
bf_rely = 0.25
bf_rel_w = 0.75
bf_rel_h = 0.6
bf_anchor = 'n'

# - Bottom frame immage label:
bf_im_relx = 0
bf_im_rely = 0
bf_im_rel_h = 1
bf_im_rel_w = 1

# - Numerical data output:
otp_txt_bg = 'white'
otp_txt_font = 40
otp_txt_rel_w = 1
otp_txt_rel_h = 1

# - Column 'Date:
dt_anchor = 'w'
dt_width = 25
dt_head = 'Date'

# - Column 'Open':
opn_anchor = 'w'
opn_width = 25
opn_head = 'Open'

# - Column 'High':
high_anchor = 'w'
high_width = 25
high_head = 'High'

# - Column 'Low':
lw_anchor = 'w'
lw_width = 25
lw_head = 'Low'

# - Column 'Close':
cls_anchor = 'w'
cls_width = 25
cls_head = 'Close'

# - Column 'Volume':
vol_anchor = 'w'
vol_width = 25
vol_head = 'Volume'

# GUI molding:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root_window = tk.Tk()

# - Window dimensions:
canvas = tk.Canvas(root_window, height = canvas_height, width = canvas_width)
canvas.pack()

# - Background proprieties:
bg_image = ImageTk.PhotoImage(Image.open(Image_directory_bg))
bg_lbl = tk.Label(root_window, image = bg_image)
bg_lbl.place(relx = bg_im_relx, rely = bg_im_rely, relwidth = bg_im_rel_w, relheight = bg_im_rel_h)
   
# - Intro frame (Frame on the upper side of the GUI, this frame stores label with the wellcome message and brief instructions for the user.):
intro_frame = tk.Frame(root_window, bg = int_f_bg_colour, bd = int_f_border_dim)
intro_frame.place(relx = int_f_relx, rely = int_f_rely, relheight = int_f_rel_h, relwidth = int_f_rel_w)

# - Intro label (Label on the upper side of the GUI, it stores the welcome message and brief instructions for the user.):
intro_lbl1 = tk.Label(intro_frame, text = txt_intro_lbl, wraplength = int_lbl_wl, font = int_lbl_fnt)
intro_lbl1.place(relx = int_lbl_relx, rely = int_lbl_rely, relheight = int_lbl_rel_h, relwidth = int_lbl_rel_w)

# - Input frame (Frame on the upper side of the GUI, it stores the text box where the user writes the company's ticker symbol.):
input_frame = tk.Frame(root_window, bg = Inp_f_bg_colour, bd = Inp_f_border_dim)
input_frame.place(relx = Inp_f_relx, rely = Inp_f_rely, relheight = Inp_f_rel_h, relwidth = Inp_f_rel_w, anchor = Inp_f_anchor)

# - Search box (Label on the upper side of the GUI. The user writes companies' thicker symbols in it.):
input_txt_box = tk.Entry(input_frame, font=txt_b_font)
input_txt_box.place(relx = txt_b_relx, rely = txt_b_rely, relwidth = txt_b_rel_w, relheight = txt_b__rel_h)

# - Numerical data button (Located on the upper side of the GUI. When pressed, the application returns a dataframe of the last 100 days company stock prices.):
button_n = tk.Button(input_frame, text=output2user_num, font=bt_num_rel_fnt, command = lambda: get_df())
button_n.place(relx = bt_num_relx, rely = bt_num_rely, relheight = bt_num_rel_h, relwidth = bt_num_rel_w)

# - Numerical data button (Located on the upper side of the GUI. When pressed, the application returns a candlestick plot of the last 100 days company stock prices):
button_p = tk.Button(input_frame, text=output2user_plt, font=bt_plt_rel_fnt, command = lambda: get_graph())
button_p.place(relx = bt_plt_relx, rely = bt_plt_rely, relheight = bt_plt_rel_h, relwidth = bt_plt_rel_w)

# - Bottom frame (Located on the lower side of the GUI. At the start, it simply contains label with a picture of the New York Stock Exchange trading room, when the "Get dataframe" button is pressed, this frame sows the dataframe of the last 100 days company stock prices.):
bottom_frame = tk.Frame(root_window, bg=bf_bg_colour, bd=bf_border_dim)
bottom_frame.place(relx = bf_relx, rely = bf_rely, relwidth = bf_rel_w, relheight = bf_rel_h, anchor = bf_anchor)

# - Bottom frame image label (Located on the bottom side of the GUI. It simply contains a picture fo the New York Stock Exchange trading room):
bf_image = ImageTk.PhotoImage(Image.open(Image_directory_bl))
bf_im_lbl = tk.Label(bottom_frame, image = bf_image)
bf_im_lbl.place(relx = bf_im_relx, rely = bf_im_rely, relwidth = bf_im_rel_w, relheight = bf_im_rel_h)


root_window.mainloop()

