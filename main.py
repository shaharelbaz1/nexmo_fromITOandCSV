from Tkinter import *
import Tkinter as tk
from PIL import ImageTk, Image
import main_fromITO_longSuffix
import main_fromITO_shortSuffix
import main_fromCSV
import main_fromITO_REST
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
   global list, ents
   printToXml=False
   IsExportObj=False
   root = Tk()

   root.wm_title("Mobile Tornado v0.1")
   root.iconbitmap(resource_path("images\MobilTornado_splash_image_icon.ico"))

   mainframe = Frame(root)
   mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
   mainframe.columnconfigure(0, weight=1)
   mainframe.rowconfigure(0, weight=1)
   mainframe.pack(pady=50, padx=50)

   path = resource_path("images\MobilTornado_splash_image.png")
   img = ImageTk.PhotoImage(Image.open(path))
   panel = tk.Label(mainframe,  image=img)

   panel.pack(side="top", fill="both", expand="yes")

   b_choose = Button(root, text='ITO', height=3, width=15, bg="turquoise", command=lambda: main_fromITO_REST.main(root))
   b_choose.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   b_choose = Button(root, text='CSV', height=3, width=15, bg="turquoise", command=lambda: main_fromCSV.main(root))
   b_choose.pack(side="left", padx=5, pady=5, fill="none", expand=True)

   b_exit = Button(root, text='Quit', height=3, width=15, bg="turquoise", command=lambda:root.destroy())
   b_exit.pack(side="left", padx=5, pady=5, fill="none", expand=True)



   root.mainloop()