import "ol/ol.css";

import { Map } from "ol";
import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
import { fromLonLat } from "ol/proj";
import { OSM, Vector as VectorSource } from "ol/source";
import { Style, Fill, Stroke } from "ol/style";

import View from "ol/View";
import LineString from "ol/geom/LineString";
import Feature from "ol/Feature";
import Polyline from "ol/format/Polyline";

export class OpenLayerMap {
  constructor() {
    this.styleRun = new Style({
      stroke: new Stroke({
        color: "red"
      })
    });
    this.styleRide = new Style({
      stroke: new Stroke({
        color: "blue"
      })
    });
    this.polylineParser = new Polyline();
  }

  addToDiv(divId) {
    this.map = new Map({
      target: divId,
      layers: [
        new TileLayer({
          source: new OSM()
        })
      ]
    });
    this.view = new View({
      center: fromLonLat([11.7271, 48.10963]),
      zoom: 10
    });
    this.map.setView(this.view);
  }

  createPolyline(data) {
    let line = this.polylineParser.readFeature(data.polyline);
    line.setGeometry(line.getGeometry().transform("EPSG:4326", "EPSG:3857"));

    if (data.activity_type == "run") {
      line.setStyle(this.styleRun);
    }

    if (data.activity_type == "ride") {
      line.setStyle(this.styleRide);
    }

    return line;
  }

  addPolylines(data) {
    const func = this.createPolyline;
    const features = data.map(this.createPolyline, this);

    let source = new VectorSource({
      features: features
    });

    this.view.fit(source.getExtent(), { padding: [25, 25, 50, 25] });

    var layerLines = new VectorLayer({
      source: source
    });

    this.map.addLayer(layerLines);
    this.map.render();
  }
}
