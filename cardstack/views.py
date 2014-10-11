from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
import datetime

def main(request):
    return render(request, 'index.html')

def spending(request):
    now = datetime.datetime.now()
    # html = "<html><body>It is now %s.</body></html>" % now
    # return render_to_response('polls/detail.html', {'poll': p})
    return render(request, 'spending.html', {'time' : now})
