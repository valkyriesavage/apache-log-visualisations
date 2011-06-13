var map = null;

function initialize_map() {
    var SLAC = new google.maps.LatLng(37.418265, -122.2008149);
    var origin = new google.maps.LatLng(15, 0);
    var worldCentredOnOrigin = {
      zoom: 2,
      center: origin,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
            worldCentredOnOrigin);
    wait_a_moment();
}

function 

function map_new_point() {
    if (pointsToMap.length < 1) {
        return 1;
    }
    if (!running) {
        return 0;
    }
    point_and_search = pointsToMap.shift();
    latitude = point_and_search['latitude'];
    longitude = point_and_search['longitude'];
    search = point_and_search['search'];
    drop_point(latitude, longitude, search);
}

function drop_point(latitude, longitude, search) {
    inst = new google.maps.LatLng(latitude, longitude);
}
