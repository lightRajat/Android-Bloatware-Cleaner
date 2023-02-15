import subprocess as sp
from os import getcwd

sp.run("adb.exe start-server", shell = True)
class CleanUp():

    title = 'Android Bloatware CleanUp'
    font = ('Comic Sans MS', 15)
    apps = {}
    path = 'apps.csv'

    def __init__(self):
        self.selApps = []
        self.retrieveApps()
        self.main()

    def retrieveApps(self):
        def run(command):
            return check_output(command).decode()
        sp.run('adb.exe push "{}" /data/local/tmp'.format(getcwd() + "\\aapt-arm-pie"), shell = True)
        sp.run("adb.exe shell chmod 0755 /data/local/tmp/aapt-arm-pie")
        
        output = sp.run("adb.exe shell pm list packages -f", shell = True, capture_output = True).stdout.decode().split()
        for i in output:
            #address
            end = i.find(".apk")
            address = i[8 : end + 4]
            #package
            package = i[end + 5:]
            #name
            try:
                info = sp.run("adb.exe shell /data/local/tmp/aapt-arm-pie d badging {}".format(address), shell = True, capture_output = True).stdout.decode()
                start = info.find("application-label:") + 19
                end = info.find("'", start)
                name = info[start : end]

                self.apps[name] = package
            except:
                pass
            
        sp.run("adb.exe shell rm /data/local/tmp/aapt-arm-pie", shell = True)

    def main(self):

        def clean():
            apkNames = self.selApps.copy()
            for i in range(len(apkNames)):
                apkNames[i] = apkNames[i].get()
            
            while '' in apkNames:
                apkNames.remove('')

            for i in apkNames:
                sp.run("adb.exe shell pm uninstall --user 0 " + i, shell = True)
                logLabel.config(text = "Done")

        def createSpace(name, apkName):
            self.selApps.append(StringVar())
            cb = Checkbutton(master = scroll, text = name, onvalue = apkName, offvalue = '', variable = self.selApps[-1], font = self.font, bg = 'white', anchor = 'w', cursor = 'arrow')
            scroll.window_create('end', window = cb)
            scroll.insert('end', '\n')

        ##GUI Design
        from tkinter import Tk, Label, Frame, Button, Checkbutton, StringVar, Entry
        from tkinter.scrolledtext import ScrolledText

        ##Main Window
        window = Tk()
        window.title(self.title)

        ##Frames
        frameMain = Frame(master = window)
        frameMain.pack(fill = 'both', expand = 'true', padx = 10, pady = 10)
        frame1 = Frame(master = frameMain)
        frame1.pack(pady = 5)
        frame2 = Frame(master = frameMain)
        frame2.pack(pady = 5)
        frame3 = Frame(master = frameMain)
        frame3.pack(fill = 'x', pady = 5)
        
        ## Frame 1
        qLabel = Label(master = frame1, text = 'Which apps do you want to remove?', font = self.font)
        qLabel.pack(fill = 'x', expand = 'true')

        ## Frame 2
        scroll = ScrolledText(master = frame2, width = 50, height = 30)
        scroll.pack()
        for i in self.apps:
            createSpace(i, self.apps[i])

        ## Frame 3
        logLabel = Label(master = frame3, text = '--Status--', font = self.font)
        logLabel.pack(side = 'left', fill = 'x', expand = 'true')
        frameButtons = Frame(master = frame3)
        frameButtons.pack(side = 'right')
        cleanButton = Button(master = frameButtons, text = 'Clean', command = clean, font = self.font)
        cleanButton.pack(side = 'right')

        window.mainloop()

CleanUp()
sp.run("adb.exe kill-server", shell = True)
