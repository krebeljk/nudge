import tkinter as tk
from datetime import datetime

TIMEWORK = 3 # 45 * 60 # seconds
TIMENUDGE = 3 # 5 * 60 # seconds


class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

        self.t_start = datetime.now()

        self.loop()

    def configure_gui(self):
        self.master.title("Break")
        self.master.geometry("200x100")
        self.master.resizable(False, False)

    def create_widgets(self):
        b_quit = tk.Button(self.master, text = "Quit", width = 10, command = quit)
        b_quit.pack()

    def loop(self):
        sec_elaps = (datetime.now() - self.t_start).total_seconds()
        if sec_elaps > TIMEWORK:
            self.master.deiconify() # pop-up the window

        #loop back
        self.master.after(1000, self.loop)


if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()