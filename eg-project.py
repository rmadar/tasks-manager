import task as tsk

# task 1
lep_kinem_ljets = tsk.Task('lep_kinem_ljets','Optimization of the lepton kinematics in the l+jets/os2L channel')
lep_kinem_ljets.set_subproject('l+jets')
lep_kinem_ljets.add_categories(['optimizations'])
lep_kinem_ljets.add_people(['Matt K.','Simon'])
lep_kinem_ljets.set_priority(1)
lep_kinem_ljets.set_progress(0)

# task 2
lep_kinem_ss2L = tsk.Task('lep_kinem_ss2L','Optimization of the lepton kinematics in the ss2L/3L channel')
lep_kinem_ss2L.set_subproject('ss2L/3L')
lep_kinem_ss2L.set_categories(['optimizations'])
lep_kinem_ss2L.set_people(['Shuyang'])
lep_kinem_ss2L.set_priority(1)
lep_kinem_ss2L.set_progress(0)
lep_kinem_ss2L.add_study( tsk.Study('11-04-2018','Zhi','https://indico.cern.ch/event/696609/contributions/2943411/attachments/1625965/2589626/OverlapRemovalStudy.pdf')  )

# task 3
btagging_ss2L = tsk.Task('btagging_ss2L','Optimization of the b-tagging working point for the ss2L/3L channel')
btagging_ss2L.set_subproject('ss2L/3L')
btagging_ss2L.set_categories(['optimizations'])
btagging_ss2L.set_people(['Romain'])
btagging_ss2L.set_priority(1)
btagging_ss2L.set_progress(0.5)
btagging_ss2L.add_study( tsk.Study('03-04-2018','Romain','https://indico.cern.ch/event/696609/contributions/2943410/attachments/1625903/2589232/Btagging.pdf') )

# task 4
NP_naming = tsk.Task('NP_naming','Design the naming convention of nuisance paramter for the combination')
NP_naming.set_subproject('combination')
NP_naming.set_people(['Robert Deniro'])


# A study
contrib_test  = tsk.Study('12-03-2017','Romain Madar','http://romain-madar.com')
lep_kinem_ljets.add_study(contrib_test)

# Array of tasks
lepton_tasks = [lep_kinem_ljets,lep_kinem_ss2L,btagging_ss2L,NP_naming]
    

# Project
my_project = tsk.Project('4topSM')
my_project.add_tasks(lepton_tasks)
print(my_project.subprojects())
print(my_project.contributors())
