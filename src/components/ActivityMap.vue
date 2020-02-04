<template>
  <div id="mapid"></div>
</template>

<script>
import { OpenLayerMap } from "../olmap.js";

export default {
  name: "ActivityMap",
  data: function() {
    return {
      openLayerMap: new OpenLayerMap()
    };
  },
  mounted: function() {
    this.openLayerMap.addToDiv("mapid");
    fetch("/api/polylines")
      .then(d => d.json())
      .then(d => {
        this.openLayerMap.addPolylines(d.thisYear);
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
}
</style>
