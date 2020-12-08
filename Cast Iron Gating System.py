import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msg
from tkinter import Menu

class CastIron(tk.Tk):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.title('AUTOMATED GRAY CAST IRON GATING SYSTEM DESIGN')
        mb = Menu(self)  # creates menu bar
        self.config(menu=mb)
        fm = Menu(mb, tearoff=0)  # creates file menu item
        fm.add_command(label='New')
        fm.add_command(label='Clear Session', command=self._reset)
        fm.add_separator()
        mb.add_cascade(label="File", menu=fm) # adds menu item to menu
        hl = Menu(mb, tearoff=0)
        hl.add_command(label='About', command=self._showcredits)
        mb.add_cascade(label='Help', menu=hl)
        fm.add_command(label='Exit', command=self._quit)

        self.f1 = ttk.LabelFrame(self,text='Phase One: Poured Weight And Pouring Time')
        self.f1.grid(row=0,column=0, sticky="NSWE", pady=(0,0))
        self.input = ttk.LabelFrame(self.f1, text = 'Inputs')
        self.input.grid(row=0, column=0, padx=10, pady =10, sticky = 'NW')
        self.output = ttk.LabelFrame(self.f1, text='Outputs')
        self.output.grid(row=0, column=1, rowspan=1, padx=10, pady =10, sticky = 'NE')
        self.poinputs = {'Casting Weight':'kg', 'Casting Volume':'cub.mm','Casting Length':'mm','Yield':'%',
                         'Section Thickness':'mm','Fluidity Factor':'inch','Density of Solid GCI': 'kg/cub.mm', 'Density of Liquid GCI':'kg/cub.mm', 'Metal Composition':'%C:%Si:%P'}
        self.pooutputs = {'PouredWeight':'kg', 'PouringTemperature':'Celsius', 'Fluidity':'mm', 'Pouring Time':'Sec',
                          'Pouring Rate': 'kg/s'}
        self.poinput = self.create_widget(self.input,self.poinputs, input=True)
        self.pooutput = self.create_widget(self.output,self.pooutputs)
        calc = ttk.Button(self.f1, text='Calc', command=self.pouring)
        calc.grid(row=2,column=0, sticky = "NW")

        self.f2 = ttk.LabelFrame(self, text = 'Phase Two: Sprue Design')
        self.f2.grid(row=0,column=1, sticky='NSWE')
        self.input = ttk.LabelFrame(self.f2, text='Inputs')
        self.input.grid(row=0, column=0, padx=10, pady=10)
        self.output = ttk.LabelFrame(self.f2, text='Outputs')
        self.output.grid(row=0, column=1, rowspan=1, padx=10, pady=10)
        self.sprueinputs = {'Total Sprue Height':'mm','Height in Cope': 'mm', 'Height of Mould Cavity': 'mm', 'Basin Head': 'mm'}
        self.sprueoutputs = {'Sprue Effect. Height': 'mm', 'Sprue Choke Area': 'sq.mm', 'Sprue Top Area': 'sq.mm',
                            'Base Well Area': 'sq.mm', 'Choke Diameter': 'mm', 'Top Diameter': 'mm',
                             'Choke Length': 'mm', 'Top Length': 'mm'}
        self.t = ttk.LabelFrame(self.input, text="Sprue Tapering")
        self.g = ttk.LabelFrame(self.input, text="Gating")
        self.g.grid(row=0, column=0, columnspan=1, sticky='EW')
        self.t.grid(row=0, column=1, sticky='WE')
        self.lf= ttk.LabelFrame(self.input)
        self.lf.grid(row=0,column=2,sticky='WE')
        self.cfd = ttk.Label(self.lf, text='Efficiency Factor').grid(row=0, column=0, sticky='NS')
        self.cf = tk.Spinbox(self.lf, textvar=tk.DoubleVar(), from_=0.7, to=0.9, increment=0.01, state='readonly',
                             bd=5, width=4)
        self.cf.grid(row=1, column=0,sticky="WE")
        self.gt = tk.IntVar()
        self.st = tk.IntVar()
        self.to = ttk.Radiobutton(self.g, text='Top', value=1, variable=self.gt,state='active',command=self.cc).grid(row=0, column=0, sticky='WE')
        self.pt = ttk.Radiobutton(self.g, text='Parting', value=2, variable=self.gt,command=self.cc).grid(row=1, column=0, sticky='WE')
        self.bo = ttk.Radiobutton(self.g, text='Bottom', value=3, variable=self.gt,command=self.cc).grid(row=2, column=0, sticky='WE')
        self.tc = ttk.Radiobutton(self.t, text='Circular', value=2, variable=self.st).grid(row=0, column=0, sticky='WE')
        self.ts = ttk.Radiobutton(self.t, text='Square',value=1,variable=self.st).grid(row=2, column=0, sticky='WE')
        self.sinputs = self.create_widget(self.input, self.sprueinputs, x=1, input=True)
        self.soutputs = self.create_widget(self.output, self.sprueoutputs)
        self.calc2 = ttk.Button(self.f2, text='Calc', command=self.spruedesign, state='disabled')
        self.calc2.grid(row=1, column=1, sticky='NE')

        self.f3 = ttk.LabelFrame(self, text='Phase Three: Ingate and Pouring Basin Design')
        self.f3.grid(row=1, column=0, sticky='NSWE')
        self.input = ttk.LabelFrame(self.f3, text='Inputs')
        self.input.grid(row=0, column=0, padx=10, pady=10)
        self.output = ttk.LabelFrame(self.f3, text='Outputs')
        self.output.grid(row=0, column=1, rowspan=1, padx=10, pady=10)
        self.gateinputs = {'Number of Ingates':'', 'Aspect Ratio(H:W)':'', 'Gating Ratio(S:R:I)':''}
        self.gateoutputs = {'Basin Depth': 'mm', 'Ingate Area': 'sq.mm', 'Ingate Height': 'mm', 'Ingate Width': 'mm'}
        self.ginputs = self.create_widget(self.input, self.gateinputs, input=True)
        self.goutputs = self.create_widget(self.output, self.gateoutputs)
        self.calc3 = ttk.Button(self.f3, text='Calc', state='disabled', command=self.ingatedesign)
        self.calc3.grid(row=1, column=0, sticky='SW')

        self.f4 = ttk.LabelFrame(self, text='Phase Four: Runner Design')
        self.f4.grid(row=1, column=1, sticky="NSWE", pady=(0, 0))
        self.input = ttk.LabelFrame(self.f4, text='Inputs')
        self.input.grid(row=0, column=0, padx=10, pady=10, sticky='SW')
        self.output = ttk.LabelFrame(self.f4, text='Outputs')
        self.output.grid(row=0, column=1, rowspan=1, padx=(10,0), pady=10, sticky='SE')
        self.runnerinputs = {'Number of Runners': '', 'Aspect Ratio (H:W)': ''}
        self.runneroutputs = {'Runner Area': 'sq.mm', 'Runner Height': 'mm', 'Runner Width': 'mm'}
        self.rinputs = self.create_widget(self.input, self.runnerinputs, input=True)
        self.routputs = self.create_widget(self.output, self.runneroutputs)
        self.calc4 = ttk.Button(self.f4, text='Calc', state='disabled', command=self.runnerdesign)
        self.calc4.grid(row=1, column=1, sticky='SE')

    def create_widget(self,container, inputs, x=0, y=0, widgets={},input=False):
        for i in inputs:
            l = ttk.Label(container, text=i)
            l.grid(row=x, column=y, padx=(0, 5), sticky='NW')
            y += 1
            widgets[i] = tk.Entry(container, textvar=tk.StringVar())
            widgets[i].grid(row=x, column=y)
            if i == 'Metal Composition':
                widgets[i].config(bg='azure', textvar=tk.StringVar())
                widgets[i].insert(1,'3.4:2.4:0.6')
            y += 1
            if i in ['Casting Weight', 'Casting Volume', 'Yield', 'Section Thickness','Fluidity Factor',
                     'Number of Runners', 'Aspect Ratio (H:W)', 'Number of Ingates','Aspect Ratio(H:W)','Gating Ratio(S:R:I)','Total Sprue Height','Basin Head']:
                widgets[i].config(bg='orange')
            if input and i != 'Metal Composition':
                widgets[i].config(textvar=tk.StringVar)
                widgets[i].insert(1,'0')
            if inputs[i] != '':
                b = ttk.Label(container, text=inputs[i])
                b.grid(row=x, column=y, sticky='WE')
            x += 1
            y = 0
        return widgets

    def _quit(self):
        if msg.askyesnocancel('Exit', 'Do You Really Want to Exit'):
            self.quit()
            self.destroy()
            exit()
        else:
            pass

    def _showcredits(self):
        msg.showinfo('', 'Coded by Ichinga Samuel Chukwudike')

    def cc(self):
        self.sprueinputs = {'Total Sprue Height':'mm','Height in Cope': 'mm', 'Height of Mould Cavity': 'mm', 'Basin Head': 'mm'}
        if self.gt.get() == 2:
            self.sinputs['Height in Cope'].config(bg='orange')
            self.sinputs['Height of Mould Cavity'].config(bg='orange')
        elif self.gt.get() == 3:
            self.sinputs['Height of Mould Cavity'].config(bg='orange')
            self.sinputs['Height in Cope'].config(bg='white')
        elif self.gt.get() ==1:
            self.sinputs['Height of Mould Cavity'].config(bg='white')
            self.sinputs['Height in Cope'].config(bg='white')
    def _calctemp(self,ti):
        thick2temp = {4: 1405, 8: 1385, 15: 1360, 30: 1340, 75: 1295, 125: 1265, 150: 1240}
        if ti < 4:
            t = 4
        elif 4 < ti <= 10:
            t = 8
        elif 10 < ti < 20:
            t = 15
        elif 20 <= ti < 50:
            t = 30
        elif 50 <= ti < 100:
            t = 75
        elif 100 <= ti < 150:
            t = 125
        elif ti >= 150:
            t = 150
        return thick2temp[t]

    def pouring(self):
        ds = 7.2e-6
        dl = 6.09e-6
        w, vc, self.cl, y, st, ff, dns, dnl = [float(self.poinput[i].get()) for i in self.poinputs if i!='Metal Composition']
        ff = ff/40
        dns = dns or ds
        self.dnl = dnl or dl
        PT = self._calctemp(st)
        mtc = self.poinput['Metal Composition'].get()
        k1 = mtc.split(':')
        c, si, ph = [float(i) for i in k1]
        cf = c + (0.25 * si) + (0.5 * ph)
        k = 37.846 * cf + 0.228 * PT - 389.6
        W = w or (dns * vc)

        # Lambda Function to Calculate Fluidity When Weigth is Less Than 450
        w1 = lambda k,st,W: (k * (1.41 + (st / 14.59))) * W**0.5

        # Lambda Function to Calculate Fluidity When Weigth is Greater Than 450
        w2 = lambda k,st,W: (k * (1.236 + (st / 16.65))) * W**(1/3)

        self.Wp = W / (y / 100)
        if W < 450:
            self.t = w1(ff,st,self.Wp)
        elif W >= 450:
            self.t = w2(ff,st,self.Wp)
        Pr = W / self.t
        [self.pooutput[i].insert(1,round(j,4)) for i,j in zip(self.pooutputs,(self.Wp, PT, k, self.t, Pr))]
        self.calc2.configure(state='enabled')

    def spruedesign(self):
        sh, p, c, bh = [float(self.sinputs[i].get()) for i in self.sprueinputs]
        if self.gt.get() == 1:
            self.esh = sh
        elif self.gt.get() == 2:
            self.esh = sh - (p**2 / (2 * c))
        elif self.gt.get() == 3:
            self.esh = sh - (c / 2)

        cf = float(self.cf.get()) or 0.8
        self.AC = self.Wp / ((cf * self.dnl * self.t) * (2 * 9810 * self.esh)**0.5)
        dia = lambda ar: ((ar/3.142) ** 0.5) * 2
        wid = lambda ar: ar**0.5
        self.bwa = self.AC * 5
        self.dbw = dia(self.bwa)
        self.at = self.AC * ((self.esh + bh / bh) ** 0.5)
        if self.st.get() == 1:
            self.tl = wid(self.at)
            self.cl = wid(self.AC)
            self.dic = 0
            self.dat = 0
        elif self.st.get() == 2:
            self.dic = dia(self.AC)
            self.dat = dia(self.at)
            self.cl = 0
            self.tl = 0
        [self.soutputs[i].insert(1, round(j,4)) for i, j in zip(self.sprueoutputs, (self.esh, self.AC, self.at, self.bwa, self.dic, self.dat, self.cl, self.tl))]
        self.calc3.configure(state='enabled')

    def ingatedesign(self):
        ng, ar, gr = [self.ginputs[i].get() for i in self.gateinputs]
        self.ac, self.ar, self.ag = [float(i) for i in gr.split(':')]
        h, w = [float(i) for i in ar.split(':')]
        self.AG = (self.ag / self.ac) * self.AC
        ng = float(ng)
        bd = 2.5 * (self.dat or self.tl)
        c = w / h
        h = (self.AG / (ng * c))**0.5
        w = c * h
        [self.goutputs[i].insert(1, round(j, 4)) for i, j in zip(self.gateoutputs, (bd, self.AG, h, w))]
        self.calc4.configure(state='enabled')

    def runnerdesign(self):
        nr, ar= [self.rinputs[i].get() for i in self.runnerinputs]
        self.AR = (self.ar / self.ac) * self.AC
        h, w = [float(i) for i in ar.split(':')]
        c = w / h
        h = (self.AR / (float(nr) * c)) ** 0.5
        w = c * h
        [self.routputs[i].insert(1, round(j, 4)) for i, j in zip(self.runneroutputs, (self.AR, h, w))]

    def _reset(self):
        [self.pooutput[i].delete(0,'end') for i in self.pooutputs]
        [self.soutputs[i].delete(0,'end') for i in self.sprueoutputs]
        [self.goutputs[i].delete(0,'end') for i in self.gateoutputs]
        [self.routputs[i].delete(0,'end') for i in self.runneroutputs]


CastIron().mainloop()