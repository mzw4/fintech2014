import requests, json
import httplib
import urllib,urllib2, urlparse, base64
from oauthlib import oauth1
import xml.etree.ElementTree as ET
import time
from datetime import date

from Purchase import Purchase

GEOLOC_API_KEY = 'AIzaSyBR_ITmkxEZzk0za75DWVFoTva_IryImi0'

def FindAddr(lat, lng):
  params = dict(
    key=GEOLOC_API_KEY,
    latlng=str(lat) + ',' + str(lng)
  )
  headers = {'content-type': 'application/json'}
  r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
  return r.text

def GetLocation(input):
  params = dict(
    key=GEOLOC_API_KEY,
    address=input
  )
  headers = {'content-type': 'application/json'}
  r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
  return r.text

# get_addr("40.714224,-73.961452")

def LocateMerchants(Lat, Lon, pageOffset, pageLength):
    response = ''
    # MASTERCARD PROD CLIENT KEY
    client_key='YC1MU_DP-HqxYAy7qAarr2CiUkf-eKWvlYcymhob063ff9f2!50643436664e675049674b694e444b436857546b6b413d3d'
    # PROD API ENDPOINT
    url = "https://sandbox.api.mastercard.com/merchants/v1/merchant"

    # SET THE REQUEST PARAMETERS
    params = {
        'Format': 'XML',
        'PageLength': pageLength,
        'PageOffset': pageOffset,
        'Country': 'USA',
        'Latitude': Lat,
        'Longitude': Lon,
        'DistanceUnit': 'mile',
        'Radius':10000,
        # 'CountrySubdivision':'NY',
        # 'AddressLine1':'42 Elm Avenue',
        # 'AddressLine2':'Suite 101',
        # 'City':'New York',
        # 'PostalCode':'07114',
    }

    # PUT THE URL TOGETHER WITH THE PARAMS
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    # ENCODE THE URL
    url_parts[4] = urllib.urlencode(query)
    
    # THIS IS THE FINAL URL W/PARAMS
    u = urlparse.urlunparse(url_parts)
    
    # BUILD THE REQUEST
    client = oauth1.Client(client_key,
         signature_method=oauth1.SIGNATURE_RSA,
         rsa_key=open('MCKey.pem').read()
         )
    
    # SIGN THE REQUEST
    uri, headers, body = client.sign(u)

    # PARSE THE AUTHORIZATION HEADER FOR USE BELOW
    for k,v in headers.iteritems():
        h = "%s" % (v)
    
    # BUILD THE REQUEST HANDLER & OPENER
    handler=urllib2.HTTPSHandler(debuglevel=1)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    # BUILD THE REQUEST
    request = urllib2.Request(u)
    # ADD THE AUTHORIZATION HEADER
    request.add_header('Authorization',h)
    # SEND THE REQUEST AND READ THE RESULT - ALSO CATCH ERRORS
    try:
        response = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        print ('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        print ('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        print ('HTTPException')
    except Exception:
        import traceback
        print ('generic exception: ' + traceback.format_exc())

    if not response:
      return
    merchants = ET.fromstring(response)
    merchant_list = merchants.findall('Merchant')

    if not merchant_list:
      return []

    results = []
    for merchant in merchant_list:
      if merchant.find('Name').text and merchant.find('Category').text:
        print merchant.find('Name').text + ' ' + merchant.find('Category').text

        results.append({
          'name': merchant.find('Name').text,
          'category': merchant.find('Category').text,
          'distance': merchant.find('Location').find('Distance').text,
          })

    return results

def get_recommendation(store, category, user):
  today = date.today()
  (recommendation, reward) = user.optimalCard(Purchase(category, store, today.year, today.month, today.day))
  reward = user.getUtilityType(reward)
  return (recommendation.type, recommendation.description)



