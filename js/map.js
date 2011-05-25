var map = null;
var clusterer = null;

var ajaxRequest = null;

var pointsToMap = [];
var markersAdded = [];

var live = false;

var requested = -1;

var running = true;
var speed = .7;

function initialize_map(cluster) {
    var SLAC = new google.maps.LatLng(37.418265, -122.2008149);
    var worldCentredOnSLAC = {
      zoom: 2,
      center: SLAC,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
            worldCentredOnSLAC);
    wait_a_moment();
    if (cluster) {
        init_clustering();
    }
}

function init_clustering() {
    clusterer = new MarkerClusterer(map);
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

function toggle_live(button) {
    live = !live;
    for (var i; i = 0; i < markersAdded.length) {
        marker = markersAdded[i];
        marker.setVisible(false);
    }
    markersAdded = [];
    pointsToMap = [];
    if (!live) {
        button.innerHTML = 'live logs';
    }
    else {
        button.innerHTML = 'replay of old logs';
    }
}

function change_speed(newSpeed) {
    speed = newSpeed/10;
}

function update_searched(search) {
    document.getElementById('searched').innerHTML = '<a href="http://inspirebeta.net/search?p=' +
            encodeURI(search.replace(/ /g, '+')) + '">' + search + '</a>';
}

function update_behind_count(current, total) {
    if (live) {
        document.getElementById('count').innerHTML = 'behind by ' + total-current + ' searches';
    }
    else {
        document.getElementById('count').innerHTML = 'search ' + current + '/' + total;
    }
}


function request_lat_longs_ajax(){
    if (running) {
        $.getJSON('http://inspire-viz.com/python/searchesmap.py?mapped='+requested+'&live='+live,
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

    data = pointsToMap.shift();

    totalRows = data[0];

    pointAndSearch = data[1];
    latitude = pointAndSearch['latitude'];
    longitude = pointAndSearch['longitude'];
    search = pointAndSearch['search'];
    timestamp = pointAndSearch['timestamp'];

    update_behind_count(pointAndSearch['id'], totalRows);

    if (requested < 0) {
        requested = pointAndSearch['id'];
    }
    drop_point(latitude, longitude, search, timestamp);
}

function drop_point(latitude, longitude, search) {
    accessedPoint = new google.maps.LatLng(latitude, longitude);
    marker = new google.maps.Marker({
        map:map,
        draggable:true,
        animation: google.maps.Animation.DROP,
        position: accessedPoint,
        title: search,
    });
    marker.click = "update_searched('"+marker.getTitle()+"');";
    update_searched(search);
    markersAdded.push((marker, timestamp));
    if (clusterer) {
        clusterer.addMarker(marker);
    }
}
