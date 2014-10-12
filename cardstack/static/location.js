var map;
var cur_location;

var cur_store;
var cur_store_category;

var csrftoken = $.cookie('csrftoken');

var $nearestMerchants;
var $userCards;

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
  $userCards = $('#user_cards');

  google.maps.event.addDomListener(window, "load", initialize);

  $('#nearest_toggle', 'body').on('click', function(e) {
    $($nearestMerchants).slideToggle(200);
  });
  $('#cards_toggle', 'body').on('click', function(e) {
    $($userCards).slideToggle(200);
  });

  $(document).on('click', '#recommend', function() {
    getRecommendation();
  });

  $(document).on('click', '#other_options_button', function() {
    $('html, body').animate({
      scrollTop: $("#other_options").offset().top
    }, 200);
  });

  $('#loc_form').submit(function(event) {
    event.preventDefault();
    var text = $('#loc_input').val();
    getLocation($('#loc_input').val());
  });

  $(document).on('click', '#nearest_merchants .list-group-item', function() {
    $('#current_store').html($(this).text().split(',')[0]);
    cur_store_category = $(this).data('category');
    cur_store = $(this).text().split(',')[0];
  })
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
        input: coords.lat + ',' + coords.lng
      },
      success: function(data){
        if(data && data.merchants && data.location && data.cards) {
          if(data.merchants.length !== 0) {
            cur_store = data.merchants[0].name;
            cur_store_category = data.merchants[0].category;
            $('#current_store').html(cur_store)

            $.each(data.merchants, function(i, entry) {
              $nearestMerchants.append('<li class="list-group-item" data-category=' + entry.category + '>' + entry.name + ', ' + entry.distance + ' miles away, ' + entry.category + '</li>');
            });
          } else {
            $('#current_store').html('None')
            $nearestMerchants.append('<li class="list-group-item">None</li>');
          }

          $('#loc_input').val(data.location.results[0].formatted_address)

          $('#info').fadeIn('fast');
          $($userCards).slideToggle(200);

          $.each(data.cards, function(i, card) {
            $('#card_table').append('<tr><td>' + card.t + '</td><td>' + card.description + '</td></tr>');
            $('#user_cards').append('<li class="list-group-item">' + card.t + '</li>');
          });
        }
      },
      error: function(jqXHR, textStatus, errorThrown){
          alert(errorThrown);
      }
  });
}

function getLocation(location) {
  $.ajax({
      type: "POST",
      url:"/get_location/",
      data: {
        location: location
      },
      success: function(data){
        if(data && data.location) {
          var coords = data.location.results[0].geometry.location;
          cur_location = new google.maps.LatLng(coords.lat, coords.lng);

          var infowindow = new google.maps.InfoWindow({
            map: map,
            position: cur_location,
            content: 'You are here!'
          });

          map.setCenter(cur_location);

          $nearestMerchants.html('');
          if(data.merchants.length !== 0) {
            cur_store = data.merchants[0].name;
            cur_store_category = data.merchants[0].category;
            $('#current_store').html(cur_store)

            $.each(data.merchants, function(i, entry) {
              $nearestMerchants.append('<li class="list-group-item" data-category=' + entry.category.replace(' ','') + '>' + entry.name + ', ' + entry.distance + ' miles away, ' + entry.category + '</li>');
            });
          } else {
            $('#current_store').html('None')
            $nearestMerchants.append('<li class="list-group-item">None</li>');
          }
        }
      },
      error: function(jqXHR, textStatus, errorThrown){
          alert(errorThrown);
      }
  });
}

function getRecommendation() {
  $.ajax({
      type: "POST",
      url:"/get_recommendation/",
      data: {
        store: cur_store,
        category: cur_store_category
      },
      success: function(data){
        if(data && data.recommendation) {
          $('#recommendation').fadeIn('fast');
          $('#other_options').fadeIn('fast');
          
          $('#recommended_card').html(data.recommendation);
          $('#rewards').html(data.reward)

          $('html, body').animate({
            scrollTop: $("#recommendation").offset().top
          }, 200);
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





