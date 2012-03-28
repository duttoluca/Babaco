from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

MIN_ATTENTION = 0
MAX_ATTENTION = 100
MIN_TIME = 0
MAX_TIME = 360

class Recipe(models.Model):
    name = models.CharField(max_length=300, verbose_name='Nome ricetta')
    description = models.TextField(blank=True,
                                   max_length=4000,
                                   verbose_name='Descrizione ricetta')
    is_active = models.BooleanField(default=True)
    ins_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Data inserimento')
    # prevediamo una fotina per la ricetta?
    #Per ora solo un placeholder, bisogna installare PIL e impostare upload
    #image = models.ImageField(upload_to="",
    #                          verbose_name='Immagine Main Ricetta')
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
    recipe = models.ForeignKey(Recipe, verbose_name='Ricetta')
    parents = models.ManyToManyField('self', blank=True, null=True,
                                     verbose_name='Task padri',
                                     symmetrical=False)
    name = models.CharField(max_length=200, verbose_name='Nome task')
    description = models.TextField(blank=True,
                                   max_length=4000,
                                   verbose_name='Descrizione task')
    # ipotizzo 360 minuti max per il singolo task
    time_needed = models.IntegerField(validators=[MinValueValidator(MIN_TIME),
                                                  MaxValueValidator(MAX_TIME)],
                                      verbose_name='Tempo necessario')
    attention_needed = models.IntegerField(validators=[MinValueValidator(MIN_ATTENTION),
                                                       MaxValueValidator(MAX_ATTENTION)],
                                        verbose_name='Attenzione necessaria')
    is_active = models.BooleanField(default=True)
    ins_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Data inserimento')
    # questi campi non dovrebbero servire nel model, li tengo qui per ora
    startTime = models.IntegerField()
    stopTime = models.IntegerField()

    def __unicode__(self):
        return "%s" % (self.name)

    @property
    def hasParents(self):
        if self.parents.count() > 0:
            return True
        return False
