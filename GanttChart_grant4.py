#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:06:16 2021

@author: phykc
"""
import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd

#Create a class that hold the data for the gantt chart in pandas
class Gantt:
    """Process a  Gantt chart from .csv file using the Matplotlib module. Use the template csv to create data and save in the same directory as the .py file"""
    def __init__(self,filename,total_months=42, height=8, gap=1, timeunit='Month', WP=True):
        
        self.filename=filename
        self.total_months=total_months
        self.height=height
        self.gap=gap
        self.timeunit=timeunit
        self.WP=WP
        self.definetasklist()
        self.milestoneindex=[]
        self.milestonelist=[]
        self.deliverableindex=[]
        self.deliverablelist=[]
        
    def definetasklist(self):
        #Read the file into the df - the csv file example is the template required
        self.df=pd.read_csv(self.filename,dtype={'Task': 'str','WP': 'str'})
        #Create a dataframe to test the boundaries of the data, allows skipped task lines
        self.checkdf=self.df.isnull()
        tasks=self.df['Task']
        self.tasklist=[]
        # Set up the colours to be used allows 50 personnel but only 10 colors
        colors=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray', 'tab:olive', 'tab:cyan']*10
        textcolors=['tab:blue','tab:green','tab:red','tab:purple','tab:brown','tab:gray', 'tab:olive', 'tab:cyan']*10
        people=self.df['Personnel'].tolist()
        people = list(dict.fromkeys(people))
        wp_lab=self.df['WP'].tolist()
        wp_lab=list(dict.fromkeys(wp_lab))
        self.milestonemonths=self.df[['Milestone','M Month']]
        self.milestonemonths=self.milestonemonths.sort_values(by=['M Month'])
        self.milestonemonths.insert(0, 'New_ID', range(1,len(self.milestonemonths)+1))
        self.delivermonths=self.df[['Deliverable','D Month']]
        self.delivermonths=self.delivermonths.sort_values(by=['D Month'])
        self.delivermonths.insert(0, 'New_ID', range(1,len(self.delivermonths)+1))
        #Loops through the dataframe
        for n in self.df.index:
            if self.checkdf.loc[n,'Task']==False:
                # Initalises a list of tuples for start and length of time
                a=0
                sslist=[tuple([self.df.loc[n,'Start'],self.df.loc[n,'Length']])]
                cell_test=False
                # Looks for addional start times for a task e.g. a break in the task the column positions must be the same.
                # A missing 'start' will cause an error
                while cell_test==False:
                    if self.checkdf.iloc[n,5+a]==True:
                        cell_test=True
                    else:
                        sslist.append(tuple([self.df.iloc[n,5+a], self.df.iloc[n,6+a]]))
                        a+=2
                #Determine the personnel
                staffindex=people.index(self.df.loc[n,'Personnel'])
                wpindex=wp_lab.index(self.df.loc[n,'WP'])
                #Creates a formatted list to be passed through the plot
                if self.WP==True:
                    self.tasklist.append([self.df.loc[n,'Task']+ ' [WP'+str((self.df.loc[n,'WP']))+']',sslist,colors[staffindex],self.df.loc[n,'Personnel']]) 
                else:
                    self.tasklist.append([self.df.loc[n,'Task'],sslist,colors[staffindex],self.df.loc[n,'Personnel']]) 
                
    def milestone(self,i):
        if self.checkdf.loc[i,'M Month']==False and self.MS==True:
            NewID=self.milestonemonths.loc[i,'New_ID']
            plt.scatter(self.df.loc[i,'M Month'], (i+1)*(self.height+self.gap)+self.height*0.5, marker='*',s=self.MSmarker, c='black')
            plt.text(self.df.loc[i,'M Month']+0.5,(i+1)*(self.height+self.gap)+self.height*0.75, s='MS'+str(NewID))
            self.milestoneindex.append('MS' +str(NewID))
            self.milestonelist.append(self.df.loc[i,'Milestone'])
            
    def deliverable(self,i):
         if self.checkdf.loc[i,'D Month']==False and self.D==True:
             NewID=self.delivermonths.loc[i,'New_ID']
             plt.scatter(self.df.loc[i,'D Month'], (i+1)*(self.height+self.gap)+self.height*0.5, marker='^',s=self.Dmarker, c='black')
             plt.text(self.df.loc[i,'D Month']+0.5,(i+1)*(self.height+self.gap)+self.height*0.75, s='D'+str(NewID))
             self.deliverableindex.append('D' +str(NewID))
             self.deliverablelist.append(self.df.loc[i,'Deliverable'])
              
    def plot(self, figure_size=[10,5], gridlines=True, save=True, savename="ganttchart.png", frequency=3,fontsize=12, axisfont=16, wraplen=40, wrap=True, legend=True, loc=1, MS=True, D=True, MSmarker=200,Dmarker=200):
        """The plot creates a broken bar chart from the csv data processed."""
        self.figure_size=figure_size
        self.gridlines=gridlines
        self.save=save
        self.savename=savename
        self.fontsize=fontsize
        self.axisfont=axisfont
        self.wraplen=wraplen
        self.wrap=wrap
        self.frequency=frequency
        self.legend=legend
        self.loc=loc
        self.MS=MS
        self.D=D
        self.MSmarker=MSmarker
        self.Dmarker=Dmarker
        plt.rcParams.update({'font.size': self.axisfont})
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()
    
        # fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
    
        # Setting Y-axis limits
        gnt.set_ylim(len(self.tasklist)*(self.height+self.gap)+self.height+self.gap,self.height-self.gap/5)
          
        # Setting X-axis limits
        gnt.set_xlim(0,self.total_months+1)
          
        # Setting labels for x-axis and y-axis
        gnt.set_xlabel(self.timeunit, fontsize=self.axisfont)
        gnt.margins(0.6)
        # Setting ticks on y-axis and labelling tickes of y-axis
        yticks=[]
        yticklabels=[]
        for a in range(len(self.tasklist)):
            b=a*(self.height+self.gap)+self.gap+self.height*1.5
            yticks.append(b)
            thelabel=self.tasklist[a][0]
            if len(thelabel)>wraplen and self.wrap==True:
                split=thelabel.split(' ')
                string_label=split[0]
                n_split=len(split)//2+1
                for n in range(1,n_split):
                    string_label+=' '+ split[n]
                string_label+='\n'
                for n in range(n_split, len(split)):
                    string_label+=' '+split[n]
                               
                thelabel=string_label         

            yticklabels.append(thelabel)

        gnt.set_yticks(yticks)
        gnt.set_yticklabels(yticklabels, fontsize=self.fontsize,wrap=True)
        xticks = ticker.MaxNLocator(int(self.total_months/self.frequency+1))
        gnt.xaxis.set_major_locator(xticks)
        
        # Setting graph attribute
        if self.gridlines==True:
            gnt.grid(axis='x')
        else:
            gnt.grid(False)
        self.no_milestones=1 
        self.no_deliverables=1 
        for i,task in enumerate(self.tasklist):    
        # Declaring a bar in schedule
            
            gnt.broken_barh(task[1], ((i+1)*(self.height+self.gap), self.height), facecolors =task[2], label=task[3])
            self.milestone(i)
            self.deliverable(i)
                
    
        msdf=pd.DataFrame(data={'Number':self.milestoneindex,'Milestone':self.milestonelist})
        msdf=msdf.sort_values(by=['Number'])
        msdf=msdf.reset_index(drop=True)
        ddf=pd.DataFrame(data={'Object':self.deliverableindex,'Deliverable':self.deliverablelist})
        ddf=ddf.sort_values(by=['Object'])
        ddf=ddf.reset_index(drop=True)
        
        sumdf = pd.concat([msdf, ddf], axis=1) 
        
        ddf.to_csv('deliverabletable.csv',index=False)
        msdf.to_csv('milestonetable.csv',index=False)
        sumdf.to_csv('summarytable.csv',index=False)
        fig.set_size_inches(self.figure_size[0], self.figure_size[1])
        
        #A neat method to return the legend without repeating
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        if legend==True:
            plt.legend(by_label.values(), by_label.keys(), loc=self.loc, fontsize=12)
        if save==True:
            plt.savefig(self.savename, format='pdf',dpi=fig.dpi)
        plt.show()
        plt.close()
       
            
    
if __name__ == "__main__":   
    filename='tasklist.csv'
    #WP represents Work Packages and should be numberical 1,2,3 etc.
    gantt=Gantt(filename, gap=10, height=60, WP=True)
    # The first argument is figure size in inches 
    gantt.plot([34/2.5,30/2.5],wraplen=50, wrap=True, frequency=6, loc=1, savename='gantt.pdf', MSmarker=350)
    
    
