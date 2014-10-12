from django.shortcuts import render, render_to_response
import admin
import json

from CreditCard import CreditCard
from User import User
from Purchase import Purchase

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

data = open('cards1.json', 'r')
cards_json = json.load(data)

cards = []
for card in cards_json:
  credcard = CreditCard(card['t'], card['number'], card['reward'], card['rewardType'], card['sReward'], card['stores'],
      card['dRewards'], int(card['byear']), int(card['bmonth']), int(card['bdate']), int(card['eyear']), int(card['emonth']), int(card['edate']),
      card['moneyConversion'], int(card['limit']), card['description'])
  cards.append(credcard)

_user = User('Bruce', 'Wayne', cards, [1, 1, 1, 1, 1])

merchants_list = []

def ajax_get_data(request):
  if request.is_ajax() or request.method == 'POST':
    location = admin.GetLocation(request.POST['input'])
    location = json.loads(location)

    merchants = []

    if location['results']:
      coords = location['results'][0]['geometry']['location']
      merchants = admin.LocateMerchants(coords['lat'], coords['lng'], 1, 10)

    if merchants:
      merchants_list = merchants

    return HttpResponse(json.dumps({'merchants': merchants, 'location':location, 'cards':cards_json}), content_type="application/json")
  else:
    return HttpResponse('fail')

def ajax_get_location(request):
  if request.is_ajax() or request.method == 'POST':
    location = admin.GetLocation(request.POST['location'])
    location = json.loads(location)

    merchants = []

    if location['results']:
      coords = location['results'][0]['geometry']['location']
      merchants = admin.LocateMerchants(coords['lat'], coords['lng'], 1, 10)

    if merchants:
      merchants_list = merchants

    return HttpResponse(json.dumps({'merchants': merchants, 'location':location}), content_type="application/json")
  else:
    return HttpResponse('fail')

def ajax_get_recommendation(request):
  if request.is_ajax() or request.method == 'POST' and cards_json and merchants_list:
    (card, reward) = admin.get_recommendation(request.POST['store'], request.POST['category'], _user)
    return HttpResponse(json.dumps({'recommendation':card, 'reward':reward}), content_type="application/json")
  else:
    return HttpResponse('fail')



