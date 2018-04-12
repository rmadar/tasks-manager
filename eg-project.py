import analysis_management as am

# task 1
task1 = am.Task(name='task1',description='Test a standalone task')
task1.set_subproject('combination')
task1.add_categories(['systematics'])
task1.add_people(['Jean-Claude','Pierre'])
task1.set_priority(1)
task1.set_progress(0)

# A study
contrib_test=am.Study('12-03-2017','Jacques','http://google.com')
task1.add_study(contrib_test)

# Read task from as single-task file
task2 = am.Task(infile='one_task.task')

# Project
my_project = am.Project('4topSM')

# Load task file project
my_project.load_tasks_file('lepton.task')

# Add some taks on the fly
my_project.add_tasks([task1,task2])



print(my_project.get_subprojects())
print(my_project.get_categories())

for t in my_project.get_tasks():
    print(t.name,t.progress)

#for t in my_project.get_tasks():
#    print(t.formatted_str('html'))
