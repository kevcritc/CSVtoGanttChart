#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:06:16 2021

@author: phykc
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:06:16 2021
@author: phykc
"""
import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd
import random
from ast import literal_eval
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable

#Create a class that hold the data for the gantt chart in pandas
class Gantt:
    """Process a  Gantt chart from .xlsx file using the Matplotlib module. Use the template csv to create data and save in the same directory as the .py file"""
    def __init__(self,filename,total_months=42, height=8, gap=1, timeunit='Month', WP=True, FS=True):
        
        self.filename=filename
        self.total_months=total_months
        self.height=height
        self.gap=gap
        self.timeunit=timeunit
        self.WP=WP
        self.FS=FS
        self.definetasklist()
        self.milestoneindex=[]
        self.milestoneID=[]
        self.milestonelist=[]
        self.deliverableindex=[]
        self.deliverablelist=[]  
        self.deliverableID=[]  
    def definetasklist(self):
        #Read the file into the df - the csv file example is the template required
        self.df=pd.read_excel(self.filename,dtype={'Task': 'str','WP': 'str','FS Dependency':'object'})
        #Create a dataframe to test the boundaries of the data, allows skipped task lines
        self.checkdf=self.df.isnull()
        tasks=self.df['Task']
        self.tasklist=[]
        # Set up the colours to be used allows 50 personnel but only 10 colors
        colors=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray', 'tab:olive', 'tab:cyan']*10
        textcolors=['tab:blue','tab:green','tab:red','tab:purple','tab:brown','tab:gray', 'tab:olive', 'tab:cyan']*10
        self.linecolors=['blue','orange','green','red','purple','brown','pink','gray', 'olive', 'cyan']*10
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
                indexstart=self.df.columns.get_loc('Length')+1
                # Looks for addional start times for a task e.g. a break in the task the column positions must be the same.
                # A missing 'start' will cause an error
                while cell_test==False:
                    if self.checkdf.iloc[n,indexstart+a]==True:
                        cell_test=True
                    else:
                        sslist.append(tuple([self.df.iloc[n,indexstart+a], self.df.iloc[n,indexstart+1+a]]))
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
            if self.checkdf.loc[i,'MS Task ID']==True:
                tasklineheight=(i+1)*(self.height+self.gap)
            else:
                tasklineheight=(self.df.loc[i,'MS Task ID'])*(self.height+self.gap)
            
            plt.scatter(self.df.loc[i,'M Month'], tasklineheight+self.height*0.5, marker='*',s=self.MSmarker, c='black')
            plt.text(self.df.loc[i,'M Month']+0.5,tasklineheight+self.height*0.75, s='MS'+str(NewID))
            self.milestoneindex.append(NewID)
            self.milestoneID.append('MS'+str(NewID))
            self.milestonelist.append(self.df.loc[i,'Milestone'])
            
    def deliverable(self,i):
         if self.checkdf.loc[i,'D Month']==False and self.D==True:
             NewID=self.delivermonths.loc[i,'New_ID']
             if self.checkdf.loc[i,'D Task ID']==True:
                 tasklineheight=(i+1)*(self.height+self.gap)
             else:
                 tasklineheight=(self.df.loc[i,'D Task ID'])*(self.height+self.gap)
             tasklineheight=(self.df.loc[i,'D Task ID'])*(self.height+self.gap)
             plt.scatter(self.df.loc[i,'D Month'], tasklineheight+self.height*0.5, marker='^',s=self.Dmarker, c='black')
             plt.text(self.df.loc[i,'D Month']+0.5,tasklineheight+self.height*0.75, s='D'+str(NewID))
             self.deliverableindex.append(NewID)
             self.deliverableID.append('D'+str(NewID))
             self.deliverablelist.append(self.df.loc[i,'Deliverable'])
             
    def offset_line(self,off):
        w=off+1
        if w%2==0:
            f=-1
        else:
            f=1
        q=w//2
        return f*q*self.gap
        
    def dependancy(self,i):
        padx=0.5
        if self.checkdf.loc[i,'FS Dependency']==False and self.FS==True:
            dlist=literal_eval(self.df.loc[i,'FS Dependency'])
        
            for off,fs in enumerate(dlist):
                to_y=((i+1)*(self.height+self.gap)+self.height*0.5)+self.offset_line(off)
                from_index=fs-1
                from_y=((from_index+1)*(self.height+self.gap)+self.height*0.5)
                to_x=self.df.loc[i,'Start']
                from_x=self.df.loc[from_index,'Start']+self.df.loc[from_index,'Length']
                xlinelist=[from_x, from_x+padx,from_x+padx, from_x+padx,from_x+padx, from_x-padx,from_x-padx, from_x-padx,from_x-padx, to_x]
                ylinelist=[from_y,from_y,from_y,from_y+self.gap*0.5+self.height*0.5,from_y+(self.gap)*0.5+self.height*0.5,from_y+(self.gap)*0.5+self.height*0.5,from_y+(+self.gap)*0.5+self.height*0.5,to_y,to_y,to_y]
                if self.FScolors==False:
                    linecol='gray'
                else:
                    
                    linecol=self.linecolors[i]
                plt.plot(xlinelist,ylinelist , linewidth=3, color=linecol)           
             
    def plot(self, figure_size=[10,5], gridlines=True, save=True, savename="ganttchart.png", frequency=3,fontsize=12, axisfont=16, wraplen=40, wrap=True, legend=True, loc=1, MS=True, D=True, MSmarker=200,Dmarker=200, FScolors=True):
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
        self.FScolors=FScolors
        plt.rcParams.update({'font.size': self.axisfont})
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()
    
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
        # Makes room for long labels
        make_axes_area_auto_adjustable(gnt)
        # Adds the ability to split the text over 2/3 lines.
        for a in range(len(self.tasklist)):
            b=a*(self.height+self.gap)+self.gap+self.height*1.5
            yticks.append(b)
            thelabel=self.tasklist[a][0]
            if len(thelabel)>self.wraplen and self.wrap==True: 
                split=thelabel.split(' ')
                line_label=[]
                stringlist=[]
                for word in split:
                    stringlist.append(word)
                    sentance=' '.join(stringlist)
                    if len(sentance)>self.wraplen:
                        line_label.append(sentance+'\n')
                        stringlist=[]
                line_label.append(' '.join(stringlist))
                thelabel=''.join(line_label)
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
            p=self.df.loc[i,'Task ID']-1
            gnt.broken_barh(task[1], ((p+1)*(self.height+self.gap), self.height), facecolors =task[2], label=task[3])
            if self.FS==True:
                self.dependancy(p)
                if self.MS==True:
                    self.milestone(p)
                if self.D==True:
                    self.deliverable(p)
                
        
        while self.checkdf.loc[i,'Milestone']==False or self.checkdf.loc[i,'Deliverable']==False:
            i+=1
            
        
            if self.MS==True:
                self.milestone(i)
            if self.D==True:
                self.deliverable(i)
            
    
        msdf=pd.DataFrame(data={'Number':self.milestoneindex,'ID':self.milestoneID,'Milestone':self.milestonelist})
        msdf=msdf.sort_values(by=['Number'])
        msdf=msdf.reset_index(drop=True)
        ddf=pd.DataFrame(data={'Number':self.deliverableindex,'ID':self.deliverableID,'Deliverable':self.deliverablelist})
        ddf=ddf.sort_values(by=['Number'])
        ddf=ddf.reset_index(drop=True)
        sumdf = pd.concat([msdf, ddf], axis=1) 
        ddf.to_excel('deliverabletable.xlsx',index=False)
        msdf.to_excel('milestonetable.xlsx',index=False)
        sumdf.to_excel('summarytable.xlsx',index=False)
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
    filename='tasklist1exaample.xlsx'
    #WP represents Work Packages and should be numberical 1,2,3 etc.
    gantt=Gantt(filename,total_months=42, height=120, gap=25, timeunit='Month', WP=True, FS=True)
    # The first argument is figure size in inches 
    gantt.plot(figure_size=[17,11],gridlines=True, save=True, savename="ganttchart.png", frequency=6,fontsize=10, axisfont=14, wraplen=75, wrap=True, legend=True, loc=1, MS=True, D=True, MSmarker=200,Dmarker=200,FScolors=False)
