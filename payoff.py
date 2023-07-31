import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Home(tk.Tk):

    bg = 'white'
    fg = 'blue'

    hold_options = []

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Options Payoff Diagram GUI')
        self.geometry('900x650')
        self.configure(bg=self.bg)
        
        plot_frame = tk.Frame(self, bg=self.bg)
        plot_frame.pack(side=tk.TOP)
        self.plotFrame(plot_frame)

        ctrl_frame = tk.Frame(self, bg=self.bg)
        ctrl_frame.pack(side=tk.TOP)
        self.controlFrame(ctrl_frame)

    def controlFrame(self, frame):

        def add_option():
            strike = float(self.options_info['Strike'].get())
            premium = float(self.options_info['Premium'].get())
            optype = self.options_info['Type'].get()
            side = self.options_info['Side'].get()

            self.hold_options.append([strike, premium, optype, side])

            options = '\n'.join([','.join([j if type(j) == str else str(j) for j in i]) for i in self.hold_options])

            msg = 'Selected Options\n{}'.format(options)

            self.see_options.configure(text=msg)
            self.update_idletasks()

        def calculate():
            
            def cs(a, b):
                return max(a - b, 0)
            
            stock_price = float(self.stock_info['StockPrice'].get())
            stock_range = int(self.stock_info['StockRange'].get())
            stock_delta = float(self.stock_info['StockDelta'].get())

            top = [stock_price + i*stock_delta for i in range(stock_range)]
            bot = [stock_price - i*stock_delta for i in range(stock_range)]

            line = bot[::-1][:-1] + top

            payoff = []
            cost = 0
            c_side = 0
            for (strike, premium, optype, side) in self.hold_options:
                if side == 'buy':
                    c_side = 1
                else:
                    c_side = -1
                xxx = [c_side*cs(price, strike) if optype == 'call' else c_side*cs(strike, price) for price in line]
                payoff.append(xxx)
                cost += -premium if side == 'buy' else premium

            XXX = np.array(payoff).T
            YYY = [float(np.sum(i)) for i in XXX]
            

            self.plot.cla()
            self.plot.set_title('Payoff Diagram', color=self.fg)
            self.plot.plot(line, YYY, color='green')
            self.canvas.draw()

        def clear():
            self.hold_options.clear()
            self.see_options.configure(text='...')
            self.plot.cla()
            self.canvas.draw()
            self.update_idletasks()

        
        tk.Label(frame, text='\t', bg=self.bg, fg=self.fg).grid(row=1, column=1)
        self.stock_info = {}
        self.options_info = {}
        stock_info = ('StockPrice','StockRange','StockDelta')
        for i, j in enumerate(stock_info):
            tk.Label(frame, text=j, bg=self.bg, fg=self.fg).grid(row=1, column=i+1)
            self.stock_info[j] = ttk.Entry(frame, justify='center', width=10)
            self.stock_info[j].grid(row=2, column=i+1)
        
        options_info = ('Strike','Premium','Type','Side')
        for i, j in enumerate(options_info):
            tk.Label(frame, text=j, bg=self.bg, fg=self.fg).grid(row=3, column=i+1)
            self.options_info[j] = ttk.Entry(frame, justify='center', width=10)
            self.options_info[j].grid(row=4, column=i+1)

        tk.Label(frame, text='\t', bg=self.bg, fg=self.fg).grid(row=5, column=1)
        tk.Button(frame, text='Add Option', command=lambda: add_option()).grid(row=6, column=1)
        tk.Button(frame, text='Calculate', command=lambda: calculate()).grid(row=6, column=2)
        tk.Button(frame, text='Clear Options', command=lambda: clear()).grid(row=6, column=3)
        
        self.see_options = tk.Label(frame, text='...', bg=self.bg, fg=self.fg)
        self.see_options.grid(row=7, column=2)

        

    def plotFrame(self, frame):
        fig = Figure(figsize=(8, 3))
        self.plot = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP)







Home().mainloop()
