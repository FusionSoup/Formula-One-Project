import requests
import json
from tkinter import *


dsw = None
csw = None


def driver_standings_selection(event):
    global dsw, driver_list, dsw_frame
    selection = event.widget.curselection()
    if len(selection) != 1:
        return
    for slave in dsw_frame.grid_slaves():
        slave.destroy()
    driver_key = driver_list[selection[0]]['driverId']
    year = '0'
    if year == '0':
        table = requests.get("http://ergast.com/api/f1/drivers/"+driver_key+"/driverStandings.json")
        standings = json.loads(table.content)
        standings_table = standings['MRData']['StandingsTable']
        print(standings_table)
        Label(dsw_frame, text='Year').grid(row=0, column=0)
        Label(dsw_frame, text='Position').grid(row=0, column=1)
        Label(dsw_frame, text='Points').grid(row=0, column=2)
        Label(dsw_frame, text='Wins').grid(row=0, column=3)
        Label(dsw_frame, text='Constructor').grid(row=0, column=4)
        for i in range(len(standings_table['StandingsLists'])):
            sl = standings_table['StandingsLists'][i]
            print(sl['season'], sl['DriverStandings'][0]['position'], sl['DriverStandings'][0]['points'], sl['DriverStandings'][0]['wins'], sl['DriverStandings'][0]['Constructors'][0]['name'])
            Label(dsw_frame, text=sl['season']).grid(row=i + 1, column=0)
            Label(dsw_frame, text=sl['DriverStandings'][0]['position']).grid(row=i + 1, column=1)
            Label(dsw_frame, text=sl['DriverStandings'][0]['points']).grid(row=i + 1, column=2)
            Label(dsw_frame, text=sl['DriverStandings'][0]['wins']).grid(row=i + 1, column=3)
            Label(dsw_frame, text=sl['DriverStandings'][0]['Constructors'][0]['name']).grid(row=i + 1, column=4)


def circuit_selection(event):
    global csw, circuit_list, csw_frame
    selection = event.widget.curselection()
    if len(selection) != 1:
        return
    for slave in csw_frame.grid_slaves():
        slave.destroy()





        # ds = st['DriverStandings']
        #print(repr(ds))
        #for d in ds:
       #  print(d['Driver']['givenName'])


#def driver_selection(driver):
    #total points, race wins, podiums etc
    #image of driver + bio
    #twitter feed of driver account
    #driver_standings_selection(driver, year)
    #race_results_selection(driver, year)


#def race_results_selection(year, driver, circuit):

#def circuits_selection():
   # circuit = userinput(ciruit)
    #race_results_selection(0, 0, ciruit)
    #2 image of circuit
    #1 video of circuit if possible
    #twitter feed of circuit account


def get_driver_list():
    table = requests.get('http://ergast.com/api/f1/drivers.json?limit=900')
    table_content = json.loads(table.content)
    driver_temp = table_content['MRData']['DriverTable']
    return driver_temp['Drivers']


def get_circuit_list():
    table = requests.get('http://ergast.com/api/f1/circuits.json?limit=100')
    table_content = json.loads(table.content)
    print(table_content)
    circuit_temp = table_content['MRData']['CircuitTable']
    print(circuit_temp)
    return circuit_temp['Circuits']


def driver_standings_window_destroy(event):
    global dsw
    dsw = None


def driver_standings_window():
    global dsw, driver_list, dsw_frame
    if dsw:
        dsw.tkraise()
    else:
        dsw = Tk()
        dsw.title('driver standings')
        dsw.geometry('1000x600')
        dsw.bind('<Destroy>', driver_standings_window_destroy)
        driver_listbox = Listbox(dsw, width=30)
        driver_listbox.bind('<<ListboxSelect>>', driver_standings_selection)
        my_scroll = Scrollbar(dsw, command=driver_listbox.yview)
        driver_listbox.config(yscrollcommand=my_scroll.set)
        my_scroll.pack(side=LEFT, fill=Y)
        driver_listbox.pack(side=LEFT, fill=Y)
        dsw_frame = Frame(dsw,)
        dsw_frame.pack(side='right', fill='both')
        for d in driver_list:
            driver_listbox.insert('end', d['givenName'] + ' ' + d['familyName'])

def circuit_window_destroy(event):
    global csw
    csw = None

def circuit_window():
    global csw, circuit_list
    if csw:
        csw.tkraise()
    else:
        csw = Tk()
        csw.title('circuit information')
        csw.geometry('1000x600')
        csw.bind('<Destroy>', circuit_window_destroy)
        circuit_listbox = Listbox(csw, width=30)
        circuit_listbox.bind('<<ListboxSelect>>', circuit_selection)
        my_scroll2 = Scrollbar(csw, command=circuit_listbox.yview)
        circuit_listbox.config(yscrollcommand=my_scroll2.set)
        my_scroll2.pack(side=LEFT, fill=Y)
        circuit_listbox.pack(side=LEFT, fill=Y)
        csw_frame = Frame(dsw,)
        csw_frame.pack(side='right', fill='both')
        for c in circuit_list:
            circuit_listbox.insert('end', c['CircuitName'] + ' ' + c['country'])

def main_window():
    root = Tk()
    root.title('formula one')
    root.geometry('1200x900')
    my_scroll = Scrollbar(root)
    my_scroll.pack(side=RIGHT, fill=Y)
    button_frame = LabelFrame(root, height=400, width=800, bd='5')
    button_frame.pack(side='top')
    exiting = Button(button_frame, text='exit', bd='5', height=20, width=40, command=root.destroy)
    exiting.grid(row=0, column=0, pady=2)
    driver_standings = Button(button_frame, text='driver standings', bd='5', height=20, width=40, command=driver_standings_window)
    driver_standings.grid(row=0, column=1, pady=2)
    race_results = Button(button_frame, text='race results', bd='5', height=20, width=40, command=root.destroy)
    race_results.grid(row=0, column=2, pady=2)
    drivers = Button(button_frame, text='drivers', bd='5', height=20, width=40, command=root.destroy)
    drivers.grid(row=1, column=0, pady=2)
    constructors = Button(button_frame, text='constructors', bd='5', height=20, width=40, command=root.destroy)
    constructors.grid(row=1, column=1, pady=2)
    circuits = Button(button_frame, text='circuits', bd='5', height=20, width=40, command=circuit_window)
    circuits.grid(row=1, column=2, pady=2)
    root.mainloop()


get_circuit_list()

if __name__ == '__main__':
    global driver_list, circuit_list
    driver_list = get_driver_list()
    circuit_list = get_circuit_list()
    main_window()
