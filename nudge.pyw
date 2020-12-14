import tkinter as tk
from datetime import datetime

SECWORK = 3 # 45 * 60 # seconds
SECNUDGE = 3 # 5 * 60 # seconds


class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

        self.sec_popup = SECWORK
        self.t_start = datetime.now()

        self.loop()

    def configure_gui(self):
        self.master.title("Break")
        self.master.geometry("200x100")
        self.master.resizable(False, False)

    def create_widgets(self):
        b_quit = tk.Button(self.master, text = "Quit", width = 10, command = quit)
        b_quit.pack()
        b_snoo = tk.Button(self.master, text = "Snooze", width = 10, command = self.snooze)
        b_snoo.pack()

    def loop(self):
        if self.sec_elaps() > self.sec_popup:
            self.master.deiconify() # pop-up the window

        #loop back here
        self.master.after(1000, self.loop)

    def snooze(self):
        self.sec_popup = self.sec_elaps() + SECNUDGE

        #loop back
        self.master.after(1000, self.loop)

    def sec_elaps(self):
        return (datetime.now() - self.t_start).total_seconds()



if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()