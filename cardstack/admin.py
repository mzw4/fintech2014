import requests, json
import httplib
import urllib,urllib2, urlparse, base64
from oauthlib import oauth1
import xml.etree.ElementTree as ET

def get_addr(latlng):
  params = dict(
    key='AIzaSyBR_ITmkxEZzk0za75DWVFoTva_IryImi0',
    latlng=latlng
  )
  headers = {'content-type': 'application/json'}

  r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
  print r.text

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
        'Radius':1,
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

    merchants = ET.fromstring(response)
    print response

    for merchant in merchants.findall('Merchant'):
      print merchant.find('Name').text + ' ' + merchant.find('Category').text
      features = merchant.find('Features')
      if features:
        print features.text
      # print merchant.find('Features').find('Cashback').find('MaximumAmount').text

LocateMerchants(41.588006, -87.440855, 1, 10)



