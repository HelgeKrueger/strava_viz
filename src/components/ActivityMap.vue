<template>
  <div id="mapid"></div>
</template>

<script>
import "ol/ol.css";

import { Map } from "ol";
import TileLayer from "ol/layer/Tile";
import View from "ol/View";
import LineString from "ol/geom/LineString";
import Polygon from "ol/geom/Polygon";
import Projection from "ol/proj/Projection";
import VectorLayer from "ol/layer/Vector";
import { OSM } from "ol/source";
import Feature from "ol/Feature";
import { fromLonLat } from "ol/proj";
import Polyline from "ol/format/Polyline";
import VectorSource from "ol/source/Vector";

function transformPolyline(polyline) {
  const parser = new Polyline();
  const line = parser.readFeatures(polyline)[0];

  return new Feature({
    geometry: line.getGeometry().transform("EPSG:4326", "EPSG:3857"),
    name: "Line"
  });
}

function createMap(d) {
  const map = new Map({
    target: "mapid",
    layers: [
      new TileLayer({
        source: new OSM()
      })
    ]
  });
  const view = new View({
    center: fromLonLat([11.7271, 48.10963]),
    zoom: 14
  });
  map.setView(view);

  const features = d.polylines.map(x => transformPolyline(x.polyline));
  console.log(features);

  let source = new VectorSource({
    features: features
  });

  view.fit(source.getExtent());

  var layerLines = new VectorLayer({
    source: source
  });

  map.addLayer(layerLines);
  map.render();
}

export default {
  name: "ActivityMap",
  mounted: function() {
    fetch("/api/polylines")
      .then(d => d.json())
      .then(d => {
        createMap(d);
      });
  }
};
</script>

<style>
#mapid {
  width: calc(100% - 100px);
  height: calc(100vh - 120px);
  margin-left: 50px;
  margin-top: 20px;
  /* align: center; */
}
</style>
