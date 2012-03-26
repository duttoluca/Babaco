from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'babaco.views.home', name='home'),
    # url(r'^babaco/', include('babaco.foo.urls')),
    url(r'^$', 'recipe.views.index', name = 'home'),
    url(r'^recipe/(\d+)/$', 'recipe.views.recipeDetails' , name = "recipe_view"),
    #url(r'^tasks/(\d+)/$', 'recipe.views.task'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
)

