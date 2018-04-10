##-------------------------------------------------
## 'Study' class to be able to add studies related
## to a particular tak.
##-------------------------------------------------
class Study:

    def __init__(self,date,contributor,link,**kwargs):
        """
        Study() class is the element describing a given study and its documentation:
         - date: date of the presentation (string)
         - contributor: speaker (string)
         - link: indico link (string)
         - keyword arguments can take the following:
           * meeting: string describing the type of meeting (e.g. weekly meeting, workshop)
           * title: srting describing the title of the contribution (e.g. 'Final result')
        """
        self.date=date
        self.contributor=contributor
        self.link=link

        try:
            self.meeting = kwargs['meeting']
        except:
            self.meeting=None

        try:
            self.title = kwargs['title']
        except:
            self.title='Update'
                        

    def __str__(self):
        s = self.title + ' ('+ self.contributor+ ', ' + self.date + '): ' + self.link
        return s
        
    def formatted_str(self,synthax):
        """
        Print a formatted string in different synthax. Following synthax are accepted:
         - latex (LaTeX)
         - md (Markdown)
         - html
         - twiki (ATLAS Twiki)
        """
        link_title=self.title + ' ('+ self.contributor+ ', ' + self.date + ')'
        if   (synthax is 'latex'): return '\href{'+self.link+'}{'+link_title+'}'
        elif (synthax is 'md')   : return '['+link_title+']('+self.link+')'
        elif (synthax is 'html') : return '<a href='+self.link+' target=\"_blank\">'+link_title+'</a>'
        elif (synthax is 'twiki'): return str(self)
        else: return str(self)




##--------------------------------------------------
## 'Task' class which contains all information about
## a particular task
##--------------------------------------------------
class Task:

    def __init__(self,short_name,long_name,**kwargs):
        """
        Task() class is the building block of task manager
         - short_name: string giving shot name to be used in small tables/histogram
         - long_name : string, giving a longer description
         - keyword arguments can take the following:
           * subproject: string, giving the subproject in which this task belongs to (e.g. 'l+jets')
           * categories: array of string, giving the type of task (eg. ['optimisation', 'background understanding'])
           * people    : array of string, giving the name of people involved
           * prio_tasks: array of tasks, giving all tasks that should be completed before
           * post_tasks: array of tasks, giving all tasks that need this task to be completed
        """
        
        self.sname = short_name
        self.lname = long_name
                    
        try:
            self.subproject = kwargs['subproject']
        except:
            self.subproject=[]
            
        try:
            self.cat = kwargs['categories']
        except:
            self.cat=[]

        try:
            self.people = kwargs['people']
        except:
            self.people=[]

        try:
            self.prio_tasks = kwargs['prio_tasks']
        except:
            self.prio_tasks=[]
            
        try:
            self.post_tasks = kwargs['post_tasks']
        except:
            self.post_tasks=[]

        self.priority=None
        self.progress=None
        self.studies=[]

    
    def __copy__(self,tsk,short_name,long_name):
        return Task(short_name,long_name,subproject=tsk.subproject, \
                    categories=tsk.cat,people=tsk.people,prio_tasks=tsk.prio_tasks,\
                    post_tasks=tsk.post_tasks)

    def __str__(self):
        str_long       = '  Description: ' + self.lname + '\n'        
        str_priority   = '  Priority: ' + str(self.priority) + '\n'
        str_progress   = '  Progress: ' + str(self.progress) + '\n'
        str_person     = '  People: '+ ', '.join(self.people) + '\n'
        str_subproject = '  Sub-project: '+ self.subproject + '\n'
        str_category   = '  Categories: '+ ', '.join(self.cat) + '\n'
        str_prior      = '  Needed completed tasks: '+ ', '.join(self.prio_tasks) + '\n'
        str_post       = '  To be completed for: '+ ', '.join(self.post_tasks) + '\n'
        str_studies    = '  List of studies:\n'
        for s in self.studies: str_studies += '    - ' + str(s) + '\n'
        s='\n'
        s+='-'*(len(self.sname)+4)+'\n'
        s+='- '+self.sname+' -\n'
        s+='-'*(len(self.sname)+4)+'\n'
        s+=str_long
        if (self.subproject): s+=str_subproject
        if (self.priority):   s+=str_priority
        if (self.progress):   s+=str_progress
        if (self.people):     s+=str_person
        if (self.cat):        s+=str_category
        if (self.studies):    s+=str_studies
        return s
    

    def formatted_str(self,synthax):
        title=''
        begin_block=''
        end_block=''
        begin_item=''
        end_item=''
        if (synthax is 'latex'):
            title='\\textbf{'+self.sname.replace('_','\_')+'}\n'
            begin_block='\\begin{itemize}\n'
            end_block='\\end{itemize}\n'
            begin_item='\\item '
            end_item='\n'
        elif (synthax is 'md'):
            title='**'+self.sname+'**\n'
            begin_item=' * '
            end_item='\n'
        elif (synthax is 'html'):
            title='<b>'+self.sname+'</b>\n'
            begin_block='<ul>'
            end_block='</ul>\n'
            begin_item='<li>'
            end_item='</li>\n'
        elif (synthax is 'twiki'):
            return str(self)
        else:
            return str(self)

        s=''
        s+=title
        s+=begin_block
        s+=begin_item + 'Description: '+ self.lname   + end_item
        if (self.subproject): s+=begin_item + 'Sub-project: '+ self.subproject   + end_item
        if (self.priority):   s+=begin_item + 'Priority: ' + str(self.priority)  + end_item
        if (self.progress):   s+=begin_item + 'Progress: ' + str(self.progress)  + end_item
        if (self.people):     s+=begin_item + 'People: '+ ', '.join(self.people)  + end_item
        if (self.cat):        s+=begin_item + 'Categories: '+ ', '.join(self.cat) + end_item
        if (self.studies):
            s+=begin_item + 'List of studies:' + end_item
            s+=begin_block
            for stu in self.studies: s+= '  ' + begin_item + stu.formatted_str(synthax) + end_item
            s+=end_block
        s+=end_block
        return s
    
    def copy(self,short_name,long_name):
        return self.__copy__(self,short_name,long_name)
    
    def set_priority(self,p):
        self.priority=p
        
    def set_progress(self,p):
        self.progress=p

    def set_subproject(self,subproj):
        self.subproject = subproj

    def set_categories(self,cats):
        self.cat=cats

    def set_people(self,persons):
        self.people=persons
        
    def add_categories(self,cats):
        for c in cats:
            self.cat.append(c)
            
    def add_people(self,people_name):
        for person in people_name:
            self.people.append(person)

    def add_prior_tasks(self,tasks_before):
        for tsk in tasks_before:
            self.prio_tasks.append(tsk)

    def add_posterior_tasks(self,tasks_after):
        for tsk in tasks_after:
            self.post_tasks.append(tsk)

    def add_studies(self,studies):
        for s in studies:
            self.add_study(s)

    def add_study(self,s):
        self.studies.append(s)



##-----------------------------------------------
## 'Project' class which contains all taks for a 
## given project
##-----------------------------------------------
class Project:

    def __init__(self,name):
        self.name=name
        self.tasks=[]

    def set_tasks(self,tasks):
        self.tasks = tasks
        
    def add_task(self,task):
        self.tasks.append(task)

    def add_tasks(self,tasks):
        for t in tasks: self.tasks.append(t)

    def get_tasks(self,subproject)
        
    def subprojects(self):
        subproj = [t.subproject for t in self.tasks]
        return list(set(subproj))

    def contributors(self):
        contribs = [p for t in self.tasks for p in t.people]
        return list(set(contribs))

    def dataframe(self):
        import pandas as pd
        return pd.DataFrame()
