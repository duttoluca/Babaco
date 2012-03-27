from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    name = models.CharField(max_length=300, verbose_name = 'Nome ricetta')
    description = models.TextField(blank = True, max_length = 4000, verbose_name = 'Descrizione ricetta' )
    is_active = models.BooleanField(default = True)
    ins_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Data inserimento')
    # prevediamo una fotina per la ricetta? Per ora solo un placeholder, bisogna installare PIL e impostare upload
    #image = models.ImageField(upload_to="", verbose_name = 'Immagine Main Ricetta')
    image = None
    
    class Meta:
        verbose_name = 'Ricetta'
        verbose_name_plural = 'Ricette'
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('recipe_view', [str(self.id)]) 
       

class Task(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name = 'Ricetta')
    #parent = models.ForeignKey('self', blank=True, null=True, verbose_name = 'Task padre')
    parents = models.ManyToManyField('self', blank=True, null=True, verbose_name = 'Task padri', symmetrical = False)
    name = models.CharField(max_length=200, verbose_name = 'Nome task')
    description = models.TextField(blank = True, max_length = 4000, verbose_name = 'Descrizione task' )
    # ipotizzo 360 minuti max per il singolo task
    time_needed = models.IntegerField( validators = [MinValueValidator(0), MaxValueValidator(360)], verbose_name = 'Tempo necessario')
    attention_needed = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(100)], verbose_name = 'Attenzione necessaria')
    is_active = models.BooleanField(default = True)
    ins_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Data inserimento')
    # questi campi non dovrebbero servire nel model, li tengo qui per ora
    startTime = models.IntegerField()
    stopTime = models.IntegerField()
    # questo campo non fa nulla
    MAX_ATTENTION = 100 

    def __unicode__(self):
        return "%s" % (self.name)
    
    @property
    def hasParents(self):
        if self.parents.count() > 0:
            return True
        return False


    