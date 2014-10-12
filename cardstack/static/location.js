var map;
var cur_location;

var csrftoken = $.cookie('csrftoken');

var $nearestMerchants;

// ------------------------ Init ------------------------

$(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  $nearestMerchants = $('#nearest_merchants');
  google.maps.event.addDomListener(window, "load", initialize);
});

// ------------------------ Functions ------------------------

function initialize() {
  var mapOptions = {
    zoom: 10
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  // Try HTML5 geolocation
  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      cur_location = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);

      var infowindow = new google.maps.InfoWindow({
        map: map,
        position: cur_location,
        content: 'You are here!'
      });

      map.setCenter(cur_location);

      $('#cur_location #lat').html(cur_location.k);
      $('#cur_location #lng').html(cur_location.B);

      getData( { lat: cur_location.k, lng: cur_location.B} );
    }, function() {
      handleNoGeolocation(true);
    });
  } else {
    // Browser doesn't support Geolocation
    handleNoGeolocation(false);
  }
}

function handleNoGeolocation(errorFlag) {
  if (errorFlag) {
    var content = 'Error: The Geolocation service failed.';
  } else {
    var content = 'Error: Your browser doesn\'t support geolocation.';
  }

  var options = {
    map: map,
    position: new google.maps.LatLng(60, 105),
    content: content
  };

  var infowindow = new google.maps.InfoWindow(options);
  map.setCenter(options.position);
}

function getData(coords) {
  $.ajax({
      type: "POST",
      url:"/get_data/",
      data: {
        lat: coords.lat,
        lng: coords.lng
      },
      success: function(data){
        if(data && data.merchants && data.address && data.cards) {
          $.each(data.merchants, function(i, entry) {
            $nearestMerchants.append('<li class="list-group-item">Merchant: ' + entry.name + ', Category: ' + entry.category + ', Distance: '
              + entry.distance + ' mi. </li>');
          });

          $('#addr').html(data.address.results[0].formatted_address);   
          $('#info').fadeIn('fast');
        }
      },
      error: function(jqXHR, textStatus, errorThrown){
          alert(errorThrown);
      }
  });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}





