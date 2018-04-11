##-------------------------------------------------
## 'Study' class to be able to add studies related
## to a particular tak.
##-------------------------------------------------
class Study:

    def __init__(self,date,contributor,link,title='Update'):
        """
        Study() class is the element describing a given study and its documentation:
         - date: date of the presentation (string)
         - contributor: speaker (string)
         - link: indico link (string)
         - title: contribution title (string)
        """
        self.date=date
        self.contributor=contributor
        self.link=link
        self.title=title
        
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

    def __init__(self,**kwargs):
        """
        Task() class is the building block of task manager, keyword arguments can take the following:
           * infile     : string, input file containt the task information
           * name       : string, giving the name of the task
           * description: string, giving the description of the task
           * subproject : string, giving the subproject in which this task belongs to (e.g. 'l+jets')
           * categories : array of string, giving the type of task (eg. ['optimisation', 'background understanding'])
           * people     : array of string, giving the name of people involved
           * prio_tasks : array of tasks, giving all tasks that should be completed before
           * post_tasks : array of tasks, giving all tasks that need this task to be completed
        """

        self.name='name'
        self.description='description'
        self.subproject=''
        self.people=[]
        self.cat=[]
        self.prio_tasks=[]
        self.post_tasks=[]
        self.priority=None
        self.progress=None
        self.comments=[]
        self.studies=[]

        
        if ('infile' in kwargs):

            def token_info(s,t):
                if (s[:len(t)]==t): return s[s.find(t)+len(t):].strip()
                else: return 'dummy'

            def is_token_line(l,t):
                return l[0:len(t)]==t
                
            f = open(kwargs['infile'],'r')
            for l in f.readlines():
                l = l.strip()
                try:
                    if (l[0]=='#'): continue
                except:
                    continue

                if (is_token_line(l,'.name:')):        self.name        = token_info(l,'.name:')
                if (is_token_line(l,'.description:')): self.description = token_info(l,'.description:')
                if (is_token_line(l,'.subproject:')):  self.subproject  = token_info(l,'.subproject:')
                if (is_token_line(l,'.priority:')):    self.priority    = int(token_info(l,'.priority:'))
                if (is_token_line(l,'.progress:')):    self.progress    = float(token_info(l,'.progress:'))
                if (is_token_line(l,'.categories:')):  self.cat         = [s.strip() for s in token_info(l,'.categories:').split(',')]
                if (is_token_line(l,'.people:')):      self.people      = [s.strip() for s in token_info(l,'.people:').split(',')]
                if (is_token_line(l,'.comment:')):     self.add_comment( token_info(l,'.comment:') )  
                if (is_token_line(l,'.study:')):
                    study_data  = [s.strip() for s in token_info(l,'.study:').split(',')]
                    self.add_study( Study(*study_data)  )  

                if (is_token_line(l,'.priority:')):
                    print(token_info(l,'.priority:'),int(token_info(l,'.priority:')))
                    print()
        else:
            
            if 'name'       in kwargs: self.name = kwargs['name']
            if 'description'in kwargs: self.description = kwargs['description']
            if 'subproject' in kwargs: self.subproject = kwargs['subproject']
            if 'categories' in kwargs: self.cat = kwargs['categories']
            if 'people'     in kwargs: self.people = kwargs['people']
            if 'prio_tasks' in kwargs: self.prio_tasks = kwargs['prio_tasks']
            if 'post_tasks' in kwargs: self.post_tasks = kwargs['post_tasks']

        
    def __copy__(self,tsk,name,description):
        return Task(name=name,description=description,subproject=tsk.subproject, \
                    categories=tsk.cat,people=tsk.people,prio_tasks=tsk.prio_tasks,\
                    post_tasks=tsk.post_tasks)

    def __str__(self):
        s='\n'
        s+='-'*(len(self.name)+4)+'\n'
        s+='- '+self.name+' -\n'
        s+='-'*(len(self.name)+4)+'\n'
        s+='  Description: ' + self.description + '\n'
        str_studies = '  List of studies:\n'
        for st in self.studies: str_studies += '    - ' + str(st) + '\n'
        str_comments = '  List of comments:\n'
        for cm in self.comments: str_comments += '    - ' + str(cm) + '\n'
        if (self.subproject): s+='  Sub-project: '+ self.subproject + '\n'
        if (self.priority is not None): s+='  Priority: ' + str(self.priority) + '\n'
        if (self.progress is not None): s+='  Progress: ' + str(self.progress) + '\n'
        if (self.people):     s+='  People: '+ ', '.join(self.people) + '\n'
        if (self.cat):        s+='  Categories: '+ ', '.join(self.cat) + '\n'
        if (self.studies):    s+=str_studies
        if (self.comments):   s+=str_comments
        return s
    
    
    def formatted_str(self,synthax):
        title=''
        begin_block=''
        end_block=''
        begin_item=''
        end_item=''
        if (synthax is 'latex'):
            title='\\textbf{'+self.name.replace('_','\_')+'}\n'
            begin_block='\\begin{itemize}\n'
            end_block='\\end{itemize}\n'
            begin_item='\\item '
            end_item='\n'
        elif (synthax is 'md'):
            title='**'+self.name+'**\n'
            begin_item=' * '
            end_item='\n'
        elif (synthax is 'html'):
            title='<b>'+self.name+'</b>\n'
            begin_block='<ul>\n'
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
        s+=begin_item + 'Description: '+ self.description  + end_item
        if (self.subproject):           s+=begin_item + 'Sub-project: '+ self.subproject   + end_item
        if (self.priority is not None): s+=begin_item + 'Priority: ' + str(self.priority)  + end_item
        if (self.progress is not None): s+=begin_item + 'Progress: ' + str(self.progress)  + end_item
        if (self.people):               s+=begin_item + 'People: '+ ', '.join(self.people)  + end_item
        if (self.cat):                  s+=begin_item + 'Categories: '+ ', '.join(self.cat) + end_item
        if (self.studies):
            s+=begin_item + 'List of studies:' + end_item
            s+=begin_block
            for stu in self.studies: s+= '  ' + begin_item + stu.formatted_str(synthax) + end_item
            s+=end_block
        s+=end_block
        if (self.comments):
            s+=begin_item + 'List of comments:' + end_item
            s+=begin_block
            for cm in self.comments: s+= '  ' + begin_item + cm + end_item
            s+=end_block
        return s
    
    def copy(self,name,description):
        return self.__copy__(self,name,description)
    
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

    def add_comment(self, item):
        self.comments.append(item)
        
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

    def load_tasks_file(self,filename):
        f = open(filename,'r')
        i_task=0
        for l in f.readlines():

            # Clean the line and remove commented line '#'
            l = l.strip()
            try:
                if l[0]=='#': continue
            except:
                continue

            # Keep track of when the task is changing
            # Goal: split a file with many tasks in many
            # files with only one task per file.
            local_task_index=i_task
            tmp_file = open('tmp.task','w+')
            if (l=='+tsk'):
                if (i_task>0):
                    tmp_file.close()
                    self.add_task( Task(infile='tmp.task') )
                i_task+=1
              
            if (local_task_index==i_task):
                tmp_file.write(l)
                for l2 in tmp_file: print(l2)

    
    def add_task(self,task):
        self.tasks.append(task)

    def add_tasks(self,tasks):
        for t in tasks: self.tasks.append(t)

    def get_tasks(self,subproject):
        return []
        
    def subprojects(self):
        subproj = [t.subproject for t in self.tasks]
        return list(set(subproj))

    def contributors(self):
        contribs = [p for t in self.tasks for p in t.people]
        return list(set(contribs))

    def dataframe(self):
        import pandas as pd        
        return pd.DataFrame()
