from threading import Thread
from subprocess import run
from os import getcwd
from tkinter import Tk, Label, Frame, Button, Checkbutton, StringVar, Entry, font
from tkinter.scrolledtext import ScrolledText
from time import sleep

title = 'Android Bloatware CleanUp'
appFont = ('Comic Sans MS', 15)
logs = ("Starting server",
        "Pushing extraction tool",
        "Getting packages",
        "Loading apps {}/{}...Please wait...",
        "Removing extraction tool",
        "Select apps to clean",
        "Done")

apps = {}
checkedApps = []

class Gui(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def callback(self):
        run("dependencies\\adb.exe kill-server", shell = True)
        self.window.quit()
        
    def run(self):
        ##Main Window
        self.window = Tk()
        self.window.title(title)
        self.window.protocol("WM_DELETE_WINDOW", self.callback)
        font.nametofont("TkDefaultFont").configure(family = appFont[0], size = appFont[1])

        ##Frames
        frameMain = Frame(master = self.window)
        frameMain.pack(fill = 'both', expand = 'true', padx = 10, pady = 10)
        frame1 = Frame(master = frameMain)
        frame1.pack(pady = 5)
        frame2 = Frame(master = frameMain)
        frame2.pack(pady = 5)
        frame3 = Frame(master = frameMain)
        frame3.pack(fill = 'x', pady = 5)

        ## Frame 1
        Label(master = frame1, text = 'Which apps do you want to remove?').pack(fill = 'x', expand = 'true')

        ## Frame 2
        self.scroll = ScrolledText(master = frame2, width = 50, height = 30)
        self.scroll.pack()

        ## Frame 3
        self.logLabel = Label(master = frame3, text = "Loading...")
        self.logLabel.pack(side = 'left', fill = 'x', expand = 'true')
        frameButtons = Frame(master = frame3)
        frameButtons.pack(side = 'right')
        cleanButton = Button(master = frameButtons, text = 'Clean', command = clean)
        cleanButton.pack(side = 'right')

        self.window.mainloop()

def log(msg, appIndex = None, totalApps = None):
    global gui
    if appIndex:
        gui.logLabel['text'] = logs[msg].format(appIndex, totalApps)
        return
    gui.logLabel['text'] = logs[msg]

def createSpace(name, apkName):
    global gui
    
    checkedApps.append(StringVar())
    cb = Checkbutton(master = gui.scroll, text = name, onvalue = apkName, offvalue = '', variable = checkedApps[-1], cursor = 'arrow', bg = 'white')
    gui.scroll.window_create('end', window = cb)
    gui.scroll.insert('end', '\n')

def clean():
    apkNames = checkedApps.copy()
    for i in range(len(apkNames)):
        apkNames[i] = apkNames[i].get()
    
    while '' in apkNames:
        apkNames.remove('')

    for i in apkNames:
        run("dependencies\\adb.exe shell pm uninstall --user 0 " + i, shell = True)
        log(6)

gui = Gui()
sleep(1)

# starting server
log(0)
run("dependencies\\adb.exe start-server", shell = True)

# pushing aapt tool
log(1)
run('dependencies\\adb.exe push "{}" /data/local/tmp'.format(getcwd() + "\\dependencies\\aapt-arm-pie"), shell = True)
run("dependencies\\adb.exe shell chmod 0755 /data/local/tmp/aapt-arm-pie")

# getting packages
log(2)
output = run("dependencies\\adb.exe shell pm list packages -f", shell = True, capture_output = True).stdout.decode().split()

# retrieving apps' names
totalApps = len(output)
for i in range(totalApps):
    log(3, i + 1, totalApps)
    
    ## address
    end = output[i].find(".apk")
    address = output[i][8 : end + 4]
    
    ## package
    package = output[i][end + 5:]
    
    ## name
    try:
        info = run("dependencies\\adb.exe shell /data/local/tmp/aapt-arm-pie d badging {}".format(address), shell = True, capture_output = True).stdout.decode()
        start = info.find("application-label:") + 19
        end = info.find("'", start)
        name = info[start : end]

        apps[name] = package
    except:
        pass

# removing extraction tool
log(4)
run("dependencies\\adb.exe shell rm /data/local/tmp/aapt-arm-pie", shell = True)

# adding widgets for each app
for i in apps:
    createSpace(i, apps[i])
log(5)
