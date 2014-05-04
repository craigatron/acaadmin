from django.shortcuts import render
from django.template import RequestContext

def index(request):
  return render(request, 'base.html',
      context_instance=RequestContext(request))
