import tkinter as tk
from datetime import datetime

SECWORK = 3 # 45 * 60 # seconds
SECNUDGE = 3 # 5 * 60 # seconds


class TimeHanle():
    def __init__(self):
        self.t_start = datetime.now()

    def sec_elaps(self):
        return (datetime.now() - self.t_start).total_seconds()



class MainApplication(tk.Frame, TimeHanle):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        TimeHanle.__init__(self)
        self.configure_gui()
        self.create_widgets()

        self.sec_popup = SECWORK


        self.loop()

    def configure_gui(self):
        self.master.title("Break")
        self.master.geometry("200x100")
        self.master.resizable(False, False)

    def create_widgets(self):
        # button snooze
        b_snoo = tk.Button(self.master, text = "Snooze", width = 10, command = self.snooze)
        b_snoo.pack()
        # button quit
        b_quit = tk.Button(self.master, text = "Quit", width = 10, command = quit)
        b_quit.pack()

    def loop(self):
        if self.sec_elaps() > self.sec_popup:
            self.master.deiconify() # pop-up the window

        #loop back here
        self.master.after(1000, self.loop)

    def snooze(self):
        self.sec_popup = self.sec_elaps() + SECNUDGE



if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()