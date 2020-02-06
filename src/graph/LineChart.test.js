import LineChart from "./LineChart.js";

test("LineChart - constructor", () => {
  expect(() => {
    new LineChart({});
  }).toThrow();

  expect(() => {
    new LineChart({ width: 100, height: 100 });
  }).toThrow();

  expect(() => {
    new LineChart({ width: 100, height: 100, selector: "dummy" });
  }).not.toThrow();
});
