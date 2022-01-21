# CSVtoGanttChart
Creates a Gantt chart from a csv file see the csv example.  I will add more feature in future versions.
The plot is saved in same directory as the code as default. Tasks with 'gaps' can be added (five suggested in the example, but in practive it is not limited).
The code uses pandas and matplotlib modules. Milestones and deliverables can be added but are currently associated with tasks (decoupling will be done later). An output csv file summerises the milestones and deliverables with labels in chronological order matching the plot.

