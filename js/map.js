var map = null;
var ajaxRequest = null;
var pointsToMap = [];

function initialize_map() {
    var SLAC = new google.maps.LatLng(37.418265, -122.2008149);
    var worldCentredOnSLAC = {
      zoom: 5,
      center: SLAC,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
            worldCentredOnSLAC);
    read_lat_longs_ajax('noneayobeeswax');
}

function read_lat_longs_ajax(timer){
    try{
        // Opera 8.0+, Firefox, Safari
        ajaxRequest = new XMLHttpRequest();
        console.log('we have a request');
    } catch (e) {
        // Internet Explorer Browsers
        try{
            ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try{
                ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {
                // Something went wrong
                console.log("Get a real browser.");
                console.log(e);
                return false;
            }
        }
    }
    ajaxRequest.onreadystatechange = get_new_points;
    ajaxRequest.open("POST", "http://localhost/cgi-bin/searchesmap.py", true);
    ajaxRequest.send(null);
    console.log('request to server sent');
    wait_a_moment(timer);
}

function wait_a_moment(timer) {
    t = setTimeout("read_lat_longs_ajax()", 4000);
    t = setTimeout("map_new_point()", 4000);
}

function get_new_points() {
    if (ajaxRequest.readyState == 4) {
        console.log(ajaxRequest);
        console.log(ajaxRequest.responseText);
        allPoints = ajaxRequest.responseText.split("\n");
        console.log(allPoints);
        eval(allPoints);
        console.log(allPoints);
        for (i = pointsToMap.length - 1; i < allPoints.length - 1; i++) {
            pointsToMap.push(allPoints[i]);
        }
        console.log('points retrieved');
    }
    else {
        console.log(ajaxRequest);
    }
}

function map_new_point() {
    point = pointsToMap.shift();
    console.log(point);
    point = point.split(' ');
    latitude = point[0];
    longitude = point[1];
    drop_point(map, latitude, longitude);
}

function drop_point(map, latitude, longitude) {
    accessedPoint = new google.maps.LatLng(latitude, longitude);
    marker = new google.maps.Marker({
        map:map,
        draggable:true,
        animation: google.maps.Animation.DROP,
        position: accessedPoint,
        icon: 'http://localhost/img/john-ellis.jpg',
    });
    //map.setCenter(accessedPoint);
}
