# Universidad Autónoma Chapingo
# Luis Ángel Sánchez Rodríguez
# al15123618@chapingo.mx

import tkinter as tk
import matplotlib.pyplot as plt # graphication library
from matplotlib import dates as mdates #to format the x-axis with date and time values
from tkcalendar import DateEntry
from datetime import date, datetime
import pandas as pd # csv file management
from tkinter import * 
from matplotlib.widgets import Slider # Subpaquete para agregar las barras de control
from tkinter import ttk #
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Plot configuration
def config_gra():
    ax[0].set_ylabel( 'Sensor data, [um]', fontsize = 12 )
    ax[0].tick_params('x', labelsize = 10, labelbottom = False)
    
    ax[1].set_ylabel( 'Temperature', fontsize = 12 )
    ax[1].set_xlabel( '$Time$', fontsize = 12 )
    # Adding legend, which helps us recognize the data
    ax[0].legend()
    ax[1].legend()
    fig.subplots_adjust( hspace = 0.0, wspace = 0.1 )
    ax[0].grid(True)
    ax[1].grid(True)
    
    
    
# Close button
def close():
    window.quit()     
    window.destroy()

# clean button
def clean():
    # Clear the current plot
    ax[0].cla() 
    ax[1].cla()
    config_gra()
    canvas.draw()
    
# Open file button
def read_file():
    global df,h_time,h_volt,h_um,data_time,data_um,index_list
    # file directory
    file = filedialog.askopenfilename(initialdir ='/',title='Select a file',filetype=(('csv files', '*.csv*'),('All files', '*.*')))
    # Read file
    df = pd.read_csv(file, delimiter=",") 
    
    # str containing 'header' names
    h_time = df.columns[1] # header time
    h_volt = df.columns[2] # header volts values
    h_um = df.columns[3] # header micrometer values
    # column data
    data_time = df[h_time].to_numpy() # dates column
    data_um = df[h_um].to_numpy() # data micrometer

    # the index is numeric. We want to make it time-aware using the data in the Date and Time column 
    # to be able to select rows in time ranges.
    # For that, we use the function pd.DatetimeIndex, 
    # and send as argument the column from te table that has the date and time.
    index_list = df.index
    index_list = pd.DatetimeIndex(data_time)
    
    
# Plot graph function
def my_upd(): 
    global index_list, fig, ax, data_um
    # ----------------------------> Temperature txt file <-----------------------------------
    # path, change it
    data_path = "C:/Users/luis_/Downloads/10minutenwerte_TU_00044_akt/produkt_zehn_min_tu_20201105_20220508_00044.txt"
    
    # Read the csv file, delimited by ';'
    df_temp = pd.read_csv(data_path, delimiter = ";")
    time_temp = df_temp.columns[1] # dates column # time_temp = df_temp['MESS_DATUM']
    temp_temp = df_temp.columns[4] # temperature data column # temp_temp = df_temp['TT_10']
    
    # transform to list an array to manipulate dates better
    data_time_temp = df_temp[time_temp].tolist()
    data_temp = df_temp[temp_temp].to_numpy()
    
    data_time_list_temp = [] # List to put the new format dates
    # Assign new format to input dates
    for x in data_time_temp:
        format_date = '%Y%m%d%H%M' # txt file format date (YYYYMMDDHHMM)
        # Change format data
        objDate = datetime.strptime(str(x), format_date)
        str_dt_temp = objDate.strftime("%Y-%m-%d %H:%M") # Year(0000)-month(00)-day(00) Hour(24):Minute(00)
        # Add it to a list before defined as empty
        data_time_list_temp.append(str_dt_temp)
    
    # Create an index to manage temperature data using dates
    index_list_temp = df_temp.index 
        
    # Create a time index variable to add dates as index
    index_list_temp = pd.DatetimeIndex(data_time_list_temp) # All the dates
    
    ##################################################################################
    # Time 1
    dt1 = cal1.get_date() # get the time from the calendar
    str_dt1 = dt1.strftime("%Y-%m-%d") # format to change 
    
    # Time 2
    dt2 = cal2.get_date() # get the time from the calendar
    str_dt2 = dt2.strftime("%Y-%m-%d") # format to change 
    
    # get the time from the spinbox
    # Time 1
    h1 = hour_spinbox.get() # hour
    m1 = minute_spinbox.get() # minutes 
    s1 = "00" # seconds
    m1_aux = int(m1)

    if(m1_aux < 10):
        t1 = f"{h1}:0{m1}:{s1}"
    else:
        t1 = f"{h1}:{m1}:{s1}"
    
    # get the time from the spinbox
    # Time 2
    h2 = hour_spinbox2.get() # hour
    m2 = minute_spinbox2.get() # minute
    m2_aux = int(m2)
    
    if(m2_aux < 10):
        t2 = f"{h2}:0{m2}:{s1}"
    else:
        t2 = f"{h2}:{m2}:{s1}"
    
    # Give format to the start and end date
    time1 = str_dt1 + " " + t1
    start = pd.Timestamp(time1) # transform to timestamp type
    start_temp = index_list[0]
    
    time2 = str_dt2 + " " + t2
    end = pd.Timestamp(time2) # transform to timestamp type
    end_temp = index_list[-1]

    # just take the values from the selected dates from txt file
    # ---------------> Condition: 0: Plot all the data <--------------------------------
    condition_start_1 = index_list_temp >= start_temp
    condition_end_1 = index_list_temp <= end_temp
    only_date_1 = index_list_temp[ condition_start_1 & condition_end_1 ]
    only_temp_1 = data_temp[condition_start_1 & condition_end_1]

    # -----------------> Condition: 1: Plotting data in time interval <-----------------
    # Just select the values from the start to the end date selected
    # Dendrometer data
    condition_start = index_list >= start
    condition_end = index_list <= end
    only_date = index_list[ condition_start & condition_end ]
    only_um = data_um[condition_start & condition_end]

    # Temperature data
    condition_start_temp = index_list_temp >= start
    condition_end_temp = index_list_temp <= end
    only_date_temp = index_list_temp[ condition_start_temp & condition_end_temp ]
    only_t_temp = data_temp[condition_start_temp & condition_end_temp]

    # Radio button options
    # 0: Plot all the data 
    # 1: Plotting data in time interval
    if tipo.get() == 0:
        # csv file exported from hobo program 
        only_date = index_list
        only_um = data_um
        # txt file containing temperature values
        only_date_temp = only_date_1
        only_t_temp = only_temp_1

    if tipo.get() == 1:
        # csv file exported from hobo program 
        only_date = only_date
        only_um = only_um
        # txt file containing temperature values
        only_date_temp = only_date_temp
        only_t_temp = only_t_temp
        #Format axes (define the interval between ticks in the x-axis)
        #ax[0].xaxis.set_major_locator( mdates.HourLocator( byhour = range(0,24, 12) ) ) #24-hour time, every 12 hours
        #ax[1].xaxis.set_major_locator( mdates.HourLocator( byhour = range(0,24, 12) ) )
        #format the ticks in the x-axis to have a certain format
        #ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b/%d %H:%M'))
        #ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b/%d %H:%M'))
        
    # Create lists to add dates and micrometer data > 5000 
    greater_data_um = []
    index_g = []    
    # Put those values inside the lists defined before
    for dates, micro in zip(only_date,only_um):
        if(micro > 5000):
            index_g.append(dates)
            greater_data_um.append(micro)
    
    # Plot values > 5000 um
    ax[0].plot(index_g, greater_data_um, c = 'blue', linewidth = 0.5, label = 'micrometer')
    ax[1].plot(only_date_temp, only_t_temp, color = 'red', linewidth = 0.5, label = 'temperature')

    config_gra() # Configuration axis function
    canvas.draw() # Show plot in canvas object
    fig.savefig('graph_0.pdf') # Save the current figure into a pdf file
    
##############################################################################################
# Create a window using tkinter
window = Tk()
window.title('Dendrometer data')
window.geometry("800x700")

# Main window
main_frame = Frame(window)
main_frame.pack(fill = BOTH, expand = 1)

# Creamos una ventana para la barra
sec = Frame(main_frame)
sec.pack(fill = X, side = BOTTOM) # position of the frame

# Create a Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)

# Add Scrollbars to Canvas
# x-axis
x_scrollbar = ttk.Scrollbar(sec, orient = HORIZONTAL, command = my_canvas.xview)
x_scrollbar.pack(side = BOTTOM, fill = X) # location in the frame
# y-axis
y_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command = my_canvas.yview)
y_scrollbar.pack(side = RIGHT, fill = Y) # location in the frame

# Configure the canvas
my_canvas.configure(xscrollcommand = x_scrollbar.set)
my_canvas.configure(yscrollcommand = y_scrollbar.set)
my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion = my_canvas.bbox(ALL))) 

# Create Another Frame INSIDE the Canvas
second_frame = Frame(my_canvas)
# Add that New Frame a Window In The Canvas
my_canvas.create_window((0, 0), window = second_frame, anchor = "nw")

# Graficación
fig, ax = plt.subplots( nrows=2, ncols=1, sharex='col', figsize=(12,8) )
canvas = FigureCanvasTkAgg(fig, second_frame)
canvas.draw()
canvas.get_tk_widget().grid(column = 5, row = 20) # location in the frame

###############################################################################################
# Radio button
tipo = IntVar()

# spinbox variables
hour_string = StringVar()
min_string = tk.StringVar()
hour_string2 = tk.StringVar()
min_string2 = tk.StringVar()

# font and size
f = ("Arial", 15)

#---------------------------------------------------
# hours spinbox object
hour_spinbox = tk.Spinbox(second_frame, from_ = 0, to = 23, textvariable = hour_string, width = 4, font=f)
# minutes spinbox object
minute_spinbox = tk.Spinbox(second_frame,from_= 0, to = 59, textvariable = min_string, width = 4, font=f)
# hours spinbox object
hour_spinbox2 = tk.Spinbox(second_frame, from_ = 0, to = 23, textvariable = hour_string2, width = 4, font=f)
# minutes spinbox object
minute_spinbox2 = tk.Spinbox(second_frame,from_= 0,to = 59, textvariable = min_string2, width = 4, font=f)

# Position based on rows and columns
hour_spinbox.grid(row = 7, column = 1)
minute_spinbox.grid(row = 9, column = 1)

hour_spinbox2.grid(row = 7, column = 2)
minute_spinbox2.grid(row = 9, column = 2)

######################################## Text labels ########################################

# label
title_label = tk.Label(second_frame, text = "Open cvs file to plot", font = f)
title_label.grid(row = 1, column = 1)
# button
b1 = tk.Button(second_frame, text = 'Open file', command = read_file, font = f)
b1.grid(row = 2,column = 1)
# label
title_sel = tk.Label(second_frame, text = "Select dates to analize", font = f)
title_sel.grid(row = 3, column = 1)

# calendar objects
#cal=DateEntry(window,selectmode='day',year=2021,month=8,day=17,textvariable=sel)
cal1 = DateEntry(second_frame, selectmode = 'day', date_pattern = 'mm/dd/yy', font = f)
cal2 = DateEntry(second_frame, selectmode = 'day', date_pattern = 'MM/dd/yy', font = f)
# location of the calendar objects
cal1.grid(row = 5, column = 1)
cal2.grid(row = 5, column = 2)

# Labels
msg_display_text = tk.Label(second_frame, text = 'Time 1:', font = f)
msg_display_text2 = tk.Label(second_frame, text = 'Time 2:', font = f)
msg_display_text3 = tk.Label(second_frame, text = 'Hour 1:', font = f)
msg_display_text4 = tk.Label(second_frame, text = 'Minute 1:', font = f)
msg_display_text5 = tk.Label(second_frame, text = 'Hour 1:', font = f)
msg_display_text6 = tk.Label(second_frame, text = 'Minute 1:', font = f)
# Location of the labels
msg_display_text.grid(row = 4, column = 1)
msg_display_text2.grid(row = 4, column = 2)
msg_display_text3.grid(row = 6, column = 1)
msg_display_text4.grid(row = 8, column = 1)
msg_display_text5.grid(row = 6, column = 2)
msg_display_text6.grid(row = 8, column = 2)

# Set a default value for date
#dt1 = date(2022,4,12) # specific date Year, month , day
#cal1.set_date(dt1) 
#dt2 = date(2022,4,22) # specific date Year, month , day
#cal2.set_date(dt2)

# Radio buttons
R1 = Radiobutton(second_frame, text = "Plot all the data", variable = tipo, value = 0) 
R2 = Radiobutton(second_frame, text = "Plotting data in time interval", variable = tipo, value = 1)
R1.grid(column = 4, row = 3)
R2.grid(column = 4, row = 4)

# Button to plot
button_plot = Button(second_frame, text = "Plot graph", width = 25, command = my_upd) # call function to plot
button_plot.grid(row = 10, column = 2) # location in the frame

############################################################################################
# Define buttons to clean and close
button_clean = Button(second_frame, text = "Clear", width = 25, command = clean)
button_close = Button(second_frame, text = "Close", width = 25, command = close)

# Location buttons: clean and close
button_clean.grid(column = 1, row = 10)
button_close.grid(column = 1, row = 11)

plt.close(1) # close the first window because it's empty
window.wm_attributes("-topmost",True)
window.mainloop() # Show the main window