#!/bin/python

from string import *

class Factory:
  last_id = 0
  
  def __init__ (self, id=0):
    self.last_id = id
  
  def getId (self):
    id = self.last_id
    self.last_id = self.last_id + 1
    return id

class Task:
  name = ""
  parent = -1
  id = 0
  time = 0
  attention = 0
  max = 99
  
  def __init__ (self, f, n, t, a, p=-1):
    self.id = f.getId()
    self.name = n
    self.time = t
    self.attention = a
    self.parent = p
  
  def toString(self):
    if (self.parent == -1):
      print "(%d) %s: %d min at %d" % (self.id, self.name, self.time, self.attention)
    else:
      print "(%d) %s: %d min at %d after %s" % (self.id, self.name, self.time, self.attention, self.parent.name)

  def isUsable (self, _used):
    if self.parent != -1:
      if not self.parent.id in _used:
        return False
    
    return True

  def isUsableMulti (self, _used, now):
#    print "considering " + repr (self.name) + " [[ "+repr(self.parent)+" ]]",
    if self.parent != -1:
      if self.parent.id in _used:
#        print " \t\t parent " + self.parent.name + " finishes at: " + repr(_used[self.parent.id]) + " \t\t can we place at " + repr(now) + "?",
        if _used[self.parent.id] > now:
#          print "   NO!"
          return False
        else:
#          print "   YES!"
          return True
      else:
        return False
#    print "\t no parent, we can place it at " + repr(now)
    return True
  
  def isPlacable (self, _time,):
    _total_attention = 0
        
    if _time:
      for v in _time:
        _total_attention += v.attention
    
    if (self.max - _total_attention) > self.attention:
      return True
    
    return False
    

  def __repr__(self):
    return repr(self.id)
    
class Prepare:
  tasks = {}
  name = ""
  
  def __init__ (self, n):
    self.name = n
    
  def addTask (self, t):
    self.tasks[t.id] = t
  
  def toString (self):
    print "-- %s --" % (self.name)
    for t in self.tasks:
      self.tasks[t].toString()
  
  def schedule (self):
    total_time = 0

    for t in self.tasks:
      total_time += self.tasks[t].time
    
    print total_time
  
  
  def useTask (self, _tasks, _used, time, step):
    for k,v in _tasks.items():
      # Move task form available to used
      if v.isUsable (_used):
        _used [step] = v
        time += v.time
        del _tasks [k]
  
        # If we finished the available tasks, we print the procedure
        if not _tasks:
#          print "(step %d) -- finished in %d" % (step, time)
          for k1,v1 in _used.items():
            print v1.name
#          print "----------------- "
        # otherwise, we recurse
        else:

          step += 1
          self.useTask(_tasks, _used, time, step)
          step -= 1
      
        # backtrace
        _tasks [k] = v
        time -= v.time
        del _used [step]
  
  def scheduleAll (self):
    time = 0
    used_tasks = {}
    available_tasks = self.tasks
    self.useTask (available_tasks, {}, time, 0)

  def out (self, _time, _tasks):
    print "\n vvvvvvvvvvv"
    for t_id, t_start in _tasks.items():
      print t_id
      name = ''
      for k,v in _time.items():
        found = False
        for t in v:
          if t.id == t_id:
            found = True
            name = t.name
        
        if found:
          print '-',
        else:
          print ' ',
        
      print ' ==> ' + name

    print "^^^^^^^^^^^\n"
    
  def out2 (self, _time, _tasks):
    print "vvvvvvvvvvv"
    for k,v in _time.items():
      if k!=0:
	print "%d\t"%(k),
	_tot = 0
	for i in range (5):
	
	  s = "\t"
	  for t in v:
	    if t.id == i:
	      s = "\t" + repr(t.name) + "[" + repr (t.attention) + "] \t\t\t"
	      _tot += t.attention
	    if t.id == -1:
	      s = "Dummy"
	  
	  print s,
	print "    ==> %d" % (_tot)
    print "^^^^^^^^^^^"


  def useTaskMulti (self, _tasks, _used, _time, _best, _best_time):
    # backup for backtrace
    _time_old = _time.copy()
    _tasks_old = _tasks.copy()
    
    for k,v in _tasks.items():
      # for each not used yet tasks
      
      # at worst we put the task at the end of the current preparation
      _last = len(_time)
      to_place = _last

      first_possible_time = 0
      # searching when its parents finish
      for p_time, p_val_list in _time.items():

        for p_val in p_val_list:
          if p_val == v.parent:
            first_possible_time = p_time

      if first_possible_time == 0:
        first_possible_time = -1 # dirty hack, find a better solution
      
      for i in _time:
        # we search a better place
        if (i > first_possible_time) and (v.isPlacable (_time[i])):
          # if at some point we can place it next to an already placed task, we do it
          # problem here. We assume that if a task if placable at beginning, it will be always placable
          if (to_place == _last):
            to_place = i
      
#      print "verifying if " + repr(v.name) + " is placable [[" + repr(v.parent) + "]]"
      if v.isUsableMulti (_used, to_place):
        # actual placing: we put a reference to the task for each minute of the preparation
        for i in range (v.time):
          if not (to_place + i) in _time.keys(): # this is ugly, can we do it better?
            _time[to_place + i] = []
          _time[to_place + i].append(v)
        
        # we have allocated the task, so we make it not available
        del _tasks [k]
        _used[k] = to_place + i
        
        # debug
#        self.out (_time, _used)
#        print "Added " + repr(v.name)
#        raw_input('Press Enter')

        # we can continue with the next task ..
        self.useTaskMulti (_tasks, _used, _time, _best, _best_time)
        
        # backtrace: we remove the task from the preparation
#        print v.parent
#        print _used
#        print "\n\n\n 	vvvvvvvvvvvvvvvv"
#        for x,i in _tasks.items():
#          print i.id
#          print i.name
#          if i.parent != -1:
#            print "[[" + i.parent.name + "]]"
#          print "-\n"
        
        for i in range (v.time):
          _time[to_place + i].remove(v)
          if len(_time[to_place + i]) == 0:
            del _time[to_place + i]
        _tasks[k] = v
        del _used[k]


#        print "================================== added " + v.name

#        print "\n"
#        for x,i in _tasks.items():
#          print i.id
#          print i.name
#          if i.parent != -1:
#            print "[[" + i.parent.name + "]]"
#          print "---"
#        raw_input('ok');  
        
#        for i,x in _tasks.items():
#          if x.parent != -1:
#            print x.name + "  <--  " + x.parent.name
#          else:
#            print x.name
          
        # debug
#        self.out (_time, _used)
#        print "Removed " + repr(v.name)
#        raw_input('Press Enter')
    
    # did we finish?
    if (len(_tasks)==0):
      if len(_time) < _best_time:
        _best = _time.copy()
        _best_time = len(_best)
        
        self.out (_best, _used)
        print "========= finished in " + repr(len(_best))
        raw_input('Press Enter for next scheduling')
  
  def scheduleMulti (self):
    available_tasks = self.tasks
    used = {}
    
      # adding a dummy task to fix the beginning of preparation
    f_dummy = Factory(-1)
    t_dummy = Task(f_dummy, "Dummy task", 1, 99)
    used[0] = []
    used[0].append (t_dummy)
    t_dummy.toString()
    
    best = {}
    best_time = 999
    
    # find the best schedule
    self.useTaskMulti (available_tasks, used, {}, best, best_time)
    
    
    
    


### MAIN ###

f = Factory()

t1 = Task(f, "affettare cipolla", 10, 80)
t2 = Task(f, "fare soffritto", 5, 10, t1)
t3 = Task(f, "bollire acqua", 15, 10)
t4 = Task(f, "cuocere pasta", 10, 10, t3)
t5 = Task(f, "grattugiare formaggio", 5, 80)

t6 = Task(f, "battere carne", 10, 80)
t7 = Task(f, "friggere carne", 5, 10, t6)

t8 = Task(f,"pelare e tagliare le patate in pezzi grossi",15,40)
t9 = Task(f,"condire le patate con olio sale e rosmarino",8,80,t8)
t10 = Task(f,"condire il pollo con olio e aromi tipo Ariosto",8,80)
t11 = Task(f,"in una teglia antiaderente adagiare le patate",2,26,t9)
t12 = Task(f,"adagiare il pollo sulle patate",2,26,t11)
t13 = Task(f,"cuocere in forno per 60 minuti",10,10,t12)

r = Prepare("recipe")

r.addTask (t1)
r.addTask (t2)
r.addTask (t3)
r.addTask (t4)
r.addTask (t5)
r.addTask (t6)
r.addTask (t7)
r.addTask (t8)
r.addTask (t9)
r.addTask (t10)
r.addTask (t11)
r.addTask (t12)
r.addTask (t13)

#r.toString()

#r.schedule()

r.scheduleMulti()


