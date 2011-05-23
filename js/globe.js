var globe = null;

function initialize_globe() {
    var globe_container = document.getElementById('globe');
    globe = new DAT.Globe(globe_container);
    request_globe_ajax();
}

function request_globe_ajax(){
    $.getJSON('http://inspire-viz.com/python/paperswebglglobe.py',
                {},
                map_globe_spikes);
}

function map_globe_spikes(data) {
      for (i = 0; i < data.length; i++) {
        globe.addData(data[i][1], 'magnitude', data[i][0]);
      }
      globe.createPoints();
      globe.animate();
}
