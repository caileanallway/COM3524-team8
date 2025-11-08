#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 14:15:43 2018

@author: kokos
"""
# casting error corrected by GdB 18/9/2020

import sys
sys.setrecursionlimit(5000)

"Import appropriate tkinter version depending on python version"
if sys.version_info[0] < 3:
    
    import ScrolledText
    import Tkinter as tk
    from Tkinter import *
else:
    from tkinter.scrolledtext import ScrolledText
    import tkinter as tk
    from tkinter import *

# FOR PLOTS
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")



from main.Genetic_Algo import GeneticAlgo

class RedirectText(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl
 
    #----------------------------------------------------------------------
    def write(self,string):
        """"""
        self.output.insert(tk.END, string)
        self.output.update_idletasks()
        
    def flush(self):
        pass
        
        
class MyApp(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.geometry("1200x750+80+10")
        self.title("The Travelling Salesman Problem via Genetic Algorithms")
       
        
        "Title Bars"
        "input"
        self.inputtitle = Label(self, text = "Input Parameters", font = "Verdana 12 bold", anchor = "w")
        self.inputtitle.place(x = 10, y = 30)
        "iterations/fitness"
        self.iterfit = Label(self, text = "Average Fitness Value of Population at each Generation", font = "Verdana 12 bold", anchor = "w")
        self.iterfit.place(x = 500, y = 30)

        
        Label(self, text="Choose a map: ").place(x = 10, y = 60)
        "SIMPLE MAPS"
        
        
        "display prob difficulty before anything"
        
        
        def option_changed(*args):
            name = str(self.complexity.get()) 
            
            file = open("main/csv_cities/" + name + ".csv")
            
            x = []
            y = []
            for line in file:
                
                lines = line.rsplit()[0].split(",")
                
                x.append(int(float(lines[0])))
                y.append(int(float(lines[1])))
                
                print(x,y)
                
                       
            figu, ax2 = plt.subplots(1, 1)
            self.canvass = FigureCanvasTkAgg(figu, self)
            self.canvass.get_tk_widget().place(x = 502, y = 452, height = 286, width = 656)
            ax2.axis('off')
            ax2.scatter(x, y, label = "Cities")
            ax2.legend(loc="upper right", prop={'size': 8})
        
            # Create a Tkinter variable
        self.complexity = StringVar(self)
        
            # Dictionary with options
        choices = ["difficulty_5", "difficulty_10", "difficulty_15", "difficulty_20", "difficulty_25", "custom", "country_sel"]
        self.complexity.set('difficulty_10') # set the default option
        self.complexity.trace("w", option_changed)
        
        
        popupMenu = OptionMenu(self, self.complexity, *choices)
        popupMenu.configure(background = "khaki1")
        popupMenu.place(x = 300, y = 60)
            

        
        "Iterations Label & Entry Box"
        self.iterl = Label(self, text="Number of Iterations: ")
        self.iterl.place(x = 10, y = 90)
        
        it = StringVar(self, value="300")
        self.iter = tk.Entry(self, textvariable = it)
        self.iter.place(x = 300, y = 90)
        
        " Selection Drop-Down"
    
            # Create a Tkinter variable
        self.select = StringVar(self)
        
    
            # Dictionary with options
        choicess = ["Tournament_Selection", "Rank-Based_Selection", "Roulette_Selection", "Elitism_Selection"]
        self.select.set("Tournament_Selection") # set the default option
        
        popupMenuu = OptionMenu(self, self.select, *choicess, command=self.tour_size)
        popupMenuu.configure(background = "khaki1")
        Label(self, text="Selection Method: ").place(x = 10, y = 120)
        popupMenuu.place(x = 300, y = 120)
        
        #population (search space)
        self.tourl = Label(self, text="Tournament Size: ", justify = LEFT)
        self.tourl.place(x = 10, y = 150)
    
        t = StringVar(self, value="20")
        self.tour = tk.Entry(self, textvariable = t)
        self.tour.place(x = 300, y = 150) 
        
        "Population Label & Entry Box"
        self.popl = Label(self, text="Population Size (Search Space): ")
        self.popl.place(x = 10, y = 180)
        
        p = StringVar(self, value="200")
        self.pop = tk.Entry(self, textvariable = p)
        self.pop.place(x = 300, y = 180)
        
        "Selected parents Label & Entry Box"
        self.sell = Label(self, text="Mating Pool Size: ")
        self.sell.place(x = 10, y = 210)
        
        pa = StringVar(self, value="200")
        self.parent = tk.Entry(self, textvariable = pa)
        self.parent.place(x = 300, y = 210)

        "Number of Offsprings Label & Entry Box"
        self.offl = Label(self, text="New Generation Size: ")
        self.offl.place(x = 10, y = 240)
        
        of = StringVar(self, value="200")
        self.off = tk.Entry(self, textvariable = of)
        self.off.place(x = 300, y = 240)
        
        " Cross-Over Drop-Down"
            # Create a Tkinter variable
        self.crosss = StringVar(self)
 
            # Dictionary with options
        choicesss = ["one_point", "uniform", "ordered"]
        self.crosss.set('one_point') # set the default option
 
        popupMenuuu = OptionMenu(self, self.crosss, *choicesss)
        popupMenuuu.configure(background = "khaki1")
        Label(self, text="Crossover Method: ").place(x = 10, y = 270)
        popupMenuuu.place(x = 300, y = 270)
        
        "Crossover Label & Slider Box"
        self.crossl = Label(self, text="Crossover Probability: ")
        self.crossl.place(x = 10, y = 313)
        
        cr = DoubleVar()
        self.cross = Scale(self, from_=00, to=1,variable = cr, resolution=0.01, length=100, orient=HORIZONTAL)
        self.cross.set(0.5)
        self.cross.place(x = 300, y = 300)
        
        "Mutation Drop-Down"
            # Create a Tkinter variable
        self.mut_ch = StringVar(self)
 
            # Dictionary with options
        choices_mut = ["TWORS", "CIM", "RSM"]
        self.mut_ch.set('TWORS') # set the default option
 
        popupMenu_mut = OptionMenu(self, self.mut_ch, *choices_mut)
        popupMenu_mut.configure(background = "khaki1")
        Label(self, text="Mutation Method: ").place(x = 10, y = 340)
        popupMenu_mut.place(x = 300, y = 340)

        "Mutation Label & Slider Box"
        self.mutl = Label(self, text="Mutation Probability: ")
        self.mutl.place(x = 10, y = 383)
        
        var = DoubleVar()
        self.mut = Scale(self, from_=00, to=1,variable = var, resolution=0.01, length=100, orient=HORIZONTAL)
        self.mut.set(0.1)
        self.mut.place(x = 300, y = 370)
        
        "DISPLAY OUTPUT"
        if sys.version_info[0] < 3:
            self.text = ScrolledText.ScrolledText(self)
        else:
            self.text = ScrolledText(self)

        self.text.place(x = 500, y = 60, height=320, width=660)
       
               
        "Execute Button"
        close_button = tk.Button(self, text="Search", command=self.run, anchor = "e", justify = RIGHT, bg = "pale green")        
        close_button.grid(row = 0, column = 4)
                
        "Exit Button"
        exit_button = tk.Button(self, text="Exit", command=self.close, anchor = "w", bg = "tomato")        
        exit_button.grid(row = 0, column = 0)
        
        "Custom"
        custom_button = tk.Button(self, text="Custom Map", command=self.custom_map, anchor = "w", bg = "light steel blue")
        custom_button.grid(row = 0, column = 2)
        
        "World"
        custom_button = tk.Button(self, text="World Countries", command=self.world, anchor = "w", bg = "light steel blue")
        custom_button.grid(row = 0, column = 3)
        
      
        
        "PLOT TITLES & LABELS"
        self.fitlab = Label(self, text="Average Population Fitness at Each Generation Plot", font = "Verdana 11 bold")
        self.fitlab.place(x = 10, y = 415)
        
        self.fitlab = Label(self, text="Fittest Tour Plot at the End of the Search", font = "Verdana 11 bold")
        self.fitlab.place(x = 650, y = 415)
        
        self.aaa = Label(self, text = " Plot will appear here once the search has finished ", bg = "white", borderwidth = 1, relief = "sunken")
        self.aaa.place(x = 10, y = 450, height = 280, width = 460)
        
        self.aaaa = Label(self, text = " Plot will appear here once the search has finished ", bg = "white", borderwidth = 1, relief = "sunken")
        self.aaaa.place(x = 500, y = 450, height = 280, width = 660)
        
        # variable declaration
        self.iteration = ""
        self.tournament = ""
        self.population = ""
        self.parent_num = ""
        self.next_gen = ""
        
        
        " Problem difficulty default "
        file = open("main/csv_cities/difficulty_10.csv")
            
        x = []
        y = []
        for line in file:
            lines = line.rsplit()[0].split(",")
            
            x.append(int(lines[0]))
            y.append(int(lines[1]))
            
        
        figu, ax2 = plt.subplots(1, 1)
        self.canvass = FigureCanvasTkAgg(figu, self)
        self.canvass.get_tk_widget().place(x = 502, y = 452, height = 286, width = 656)
        ax2.axis('off')
        ax2.scatter(x, y, label = "Cities")
        ax2.legend(loc="upper right", prop={'size': 8})
        
        
        
    def tour_size(self,value):
        "only for Tournament selection entry"
        if value != "Tournament_Selection":
            
            #population (search space)
            self.tourl = Label(self, text="  ", justify = LEFT)
            self.tourl.place(x = 10, y = 150, width = 450, height = 30)
        
        if value == "Tournament_Selection":
            
            #population (search space)
            self.tourl = Label(self, text="Tournament Size: ", justify = LEFT)
            self.tourl.place(x = 10, y = 150)
        
            t = StringVar(self, value="20")
            self.tour = tk.Entry(self, textvariable = t)
            self.tour.place(x = 300, y = 150) 
            
        
          
        
        
    def run(self):
        
        # testing for time
        
        import time
        
        now = time.time()
        
        
        
        # delete contents of text window so that it wont congest
        self.text.delete('1.0', END)

        #EntryBoxes
        self.iteration = int(float(self.iter.get()))
        self.tournament = int(float(self.tour.get()))
        self.population = int(float(self.pop.get()))
        self.parent_num =  int(float(self.parent.get()))
        self.next_gen =  int(float(self.off.get()))
        self.cross_prob =  float(self.cross.get())
        self.mut_prob =  float(self.mut.get())
        
        #DropDowns
        self.mapp = self.complexity.get()
        self.selection = self.select.get()
        self.crosso = self.crosss.get()
        self.mut_method = self.mut_ch.get()
        
        sys.stdout = self
        
        
        def finale(mapp, iterations, selection, tournament, pop_size, parent_num, next_gen, cross, cross_prob, mutation_method, mut_prob):
            
            testing = GeneticAlgo()
            
            testing.execute(mapp,iterations,selection, tournament, pop_size, parent_num, next_gen, cross, cross_prob, mutation_method, mut_prob) 
        
            fitnesses, runs, coords, fittest_tour, fittest, time = testing.returnstuff()
            
            return fitnesses, runs, coords, fittest_tour, fittest, time
        
        
        redir = RedirectText(self.text)
        sys.stdout = redir   
        
        
        self.fitnesses, self.runs, self.coords, self.fittest_tour, self.fittest, self.time = finale(mapp = self.mapp, iterations = self.iteration, selection = self.selection, tournament = self.tournament, pop_size = self.population, parent_num = self.parent_num, next_gen=self.next_gen, cross = self.crosso, cross_prob = self.cross_prob, mutation_method = self.mut_method, mut_prob = self.mut_prob)
        
        #print(self.fittest[-1])
        
        info =  "Time elapsed : " + str(round(self.time)) + " seconds            Number of Generations : " + str(self.runs) + "               Distance of best route : " + "{:2.1f}".format(1/(self.fittest[-1]))
        
        
        self.timing = Label(self, text=info, font = "Verdana 8")
        self.timing.place(x = 500, y = 380)
        
        
        "PLOTTING"
        
        
        " plot for fitness "
              
        y_values = self.fitnesses
        y2_values = self.fittest
        x_values = list(range(0,self.runs))

        
        plt.close('all') 

        fig = plt.figure(1, figsize=(5.5,3.9))
        
        plt.cla
        plt.clf
        
        plt.plot(x_values, y_values, label = "Average population fitness")
        plt.plot(x_values, y2_values, label = "Max. population fitness")
        plt.ylabel("Fitness", fontsize = 9)
        plt.xlabel("Generations", fontsize = 9)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.legend(loc="lower right", prop={'size': 8})
        
        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().place(x = 25, y = 451, height = 274, width = 432)
        self.canvas.print_figure
        
        
        "plot of cities"
        figu, ax2 = plt.subplots(1, 1)
        self.canvass = FigureCanvasTkAgg(figu, self)
        self.canvass.get_tk_widget().place(x = 502, y = 452, height = 286, width = 656)
        
        
       
        
        ax2.axis("off")
        
        " Adding the city names "
        
        if self.mapp == "country_sel":
            temp = {}

            for name, index in self.named_city.items():
                temp[name] = self.coords[index]
    
        else:
        
            temp = self.coords
        
        city_names = []
        x_co = []
        y_co = []
        for city, coord in temp.items():
            city_names.append(city)
            x_co.append(coord[0])
            y_co.append(coord[1])
    
        ax2.axis('off')
        
        ax2.scatter(x_co, y_co, label = "Cities")
        
        
        
        for i, txt in enumerate(city_names):
            ax2.annotate(txt, (x_co[i], y_co[i]),
            horizontalalignment='left', verticalalignment='top', size = 8)
    
        
        # connecting route function
        def connection(coords, city1, city2):
            x_1, y_1 = coords[city1]
            x_2, y_2 = coords[city2]
        
            ax2.plot([x_1,x_2], [y_1, y_2], "k-")
        
        plot_tour = self.fittest_tour + [self.fittest_tour[0]]
    
        # connecting the cities
       
        for i in range(0, len(plot_tour)-1):
            connection(self.coords, plot_tour[i], plot_tour[i+1])
                

        
        
        x_s, y_s = self.coords[plot_tour[0]]
        x_f, y_f = self.coords[plot_tour[-2]]
        
        ax2.scatter(x_s, y_s, c = "g",  label = "Starting City")
        ax2.scatter(x_f, y_f, c = "r", label = "Final City")
        ax2.legend(loc="upper right", prop={'size': 8})
        figu.tight_layout()

    
    def close(self):
        self.destroy()
        
    def export(self):
        
        None
    
    " for world map "
    def world(self):
        
        windows = tk.Toplevel(self)
        windows.geometry("280x30+300+100")
        windows.title("Select Country")
        
        x = open("main/csv_cities/worldmap.csv", "r")

        y = []
        unique_countries = []
        
        checks = {}
        
        for line in x:
            
            temp = line.split("\n")[0].split(",")
            
            y.append(temp)
            
            if temp[-1] not in checks:
                
                checks[temp[-1]] = 1
                
            else:
                
                checks[temp[-1]] += 1
                
        for country, count in checks.items():
            
            if count > 2:
                
                unique_countries.append(str(country) + "_" + str(count))
        
                
                
        "Countries Drop-Down"
            # Create a Tkinter variable
        countries = StringVar(self)
        
        countries.set("Belgium_10")
        
        
        popup_countries = OptionMenu(windows, countries, *unique_countries)
        popup_countries.configure(background = "khaki1")
        popup_countries.grid(row = 0, column = 2)
        
        def select_save():
            
            country = countries.get()
            
            country = country.split("_")[0]
            
            count = open("main/csv_cities/country_sel.csv", "w")
                        
            self.named_city = {}
            
            counting = 1
            
            for line in y:
                    
                if line[-1] == country:
                                
                    coun = str(float(line[2])*100) +  "," +  str(float(line[1])*100) + "\n"
                    
                    self.named_city[line[0]] = counting
                    
                    counting += 1
                    
                    count.writelines(coun)    
                    
            x.close()
            count.close()
            
           
        
        "Save selection"
        custom_button = tk.Button(windows, text="Save Selection", command=select_save, anchor = "w", bg = "pale green")
        custom_button.grid(row = 0, column = 3)
        
        def destroy():
            windows.destroy()
        
        "Close"
        close_button = tk.Button(windows, text="Exit", command=destroy, anchor = "w", bg = "tomato")
        close_button.grid(row = 0, column = 1)
        
        
    def custom_map(self):
        
        window = tk.Toplevel(self)
        window.geometry("656x286+100+200")
        window.title("Click Coordinates")
        
        array = []
        
        
        def callback(event):
            
            array.append([event.x,-event.y])
            python_green = "#476042"
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            canvas.create_oval(x1, y1, x2, y2, fill=python_green, outline=python_green, width=10)
            

        aa = Label(window, text = " Plot will appear in this area ", bg = "white", borderwidth = 1, relief = "sunken")
        aa.place(x = 400, y = 0, width=400, height=400)
        
        canvas = Canvas(window, width=656, height=286)
        canvas.bind("<ButtonPress-1>", callback)
        canvas.update()
        
        canvas.place(x = 0, y = 0)
        
        #############################################################
        " GRID FOR CANVAS "
        # draw horizontal lines
        x1 = 0
        x2 = 656
        for k in range(0, 650, 50):
            y1 = k
            y2 = k
            canvas.create_line(x1, y1, x2, y2)
        # draw vertical lines
        y1 = 0
        y2 = 286
        for k in range(0, 650, 50):
            x1 = k
            x2 = k
            canvas.create_line(x1, y1, x2, y2)
        ###############################################################
        
        def arrray():
            import csv
        
            with open('main/csv_cities/custom.csv', 'w') as f:
                csvwriter = csv.writer(f)
                csvwriter.writerows(array)
        
                           
        def close():
            
            window.destroy()
            
                            
        write_button = tk.Button(window, text="Save Plot", command=arrray, anchor = "w", bg = "pale green")
        write_button.place(x=1, y=1)
        
        destroy_button = tk.Button(window, text="Return", command=close, anchor = "w", bg = "tomato")
        destroy_button.place(x=1, y=30)
    

            
if __name__ == '__main__':
    
    app = MyApp()
    
    result = app.mainloop()
    
    
    
    
    



