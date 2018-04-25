import analysis_management as am
import matplotlib.pyplot   as plt
import matplotlib.dates as mdates

import warnings
warnings.filterwarnings('ignore')


########################
# Tasks related examples
########################

# helper function for dates
from datetime import datetime
def date(s):
    return datetime.strptime(s,'%Y-%m-%d')

# Create a task in the code
task1 = am.Task(name='standalone_task',description='Test a standalone task implemented on the fly',start_date='2016-10-10')
task1.set_subproject('Testing')
task1.set_categories(['code','on-the-fly'])
task1.set_priority(1)
task1.set_initial_people(['Jason','Jaymie'])
task1.set_initial_progress(0.2)
task1.add_date_block(date('2016-12-25'), comment='This is xmas -> hurry hup !!!', add_people=['Santa'], progress=0.4)
task1.add_date_block(date('2016-12-26'), comment='Xmas is gone, too late!', add_people=['Mr Coca'], progress=0.7)
task1.add_date_block(date('2016-12-27'), comment='I eat too much, becareful', add_people=['Pere Dodu'], progress=0.8)

# Adding a study to task1
study1=am.Study(date('2017-03-12'),'Katy','https://en.wikipedia.org/wiki/Jason_(given_name)','Origin of my name')
task1.add_studies([study1])

# Create a task from task inputfile
task2 = am.Task(infile='one_task.task')
task2.print_history()
fig = task2.plot_evolution()
fig.savefig('TaskEvolution.pdf')


##########################
# Project related examples
##########################

my_project = am.Project('MyAwesomeProject')   # Build an awesome project
my_project.load_tasks_file('full_list.task')  # Load a full list of tasks
my_project.add_tasks([task1,task2])           # Add some taks on the fly

# Make interesting plots
my_project.plot_status()
