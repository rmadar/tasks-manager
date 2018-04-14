import analysis_management as am
import matplotlib.pyplot   as plt
from   datetime import datetime

# task 1
task1 = am.Task(name='standalone_task',description='Test a standalone task implemented on the fly')
task1.set_subproject('Testing')
task1.add_categories(['code','on-the-fly'])
task1.add_people(['Jason','Jaymie'])
task1.set_priority(1)
task1.set_progress(0)

# A study
study1=am.Study('12-03-2017','Jason','https://en.wikipedia.org/wiki/Jason_(given_name)','Origin of my name')
task1.add_study(study1)

# Read task from as single-task file
task2 = am.Task(infile='one_task.task')
task2.print_history()


# Project
my_project = am.Project('MyAwesomeProject')   # Build an awesome project
my_project.load_tasks_file('full_list.task')  # Load a full list of tasks
my_project.add_tasks([task1,task2])           # Add some taks on the fly

# Print some useful info
#print('\nGeneral information')
#print('===================')
#print('Subprojects: {}'.format(my_project.get_subprojects()))
#print('Categogies: {}'.format(my_project.get_categories()))
#for t in my_project.get_tasks():
#    print('{}: {:0.1f}'.format(t.name,t.progress))


# Print all tasks per category:
#print('\nTasks per categories')
#print('====================')
#for cat in my_project.get_categories():
#    print('\n'+cat+':')
#    for t in my_project.get_tasks():
#        if (cat in t.cat): print('  -'+t.name)


# Plots histogram of progresses and priorities
#progresses = [t.progress for t in my_project.get_tasks()]
#priorities = [t.priority for t in my_project.get_tasks()]
#plt.hist(progresses); plt.show()
#plt.hist(priorities); plt.show()

dates=task2.get_modification_dates()
da=[datetime.strptime(d, '%Y-%m-%d') for d in task2.get_modification_dates()]
plt.plot(da, [task2.get_state(d).progress     for d in dates] ); plt.show()
plt.plot(da, [len(task2.get_state(d).people)  for d in dates] ); plt.show()
plt.plot(da, [len(task2.get_state(d).studies) for d in dates] ); plt.show()

