import analysis_management as am
import matplotlib.pyplot   as plt
import matplotlib.dates as mdates
from   datetime import datetime

import warnings
warnings.filterwarnings('ignore')

# task 1
task1 = am.Task(name='standalone_task',description='Test a standalone task implemented on the fly',start_date='2016-10-10')
task1.set_subproject('Testing')
task1.set_categories(['code','on-the-fly'])
task1.set_priority(1)
task1.set_initial_people(['Jason','Jaymie'])
task1.set_initial_progress(0.2)
task1.add_date_block(datetime.strptime('2016-12-25','%Y-%m-%d'), comment='This is xmas -> hurry hup !!!', add_people=['Santa'], progress=0.4)
task1.add_date_block(datetime.strptime('2016-12-26','%Y-%m-%d'), comment='Xmas is gone, too late!', add_people=['Mr Coca'], progress=0.7)
task1.add_date_block(datetime.strptime('2016-12-27','%Y-%m-%d'), comment='I eat too much, becareful', add_people=['Pere Dodu'], progress=0.8)

#task1.set_progress(1)

# A study
study1=am.Study(datetime.strptime('2017-03-12','%Y-%m-%d'),'Katy','https://en.wikipedia.org/wiki/Jason_(given_name)','Origin of my name')
task1.add_study(study1)

# Read task from as single-task file
task2 = am.Task(infile='one_task.task')
task2.print_history()
dates=task2.get_modification_dates()
plt.figure(); plt.plot(dates, [task2.get_state(d).progress      for d in dates] ); 
plt.figure(); plt.plot(dates, [len(task2.get_state(d).people)   for d in dates] ); 
plt.figure(); plt.plot(dates, [len(task2.get_state(d).studies)  for d in dates] ); 
plt.figure(); plt.plot(dates, [len(task2.get_state(d).comments) for d in dates] );


# Project
my_project = am.Project('MyAwesomeProject')   # Build an awesome project
my_project.load_tasks_file('full_list.task')  # Load a full list of tasks
my_project.add_tasks([task1,task2])           # Add some taks on the fly

# Print some useful info
print('\nGeneral information')
print('===================')
print('Subprojects: {}'.format(my_project.get_subprojects().keys()))
print('Categogies: {}'.format(my_project.get_categories()))
for t in my_project.get_tasks():
    print('{}: {:0.1f}'.format(t.name,t.progress))


# Print all tasks per category:
print('\nTasks per categories')
print('====================')
for cat in my_project.get_categories():
    print('\n'+cat+':')
    for t in my_project.get_tasks():
        if (cat in t.cat): print('  -'+t.name)


# Plots histogram of progresses and priorities
progresses = [t.progress for t in my_project.get_tasks()]
priorities = [t.priority for t in my_project.get_tasks()]
plt.figure(); plt.hist(progresses);
plt.figure(); plt.hist(priorities);


# Plot the number of categories as function to time
dates=my_project.get_modification_dates()
ncat = [len(my_project.get_state(d).get_categories()) for d in dates]
plt.figure()
plt.plot(dates,ncat,marker='o');


# Plot the number of contribution for each tasks
plt.figure()
for t in my_project.tasks:
    dates=t.get_modification_dates()
    plt.plot(dates, [len(t.get_state(d).studies) for d in dates], marker='o' ,label=t.name )
plt.legend()


# Plot the progression of all tasks
plt.figure()
for t in my_project.tasks:
    dates=t.get_modification_dates()
    plt.plot(dates, [t.get_state(d).progress for d in dates], marker='o' ,label=t.name )
plt.legend()


# Plot number of tasks per sub-project vs time
plt.figure()
plt.title(my_project.name)
sub_project = my_project.get_subprojects()

proj_temp = sub_project['Testing']
for d in proj_temp.get_modification_dates():
    print('\n'*2)
    print(d)
    print('N[tasks]={:.0f}'.format(len(proj_temp.get_state(d).get_tasks())))
    for t in proj_temp.get_state(d).get_tasks():
        print(t)



for name,proj in sub_project.items():
    dates=proj.get_modification_dates()
    plt.subplot(121)
    plt.plot(dates,[len(proj.get_state(d).get_tasks()) for d in dates], label=name, marker='o')
    plt.legend()
    plt.subplot(122)
    plt.plot(dates,[len(proj.get_state(d).get_contributors()) for d in dates], label=name, marker='o')
    plt.legend()

plt.show()
