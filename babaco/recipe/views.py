# Create your views here.
from django.template import Context, loader
from recipe.models import Task
from django.http import HttpResponse, Http404

def index(request):
        return HttpResponse("Hello, welcome to Babaco")

def task(request, task_id):
	try:
		t = Task.objects.get (pk = task_id)
	except Task.DoesNotExist:
		raise Http404
	return HttpResponse("This is task " + repr(t));
