import tkinter as tk
from datetime import datetime

SECWORK = 3 # 45 * 60 # seconds
SECNUDGE = 3 # 5 * 60 # seconds


class TimeHanle():
    def __init__(self):
        self.t_start = datetime.now()
        self.sec_popup = SECWORK

    def sec_elaps(self):
        return (datetime.now() - self.t_start).total_seconds()

    def str_sec_elaps(self):
        return self.sec_format(self.sec_elaps())

    def str_sec_left(self):
        return self.sec_format(self.sec_popup - self.sec_elaps())

    def popup_due(self):
        if self.sec_elaps() > self.sec_popup:
            return True
        else:
            return False

    def sec_format(self, sec):
        sign = ""
        if sec < 0:
            sign = "-"
            sec = -sec
        return sign+'{:02.0f}:{:02.0f}:{:02.0f}'.format(sec // 3600, sec % 3600 // 60, sec % 60)



class MainApplication(tk.Frame, TimeHanle):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        TimeHanle.__init__(self)
        self.configure_gui()
        self.create_widgets()



        self.loop()

    def configure_gui(self):
        self.master.title("Break")
        self.master.geometry("200x100")
        self.master.resizable(False, False)

    def create_widgets(self):
        # button snooze
        b_snoo = tk.Button(self.master, text = "Snooze", width = 10, command = self.snooze)
        b_snoo.pack()

        # label elapsed
        self.lab_count = tk.Label(self.master, width = 15)
        self.lab_count.pack()

        # label left
        self.lab_left = tk.Label(self.master, width = 15)
        self.lab_left.pack()

        # button quit
        b_quit = tk.Button(self.master, text = "Quit", width = 10, command = quit)
        b_quit.pack()

        # update
        self.widgets_update()

    def widgets_update(self):
        self.lab_count.config(text = "elapsed: " + self.str_sec_elaps())
        self.lab_left.config(text = "left: " + self.str_sec_left())

    def loop(self):
        if self.popup_due():
            self.master.deiconify() # pop-up the window

        self.widgets_update()

        #loop back here
        self.master.after(1000, self.loop)

    def snooze(self):
        self.sec_popup = self.sec_elaps() + SECNUDGE



if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()