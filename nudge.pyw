import tkinter as tk
from datetime import datetime
import pandas as pd

SECWORK = 45 * 60 # seconds
SECSNOOZE = 5 * 60 # seconds


class TimeHandle():
    def __init__(self):
        self.t_start = datetime.now()
        self.sec_popup = SECWORK
        self.t_fmt = "%Y-%m-%d %H:%M:%S"

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

    def str_date_now(self):
        return datetime.now().strftime(self.t_fmt)

    def str_date_start(self):
        return self.t_start.strftime(self.t_fmt)



class MainApplication(tk.Frame, TimeHandle):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        TimeHandle.__init__(self)
        self.running = True
        self.configure_gui()
        self.create_widgets()

        self.loop()

    def configure_gui(self):
        self.master.title("Break")
        self.master.geometry("400x200")
        #self.master.resizable(False, False)

    def create_widgets(self):
        # text
        self.entry = tk.Entry(self.master)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.submit)

        # button submit
        b_submit = tk.Button(self.master, text = "Submit", width = 10, command = self.submit)
        b_submit.pack()

        # button snooze
        b_snoo = tk.Button(self.master, text = "Snooze", width = 10, command = self.snooze)
        b_snoo.pack()

        # label elapsed
        self.lab_count = tk.Label(self.master, width = 15)
        self.lab_count.pack()

        # label left
        self.lab_left = tk.Label(self.master, width = 15)
        self.lab_left.pack()

        # button start/stop
        self.b_startStop = tk.Button(self.master, text = "Stop", width = 10, command = self.startStop)
        self.b_startStop.pack()



        # update
        self.widgets_update()

    def reset(self):
        TimeHandle.__init__(self)


    def startStop(self):
        if self.running:
            self.running = False
            self.b_startStop.config(text="Start")
        else:
            self.running = True
            self.b_startStop.config(text="Stop")
        self.widgets_update()

    def widgets_update(self):
        el = ""
        le = ""
        if self.running:
            el = self.str_sec_elaps()
            le = self.str_sec_left()

        self.lab_count.config(text = "elapsed: " + el)
        self.lab_left.config(text = "left: " + le)


    def loop(self):
        if self.popup_due():
            self.master.deiconify() # pop-up the window
            #self.entry.focus() # commented - prevent accidental enter confirm

        self.widgets_update()


        #loop back here
        self.master.after(1000, self.loop)

    def snooze(self):
        self.sec_popup = self.sec_elaps() + SECSNOOZE
        self.widgets_update()

    def submit(self, event = None):
        if event is None: # button click
            task = self.entry.get()
        else: # enter press
            task = event.widget.get()
        self.to_xlsx(task = task)
        self.running = False
        self.widgets_update()

    def to_xlsx(self, task="aaa"):
        fxlsx = "log.xlsx"
        try:
            df = pd.read_excel(fxlsx, engine='openpyxl')
        except FileNotFoundError:
            df = pd.DataFrame(columns=["start","end","delta","task"])

        df2 = pd.DataFrame({
                'start': self.str_date_start(),
                'end': self.str_date_now(),
                'delta': self.str_sec_elaps(),
                'task': task
                }, index=[1])
        df = df.append(df2)
        with pd.ExcelWriter(fxlsx) as writer:
            df.to_excel(writer, index=False)

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()