var projection = ol.proj.get("EPSG:3857");
var projectionExtent = projection.getExtent();
var s = ol.extent.getWidth(this.projectionExtent) / 256;
var matrixSet = "mercator";
var resolutions = new Array(21);
var matrixIds = new Array(21);
for (var c = 0; c < 21; ++c)
    resolutions[c] = s / Math.pow(2, c),
    matrixIds[c] = matrixSet + ":" + c;
var m = new ol.tilegrid.WMTS({
    origin: ol.extent.getTopLeft(projectionExtent),
    resolutions: resolutions,
    matrixIds: matrixIds
});

var map = new ol.Map({
  target: 'map-container',
  layers: [
    new ol.layer.Tile({
      name: "street",
      canDelete: "no",
      visible: !0,
      source: new ol.source.WMTS({
          url: "https://kmi.dpaw.wa.gov.au/geoserver/gwc/service/wmts",
          format: "image/png",
          layer: "public:mapbox-streets",
          matrixSet: matrixSet,
          projection: projection,
          tileGrid: m
      })

        // url: "https://kmi.dpaw.wa.gov.au/geoserver/gwc/service/wmts",
        // format: "image/png",
        // layer: "public:mapbox-streets",
        // style: 'default',
        // projection: 'EPSG:3857',
    }),
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([120, -24.5]),
    zoom: 5.2,
  }),
});

var url = '/api/catalogue/entries/'+id+'/layer';

var vectorSource = new ol.source.Vector({
  loader: function(extent, resolution, projection) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onload = function() {
      if (xhr.status == 200) {
        $('#map-loading').hide();
        var data = JSON.parse(xhr.responseText);
        delete data.crs;
        var features = new ol.format.GeoJSON().readFeatures(data, { featureProjection: 'EPSG:3857' });
        vectorSource.addFeatures(features);
      } else {
        $('#map-loading').css("color", "red")
        $('#map-loading').css("border-color", "red")
        $('#map-loading').html("fail to load");
      }
    };
    xhr.send();
  },
});

var vectorLayer = new ol.layer.Vector({ source: vectorSource });
map.addLayer(vectorLayer);