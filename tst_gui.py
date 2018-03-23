from tkinter import *
from tkinter import ttk

class gui_chat_p2p:

    root = Tk()
    content = ttk.Frame(root, relief="sunken")
    frame = ttk.Frame(content, width=700, height=800)
    connect = ttk.Label(content, text="connexion au server")
    rubric_connect = ttk.Frame(root)
    v_host = ttk.Entry(content)
    ehost = ttk.Entry(rubric_connect, textvariable=v_host)

    ok = ttk.Button(content, text="Okay")
    # cancel = ttk.Button(content, text="Cancel")
    frame.grid(column="-2", row=0)
    content.grid(column=0, row=0)
    connect.grid(column=0, row=0, columnspan=1)
    # name.grid(column=3, row=1, columnspan=2)

    ok.grid(column=3, row=0)
    # cancel.grid(column=4, row=3)
    def __init__(self):
        self.root.mainloop()


gui_chat_p2p()
