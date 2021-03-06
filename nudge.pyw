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
        self.popped = False
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
        self.b_submit = tk.Button(self.master, text = "Submit", width = 10, command = self.submit)
        self.b_submit.pack()

        # button snooze
        self.b_snoo = tk.Button(self.master, text = "Snooze", width = 10, command = self.snooze)
        self.b_snoo.pack()

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
        self.popped = False
        self.entryClear()

    def startStop(self):
        self.reset()
        self.running = not self.running # toggle
        self.widgets_update()

    def widgets_update(self):
        self.widgets_clear()
        if self.running:
            self.b_submit.config(text = "Submit")
            self.b_submit.pack() #show
            self.b_snoo.pack() #show

            self.lab_count.config(text = "elapsed   " + self.str_sec_elaps())
            self.lab_count.pack()

            self.lab_left.config(text = "left   " + self.str_sec_left())
            self.lab_left.pack()

            self.b_startStop.config(text="Stop")
            self.b_startStop.pack()
        else:
            self.lab_count.config(text ="break")
            self.lab_count.pack()

            self.lab_left.config(text = self.str_sec_elaps())
            self.lab_left.pack()

            self.b_startStop.config(text="Start")
            self.b_startStop.pack()

            self.b_submit.config(text = "Brk sbm")
            self.b_submit.pack() #show

    def widgets_clear(self):
            self.b_submit.pack_forget()
            self.b_snoo.pack_forget()
            self.lab_count.pack_forget()
            self.lab_left.pack_forget()
            self.b_startStop.pack_forget()


    def loop(self):
        if self.popup_due() and not self.popped:
            self.master.deiconify() # pop-up the window
            self.popped = True
            #self.entry.focus() # commented - prevent accidental enter confirm

        self.widgets_update()

        #loop back here
        self.master.after(1000, self.loop)

    def snooze(self):
        if not self.running:
            return
        self.sec_popup = self.sec_elaps() + SECSNOOZE
        self.popped = False
        self.widgets_update()

    def submit(self, event = None):
        if event is None: # button click
            task = self.entry.get()
        else: # enter press
            task = event.widget.get()
            if not self.running and not task: # break mode, empty field -> ignore event
                return



        self.entryClear()

        self.to_csv(task = task)
        self.running = False
        self.reset()
        self.widgets_update()

    def entryClear(self):
        # clear entry field
        self.entry.delete(0,tk.END)
        self.entry.insert(0,"")

    def to_csv(self, task=""):
        filename = "log.csv"
        try:
            df = pd.read_csv(filename)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["start","end","delta","seconds","task"])

        df2 = pd.DataFrame({
                'start': self.str_date_start(),
                'end': self.str_date_now(),
                'delta': self.str_sec_elaps(),
                'seconds': int(round(self.sec_elaps())),
                'task': task
                }, index=[1])
        df = df.append(df2)
        df.to_csv("log.csv", index=False)

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()