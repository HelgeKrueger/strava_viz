export function transformData(data, options = {}) {
  let transformed = data.map(d => {
    d["datetime"] = new Date(d["datetime"]);
    d["time_seconds"] = d["datetime"].getTime();
    return d;
  });

  if (options.filter) {
    transformed = transformed.filter(
      d => d["activity_type"] === options.filter
    );
  }

  return transformed;
}
