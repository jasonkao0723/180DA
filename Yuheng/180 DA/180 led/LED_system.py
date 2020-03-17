from tkinter import*
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import arrange
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.animation as animation 


LARGE_FONT= ("Verdana", 12)

######################################################################
############################# functions ##############################
######################################################################


def tran(self, obj_):
    "plot the sub figure inside the function"
    shape = obj_
    m = shape.sh_trans(arrange.n,arrange.d,arrange.crl)

    f = Figure(figsize=(5,5), dpi=100)
    sub = f.add_subplot(111)

    sub.matshow(m, cmap=plt.cm.Blues)

    for i in range(arrange.n):
        for j in range(arrange.d):
            c = m[i][j]
            sub.text(j, i, str(c), va='center', ha='center')

    plt.show()

    canvas = FigureCanvasTkAgg(f, self)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



######################################################################
############################### classes ##############################
######################################################################


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "LED Matrix Management System")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, edge_Page, random_Page, 
                    u_tri_Page,l_tri_Page, letter_U_Page,
                    letter_C_Page, letter_L_Page, cross_up_Page,
                    cross_down_Page, letter_A_Page, letter_E_Page,
                    heart_Page, tree_Page, letter_I_Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Matrix Arrangement", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label.config(background='Dark gray')
    
        ttk.Label(self, text="Number of Rows: " + str(arrange.n)).pack(pady=10,padx=10)
        
        ttk.Label(self, text="Number of Columns: " +str(arrange.d)).pack(pady=10,padx=10)

        button = ttk.Button(self, text="Edge light",
                            command=lambda: controller.show_frame(edge_Page))
        button.pack()

        button2 = ttk.Button(self, text="random shape",
                            command=lambda: controller.show_frame(random_Page))
        button2.pack()

        button3 = ttk.Button(self, text="upper triangular",
                            command=lambda: controller.show_frame(u_tri_Page))
        button3.pack()

        button4 = ttk.Button(self, text="lower triangular",
                            command=lambda: controller.show_frame(l_tri_Page))
        button4.pack()

        button6 = ttk.Button(self, text="cross up shape",
                            command=lambda: controller.show_frame(cross_up_Page))
        button6.pack()

        button7 = ttk.Button(self, text="cross down shape",
                            command=lambda: controller.show_frame(cross_down_Page))
        button7.pack()

        button12 = ttk.Button(self, text="letter I shape",
                            command=lambda: controller.show_frame(letter_I_Page))
        button12.pack()

        button5 = ttk.Button(self, text="letter U shape",
                            command=lambda: controller.show_frame(letter_U_Page))
        button5.pack()

        button5 = ttk.Button(self, text="letter C shape",
                            command=lambda: controller.show_frame(letter_C_Page))
        button5.pack()

        button5 = ttk.Button(self, text="letter L shape",
                            command=lambda: controller.show_frame(letter_L_Page))
        button5.pack()

        button8 = ttk.Button(self, text="letter A shape",
                            command=lambda: controller.show_frame(letter_A_Page))
        button8.pack()

        button9 = ttk.Button(self, text="letter E shape",
                            command=lambda: controller.show_frame(letter_E_Page))
        button9.pack()

        button10 = ttk.Button(self, text="heart shape",
                            command=lambda: controller.show_frame(heart_Page))
        button10.pack()

        button11 = ttk.Button(self, text="Arrow shape",
                            command=lambda: controller.show_frame(tree_Page))
        button11.pack()

       
class edge_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Edge light", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # plot the sub figure inside the function
        tran(self, arrange.edge())


class random_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="random shape", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        # plot the sub figure inside the function
        tran(self, arrange.random_shape())


class u_tri_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="upper triangular shape", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        # plot the sub figure inside the function
        tran(self, arrange.u_tri())


class l_tri_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="lower triangular shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # plot the sub figure inside the function
        tran(self, arrange.l_tri())
    

class letter_U_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Letter U shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # plot the sub figure inside the function
        tran(self, arrange.letter_U())

class letter_C_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Letter C shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.letter_C())

class letter_L_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Letter L shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.letter_L())


class cross_up_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Cross up shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.cross_up())  

class cross_down_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Cross up shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.cross_down())


class letter_A_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Letter A shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.letter_A())    




class letter_E_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Letter E shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.letter_E()) 



class heart_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="heart shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.heart_()) 


class tree_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Arrow shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.tree()) 

class letter_I_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Letter I shape", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

         # plot the sub figure inside the function
        tran(self, arrange.letter_I()) 

app = SeaofBTCapp()
app.mainloop()
        