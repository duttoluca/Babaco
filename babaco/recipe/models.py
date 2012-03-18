from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)

class Task(models.Model):
    recipe = models.ForeignKey(Recipe)
    name = models.CharField(max_length=200)
    taskId = models.IntegerField()
    time = models.IntegerField()
    attention = models.IntegerField()
    parent = models.IntegerField()
    startTime = models.IntegerField()
    stopTime = models.IntegerField()
    active = models.IntegerField()
    MAX_ATTENTION = 100

#    def __init__(self, task_id, name, time, attention, parent=-1):
#        self.name = name
#        self.task_id = task_id
#        self.time = int(time)
#        if attention > self.MAX_ATTENTION:
#            attention = self.MAX_ATTENTION
#        elif attention < 0:
#            attention = 0
#        self.attention = int(attention)
#        self.parent = parent
#        self.startTime = -1
#        self.stopTime = -1
#        self.active = 1

    def __str__(self):
        if self.parent == -1:
            return "%s" % (self.name)
        return "%s figlio di %s" % (self.name, self.parent.name)

    def __repr__(self):
    	return "%s" % (self.name)
