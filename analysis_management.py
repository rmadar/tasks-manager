import numpy  as np
import pandas as pd
from datetime import datetime

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
        s = self.title + ' ('+ self.contributor+ ', ' + str(self.date) + '): ' + self.link
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


##-------------------------------------------------
## 'Comment' class to be able to add comments related
## to a particular task, with a time stamp
##-------------------------------------------------
class Comment:
    def __init__(self,date,text):
        self.date=date
        self.text=text
        
    def __str__(self):
        s = str(self.date) + ': '+ self.text
        return s



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
        self.cat=[]
        self.start_date=''
        self.people=[]
        self.prio_tasks=[]
        self.post_tasks=[]
        self.priority=0.0
        self.progress=0.0
        self.comments=[]
        self.studies=[]
        self.history={}
        
        if ('infile' not in kwargs):
            if 'name'       in kwargs: self.name = kwargs['name']
            if 'description'in kwargs: self.description = kwargs['description']
            if 'subproject' in kwargs: self.subproject = kwargs['subproject']
            if 'start_date' in kwargs: self.start_date = datetime.strptime(kwargs['start_date'],'%Y-%m-%d')
            if 'categories' in kwargs: self.cat = kwargs['categories']
            if 'people'     in kwargs: self.people = kwargs['people']
            if 'prio_tasks' in kwargs: self.prio_tasks = kwargs['prio_tasks']
            if 'post_tasks' in kwargs: self.post_tasks = kwargs['post_tasks']
            self.history[self.start_date]=self.get_current_snapshot()

        else:    
            self.read_from_file(kwargs['infile']);
            
    def __copy__(self,tsk):
        return Task(name=tsk.name,description=tsk.description,start_date=tsk.start_date.strftime('%Y-%m-%d'),\
                    subproject=tsk.subproject,\
                    categories=tsk.cat,people=tsk.people,prio_tasks=tsk.prio_tasks,\
                    post_tasks=tsk.post_tasks)

    def __str__(self):
        s='\n'
        title=self.name+ ' (started on '+self.start_date.strftime('%Y-%m-%d')+')'
        s+='-'*(len(title)+4)+'\n'
        s+='- '+title+' -\n'
        s+='-'*(len(title)+4)+'\n'
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
            title='\\textbf{'+self.name.replace('_','\_')+'} (started on '+self.start_date+')\n'
            begin_block='\\begin{itemize}\n'
            end_block='\\end{itemize}\n'
            begin_item='\\item '
            end_item='\n'
        elif (synthax is 'md'):
            title='**'+self.name+'** (started on '+self.start_date+')\n' 
            begin_item=' * '
            end_item='\n'
        elif (synthax is 'html'):
            title='<b>'+self.name+'</b> (started on '+self.start_date+')\n'
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
        if (self.comments):
            s+=begin_item + 'List of comments:' + end_item
            s+=begin_block
            for cm in self.comments: s+= '  ' + begin_item + cm + end_item
            s+=end_block
        s+=end_block
        return s
    
    def read_from_file(self,infile):
        '''
        Construct a Task object using a text file
        --> this is a quite complex function split into helper functions:
            * count_tasks()
            * token_info(s,t)
            * is_token_line(l,t)
            * read_date_block()
        '''
        def count_tasks():
            ftmp=open(infile,'r')
            line = [l.strip() for l in ftmp.readlines() if len(l.strip())>0 and l.strip()[0] is not '#']
            ftmp.close()
            return line.count('+tsk')

        def token_info(s,t):
            if (s[:len(t)]==t): return s[s.find(t)+len(t):].strip()
            else: return 'dummy'
                
        def is_token_line(l,t):
            return l[0:len(t)]==t

        def read_date_blocks():
            ftmp=open(infile,'r')
            lines   = [l.strip() for l in ftmp.readlines() if len(l.strip())>0 and l.strip()[0] is not '#']
            is_date = [is_token_line(l,'.date:') for l in lines]
            i_start = [i for i,b in enumerate(is_date) if b is True]
            states={}
            Nblock=len(i_start)
            for it in range(0,Nblock):
                start=i_start[it]
                if (it<Nblock-1): stop=i_start[it+1]
                else            : stop=None
                info=lines[start:stop]
                date=datetime.strptime(info[0].replace('.date:','').strip(),'%Y-%m-%d')
                data=info[1:]
                if (date<self.start_date):
                    raise NameError('In task '+ self.name +', the update date \''+str(date)+\
                                    '\' is earlier than the starting date \''+str(self.start_date)+'\'' )
                states[date]=data
            return states
        
        if (count_tasks()>1):
            raise NameError('File given to Task() class is expected to have a single '+\
                            '\'+tsk\' occurence ({:.0f} was counted in {})'\
                            .format(count_tasks(),infile))
            
        f = open(infile,'r')
        for l in f.readlines():
            l = l.strip()
            try:
                if (l[0]=='#'): continue
            except:
                continue
            
            if (is_token_line(l,'.name:')):        self.name        = token_info(l,'.name:')
            if (is_token_line(l,'.start_date')):   self.start_date  = datetime.strptime(token_info(l,'.start_date:'),'%Y-%m-%d')
            if (is_token_line(l,'.description:')): self.description = token_info(l,'.description:')
            if (is_token_line(l,'.subproject:')):  self.subproject  = token_info(l,'.subproject:')
            if (is_token_line(l,'.priority:')):    self.priority    = int(token_info(l,'.priority:'))
            if (is_token_line(l,'.progress:')):    self.progress    = float(token_info(l,'.progress:'))
            if (is_token_line(l,'.categories:')):  self.cat         = [s.strip() for s in token_info(l,'.categories:').split(',')]
            if (is_token_line(l,'.people:')):      self.people      = [s.strip() for s in token_info(l,'.people:').split(',')]
        
        self.history[self.start_date]=self.get_current_snapshot()
        self.load_history( read_date_blocks() )
                
    def load_history(self,states):
        '''
        Update the list of people and the progress of the task using to the last
        state of the task
        '''
        dates=sorted(states)
        for d in dates:
            block = states[d]
            for info in block:
                if info[0:len('*comment:')]    =='*comment:'   : self.add_comment( Comment(d,info[len('*comment:')+1:].strip()) )
                if info[0:len('*study:')]      =='*study:'     : self.add_study( Study(d, *[l.strip() for l in info[len('*study:')+1:].split(',')]) )
                if info[0:len('*add_people:')] =='*add_people:': self.add_people( [n.strip() for n in info[len('*add_people:')+1:].split(',')] )
                if info[0:len('*progress:')]   =='*progress:'  : self.set_progress( float(info[len('*progress:')+1:].strip()) )
            self.history[d] = self.get_current_snapshot()

    def add_date_block(self, date, **kwargs):
        if 'comment'    in kwargs: self.add_comment(Comment(date,kwargs['comment']))
        if 'studies'    in kwargs: self.add_studies(kwargs['studies'])
        if 'add_people' in kwargs: self.add_people(kwargs['add_people'])
        if 'progress'   in kwargs: self.set_progress(kwargs['progress'])
        self.history[date] = self.get_current_snapshot()
        if (date is not self.get_last_update_date()): self = self.get_state()        
        
    def print_history(self):
        dates = sorted(self.history.keys())
        for date in dates:
            print('\n\n\n<<  State of the task on ' + str(date) + '>>')
            print(self.get_state(date))

    def get_state(self,date=''):
        if (not date): date=sorted(self.history)[-1]
        res=self.__copy__(self)
        res.people   = self.history[date]['people']
        res.progress = self.history[date]['progress']
        res.studies  = self.history[date]['studies']
        res.comments = self.history[date]['comments']
        return res

    def get_modification_dates(self):
        return pd.unique( sorted(self.history.keys()) ).tolist()

    def get_last_update_date(self):
        return sorted(self.history.keys())[-1]

    def get_current_snapshot(self):
        return {
            'people'    : list (self.people),
            'progress'  : float(self.progress),
            'comments'  : list (self.comments),
            'studies'   : list (self.studies),
        }
            
    def copy(self,name,description):
        res = self.__copy__(self)
        res.name=name
        res.description=description
        return res

    def is_completed(self,date):
        if (date>=self.get_last_update_date()):
            return self.get_state().progress==1.0
        else:
            return False
        
    def set_priority(self,p):
        self.priority=p
        
    def set_progress(self,p):
        self.progress=p
        
    def set_subproject(self,subproj):
        self.subproject = subproj

    def set_categories(self,cats):
        self.cat=cats

    def set_initial_people(self,persons):
        self.people=persons
        self.history[self.get_last_update_date()] = self.get_current_snapshot()

    def add_comment(self, item):
        self.comments.append(item)
        
    def add_comments(self, items):
        for c in items:
            self.comments.append(c)
        
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
        
    def __copy__(self,pjt):
        res = Project(pjt.name)
        res.tasks=pjt.tasks
        return res
        
    def set_tasks(self,tasks):
        self.tasks = tasks

    def load_tasks_file(self,filename):
        import os
        f = open(filename,'r')
        i_start=[];lines=[]; i=0
        for l in f.readlines():
            l = l.strip()
            if len(l)==0: continue
            if l[0]=='#': continue
            lines.append(l)
            if (l=='+tsk'): i_start.append(i)
            i+=1; 

        Ntask=len(i_start)
        for it in range(0,Ntask):
            start=i_start[it]
            if (it<Ntask-1): stop=i_start[it+1]-1
            else           : stop=None
            ftmp = open('tmp.task','w')
            for l in lines[start:stop]:
                ftmp.write(l+'\n')
            ftmp.close()
            self.add_task(Task(infile='tmp.task'))
            os.remove('tmp.task')
        f.close()

    def add_task(self,task):
        self.tasks.append(task)

    def add_tasks(self,tasks):
        for t in tasks: self.tasks.append(t)

    def get_subprojects(self):
        subproject={}
        subproj_name = np.unique([t.subproject for t in self.tasks])
        for s in subproj_name:
            res=self.__copy__(self)
            res.name=self.name+'_'+s
            res.tasks=[]
            for t in self.tasks:
                if s==t.subproject: res.add_task(t)
                else:               continue
            subproject[s] = res
        return subproject

    def get_contributors(self):
        contribs = [p for t in self.tasks for p in t.people]
        return list(set(contribs))

    def get_tasks(self):
        return self.tasks
    
    def get_categories(self):
        cat = [c for t in self.tasks for c in t.cat]
        return list(set(cat))

    def get_modification_dates(self):
        return pd.unique( sorted([d for t in self.get_tasks() for d in t.get_modification_dates()]) ).tolist()
    
    def get_state(self,date=''):
        if (not date): date=self.get_modification_dates[-1]
        res=self.__copy__(self)
        res.tasks=[]
        for t in self.tasks:
            task_dates=t.get_modification_dates()
            if (date>=task_dates[0] and not t.is_completed(date)):
                min_index = np.argmin([abs(date-d) for d in task_dates])
                closest_date=task_dates[min_index]
                res.add_task(t.get_state(closest_date))
            else: continue
        return res
        
    def dataframe(self):
        return pd.DataFrame()
