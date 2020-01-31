export function transformData(data) {
  return data.map(d => {
    d["datetime"] = new Date(d["datetime"]);
    d["time_seconds"] = d["datetime"].getTime();
    d["distance_km"] = d["distance_meter"] / 1000;
    return d;
  });
}
