var image = new ol.style.Circle({
        radius: 5,
        fill: null,
        stroke: new ol.style.Stroke({color: 'red', width: 1})
      });

      var style = {
        'Point': new ol.style.Style({
          image: image
        }),
        'LineString': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'green',
            width: 1
          })
        }),
        'MultiLineString': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'green',
            width: 1
          })
        }),
        'MultiPoint': new ol.style.Style({
          image: image
        }),
        'MultiPolygon': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'yellow',
            width: 1
          }),
          fill: new ol.style.Fill({
            color: 'rgba(255, 255, 0, 0.1)'
          })
        }),
        'Polygon': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'blue',
            lineDash: [4],
            width: 3
          }),
          fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.1)'
          })
        }),
        'GeometryCollection': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'magenta',
            width: 2
          }),
          fill: new ol.style.Fill({
            color: 'magenta'
          }),
          image: new ol.style.Circle({
            radius: 10,
            fill: null,
            stroke: new ol.style.Stroke({
              color: 'magenta'
            })
          })
        }),
        'Circle': new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'red',
            width: 2
          }),
          fill: new ol.style.Fill({
            color: 'rgba(255,0,0,0.2)'
          })
        })
      };

// var track_source = new ol.source.Vector({
//   url: 'static/assets/trackie/map.gpx',
//   format: new ol.format.GPX()
// });

var track_source = new ol.source.Vector();

var track_layer = new ol.layer.Vector({
  source: track_source,
  style: function(feature) {
    return style[feature.getGeometry().getType()];
  }
});

$.ajax({
  method: 'GET',
  url: 'https://openlayers.org/en/v3.20.1/examples/data/gpx/fells_loop.gpx'
}).done(function(json){
  console.log("done");
  var format = new ol.format.GPX();
  var features = format.readFeatures(json, {featureProjection: 'EPSG:3857'})
  track_source.addFeatures(features);
});

var tile = new ol.layer.Tile({
  source: new ol.source.OSM()
});

var map = new ol.Map({
  target: 'map',
  layers: [
    tile,
    track_layer
  ],
  view: new ol.View({
    center: [-7916041.528716288, 5228379.045749711],
    zoom: 1
  })
});
