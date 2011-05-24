var map = null;
var clusterer = null;

var ajaxRequest = null;

var pointsToMap = [];
var markersAdded = [];

var requested = -1;

var clustering = false;
var running = true;
var speed = .7;

function initialize_map() {
    var SLAC = new google.maps.LatLng(37.418265, -122.2008149);
    var worldCentredOnSLAC = {
      zoom: 2,
      center: SLAC,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
            worldCentredOnSLAC);
    //toggle_clustering();
    wait_a_moment();
}

function toggle_clustering() {
    clustering = !clustering;
    if (clustering) {
        if (!clusterer) {
            clusterer = new MarkerClusterer(map);
        }
        else {
            clusterer.addMarkers(markersAdded);
        }
    }
    else {
        clusterer.clearMarkers();
        for (marker in markersAdded) {
            marker.setVisible(true);
        }
    }
}

function toggle_run(button) {
    running = !running;
    if (!running) {
        button.innerHTML = 'start';
    }
    else {
        button.innerHTML = 'pause';
    }
}

function change_speed(newSpeed) {
    speed = newSpeed/10;
}

function update_searched(search) {
    document.getElementById('searched').innerHTML = '<a href="http://inspirebeta.net/search?p=' +
            encodeURI(search.replace(/ /g, '+')) + '">' + search + '</a>';
}

function request_lat_longs_ajax(){
    if (running) {
        $.getJSON('http://inspire-viz.com/python/searchesmap.py?mapped='+requested,
                  {},
                  read_lat_longs_ajax);
        if (requested > 0) {
            requested += 1;
        }
    }
    wait_a_moment();
}

function wait_a_moment() {
    setTimeout("request_lat_longs_ajax();", speed*3000);
    setTimeout("map_new_point();", speed*3000);
}

function read_lat_longs_ajax(data, textStatus, jqXHR) {
    if (data == null || data.length == 0 || data[0] == "") {
        console.log('no response from server')
    }
    else {
        pointsToMap.push(data);
    }
}

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
    timestamp = point_and_search['timestamp'];
    if (requested < 0) {
        requested = point_and_search['id'];
    }
    drop_point(latitude, longitude, search, timestamp);
}

function drop_point(latitude, longitude, search) {
    accessedPoint = new google.maps.LatLng(latitude, longitude);
    if (search.search('ellis, j') > -1) {
        marker = new google.maps.Marker({
            map:map,
            draggable:true,
            animation: google.maps.Animation.DROP,
            position: accessedPoint,
            icon: 'http://inspire-viz.com/images/john-ellis.jpg',
            title: search,
        });
    }
    else {
        marker = new google.maps.Marker({
            map:map,
            draggable:true,
            animation: google.maps.Animation.DROP,
            position: accessedPoint,
            title: search,
        });
    }
    marker.click = "update_searched('"+marker.title+"');";
    update_searched(search);
    markersAdded.push((marker, timestamp));
    if (clustering) {
        clusterer.addMarker(marker);
    }
}
