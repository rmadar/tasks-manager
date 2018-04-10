import task as tsk

lep_kinem_ljets = tsk.Task('lep_kinem_ljets','Optimization of the lepton kinematics in the l+jets/os2L channel')
lep_kinem_ljets.set_subproject('l+jets')
lep_kinem_ljets.add_categories(['optimizations'])
lep_kinem_ljets.add_people(['Matt K.','Simon'])
lep_kinem_ljets.set_priority(1)
lep_kinem_ljets.set_progress(0)

lep_kinem_ss2L = tsk.Task('lep_kinem_ss2L','Optimization of the lepton kinematics in the ss2L/3L channel')
lep_kinem_ss2L.set_subproject('ss2L/3L')
lep_kinem_ss2L.set_categories(['optimizations'])
lep_kinem_ss2L.set_people(['Shuyang'])
lep_kinem_ss2L.set_priority(1)
lep_kinem_ss2L.set_progress(0)
lep_kinem_ss2L.add_study( tsk.Study('11-04-2018','Zhi','https://indico.cern.ch/event/696609/contributions/2943411/attachments/1625965/2589626/OverlapRemovalStudy.pdf')  )


lepton_tasks = [lep_kinem_ljets,lep_kinem_ss2L]

contribution = tsk.Study('12-03-2017','Romain Madar','http://romain-madar.com')
print(contribution.formatted_str('latex'))
print(contribution.formatted_str('md'))
print(contribution.formatted_str('html'))
print(contribution.formatted_str('twiki'))

for t in lepton_tasks:
    print(t.formatted_str('latex'))
    print(t.formatted_str('md'))
    print(t.formatted_str('html'))
    print(t.formatted_str('twiki'))
