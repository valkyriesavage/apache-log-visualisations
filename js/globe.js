var globe = null;

function initialize_globe() {
    var globe_container = document.getElementById('globe');
    globe = new DAT.Globe(globe_container);
    data = ready_data(institutions);
    map_globe_spikes(data);
}

function ready_data(institutions) {
    data = [];
    for (var i = 0; i < institutions.length; i++) {
        inst = institutions[i];
        data.push([inst.institution,
                    [inst.latitude, inst.longitude, inst.magnitude]]);
    }
}

function map_globe_spikes(data) {
      for (var i = 0; i < data.length; i++) {
        globe.addData(data[i][1], 'magnitude', data[i][0]);
      }
      globe.createPoints();
      globe.animate();
}
