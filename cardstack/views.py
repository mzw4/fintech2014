from django.shortcuts import render, render_to_response
import admin
import json

# Create your views here.
from django.http import HttpResponse
import datetime

def main(request):
    return render(request, 'index.html')

def spending(request):
    now = datetime.datetime.now()
    # html = "<html><body>It is now %s.</body></html>" % now
    # return render_to_response('polls/detail.html', {'poll': p})

    return render(request, 'spending.html')

data = open('cards.json', 'r')
cards_json = json.load(data)

def ajax_get_data(request):
  if request.is_ajax() or request.method == 'POST':
    merchants = admin.LocateMerchants(request.POST['lat'], request.POST['lng'], 1, 10)
    address = admin.FindAddr(request.POST['lat'], request.POST['lng'])

    return HttpResponse(json.dumps({'merchants': merchants, 'address':json.loads(address), 'cards':cards_json}), content_type="application/json")
  else:
    return HttpResponse('fail')