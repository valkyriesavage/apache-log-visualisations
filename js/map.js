var map = null;
var ajaxRequest = null;
var pointsToMap = [];
var mapped = 0;

function initialize_map() {
    var SLAC = new google.maps.LatLng(37.418265, -122.2008149);
    var worldCentredOnSLAC = {
      zoom: 6,
      center: SLAC,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
            worldCentredOnSLAC);
    request_lat_longs_ajax();
}

function request_lat_longs_ajax(timer){
    $.getJSON('http://localhost/cgi-bin/searchesmap.py',
              { 'mapped' :  mapped },
              read_lat_longs_ajax);
    console.log('request sent to server');
    wait_a_moment(timer);
}

function wait_a_moment(timer) {
    setTimeout("request_lat_longs_ajax()", 2000);
    setTimeout("map_new_point()", 2000);
}

function read_lat_longs_ajax(data, textStatus, jqXHR) {
    if (data[0] == "") {
        console.log('no response from server')
    }
    else {
        console.log('points retrieved');
        for (var i = 0; i < data.length - 1; i++) {
            pointsToMap.push(data[i]);
        }
    }
}

function map_new_point() {
    if (pointsToMap.length < 1) {
        console.log('no points to map');
        return 1;
    }
    point_and_search = pointsToMap.shift();
    latitude = point_and_search['latitude'];
    longitude = point_and_search['longitude'];
    search = point_and_search['search'];
    drop_point(map, latitude, longitude, search);
    mapped += 1;
}

function drop_point(map, latitude, longitude, search) {
    accessedPoint = new google.maps.LatLng(latitude, longitude);
    marker = new google.maps.Marker({
        map:map,
        draggable:true,
        animation: google.maps.Animation.DROP,
        position: accessedPoint,
        icon: 'http://localhost/img/beta.png',
        title: search,
    });
    map.setCenter(accessedPoint);
}
