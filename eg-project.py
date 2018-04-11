import analysis_management as am

# task 1
#task1 = am.Task(name='task1',description='Optimization of the lepton kinematics in the l+jets/os2L channel')
#task1.set_subproject('l+jets')
#task1.add_categories(['optimizations'])
#task1.add_people(['Matt K.','Simon'])
#task1.set_priority(1)
#task1.set_progress(0)

# A study
#contrib_test=am.Study('12-03-2017','Romain Madar','http://romain-madar.com')
#task1.add_study(contrib_test)

task2 = am.Task(infile='one_task.task')
#print(task2)
#print(task2.formatted_str('html'))

# Project
my_project = am.Project('4topSM')
#my_project.add_tasks(lepton_tasks)
my_project.load_tasks_file('lepton.tasks')
print(my_project.subprojects())
#print(my_project.contributors())
