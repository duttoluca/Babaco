from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from models import Recipe

#def index(request):
#    #l = get_list_or_404(Recipe, is_active = True)
#    # non voglio 404 se non ho ricette!
#    l = Recipe.objects.filter(is_active=True).order_by('-ins_date')
#    return render_to_response('recipe/index.html',{'list': l}, context_instance=RequestContext(request))

#def task(request, task):
#    t = get_object_or_404(Task, pk=int(task))
#    return render_to_response('recipe/task_details.html', {'req': t }, context_instance = RequestContext(request) )


def recipeDetails(request, recipe):
    r = get_object_or_404(Recipe, pk=int(recipe))
    return render_to_response('recipe/recipe_details.html',
                              {'recipe': r},
                              context_instance=RequestContext(request))
