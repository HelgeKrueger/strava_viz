const d3 = require("d3");

const canvas = d3.select("#canvas");

function determineColor(d) {
  if (d["activity_type"] == "ride") {
    return "blue";
  }

  if (d["activity_type"] == "run") {
    return "red";
  }

  return "black";
}

function transformData(data) {
  return data.map(d => {
    d["datetime"] = new Date(d["datetime"]);
    d["time_seconds"] = d["datetime"].getTime();

    return d;
  });
}

d3.json("/strava-activity").then(data => {
  let circles = canvas.selectAll("circle").data(data);

  data = transformData(data);

  const time_sorted = data.map(d => d["time_seconds"]).sort();
  const time_minimum = time_sorted[0];
  const time_maximum = time_sorted[time_sorted.length - 1];
  const time_length = time_maximum - time_minimum;

  circles
    .enter()
    .append("circle")
    .attr("cx", d => ((d["time_seconds"] - time_minimum) / time_length) * 1000)
    .attr("cy", 100)
    .attr("r", d => d["distance_meter"] / 1000)
    .attr("fill", determineColor)
    .attr("fill-opacity", 0.2);
});
