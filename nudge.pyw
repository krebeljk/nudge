import tkinter as tk


class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title("Break")
        self.master.geometry("200x100")
        self.master.resizable(False, False)
    def create_widgets(self):
        pass
       # ...

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()