#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:06:16 2021

@author: phykc
"""
# Import matplotlb.pyplot
import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd

class Gantt:
    """Process a simple Gantt chart from .csv file using the Matplotlib module developed from https://www.geeksforgeeks.org/python-basic-gantt-chart-using-matplotlib/ """
    def __init__(self,filename,total_months=42, height=8, gap=1, timeunit='Months'):
        def definetasklist(self):
            tasklist=[]
            df=pd.read_csv(self.filename)
            df.dropna(subset = ['Task'], inplace=True)
            checkdf=df.isnull()
            tasks=df['Task']
            # Set up the colours to be used allows 10 personal
            colors=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray', 'tab:olive', 'tab:cyan']
            # Determine the number of tasks int he list
            number=len(tasks)
            #Loops through the dataframe
            for n in range(number):
                
                # Initalises a list of tuples for start and length of time
                a=0
                sslist=[tuple([df.loc[n,'Start'],df.loc[n,'Length']])]
                cell_test=False
                # Looks for addional start times for a task e.g. a break in the task the column positions must be the same.
                # A missing start will fail skip the other items in that task
                while cell_test==False:
                    if checkdf.iloc[n,5+a]==True:
                        cell_test=True
                    else:
                        sslist.append(tuple([df.iloc[n,5+a], df.iloc[n,6+a]]))
                        a+=2
                #Determine the colour by staff
                staffindex=int(df.loc[n,'Personal'])-1
                #Creates a formatted list to be passed through the plot
                tasklist.append([df.loc[n,'Task']+' [WP'+str(int(df.loc[n,'WP']))+']',sslist,colors[staffindex]]) 
            return tasklist
        self.filename=filename
        self.total_months=total_months
        self.height=height
        self.gap=gap
        self.tasklist=definetasklist(self)
        self.timeunit=timeunit

    def plot(self, figure_size=[5,5], gridlines=True, save=True, savename="ganttchart.png"):
        self.figure_size=figure_size
        self.gridlines=gridlines
        self.save=save
        self.savename=savename
        
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()
    
        # fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
    
        # Setting Y-axis limits
        gnt.set_ylim(len(self.tasklist)*(self.height+self.gap)+self.height+self.gap,self.height-self.gap/5)
          
        # Setting X-axis limits
        gnt.set_xlim(0,self.total_months+1)
          
        # Setting labels for x-axis and y-axis
        gnt.set_xlabel(self.timeunit)
        gnt.margins(0.6)
        # Setting ticks on y-axis and labelling tickes of y-axis
        yticks=[]
        yticklabels=[]
        for a in range(len(self.tasklist)):
            b=a*(self.height+self.gap)+self.gap+self.height*1.5
            yticks.append(b)
            yticklabels.append(self.tasklist[a][0])
            
            
        gnt.set_yticks(yticks)
        gnt.set_yticklabels(yticklabels)
        xticks = ticker.MaxNLocator(int(self.total_months/3+1))
        gnt.xaxis.set_major_locator(xticks)
    
        # Setting graph attribute
        if self.gridlines==True:
            gnt.grid(axis='x')
        else:
            gnt.grid(False)
         
        for i,task in enumerate(self.tasklist):    
        # Declaring a bar in schedule
            gnt.broken_barh(task[1], ((i+1)*(self.height+self.gap), self.height), facecolors =task[2])
    
        fig.set_size_inches(self.figure_size[0], self.figure_size[1])
        if save==True:
            plt.savefig(self.savename,bbox_inches="tight")
        plt.show()
        plt.close()
    
if __name__ == "__main__":   
    filename='tasklist.csv'
    
    gantt=Gantt(filename)
    gantt.plot([10,5])