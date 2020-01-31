export function transformData(data) {
  return data.map(d => {
    d["datetime"] = new Date(d["datetime"]);
    d["time_seconds"] = d["datetime"].getTime();

    return d;
  });
}
