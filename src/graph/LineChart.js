export default class LineChart {
  constructor(options) {
    this.width = options.width;
    this.height = options.height;
    this.selector = options.selector;

    if (!this.width || !this.height) {
      throw "Width and height must be set";
    }

    if (!this.selector) {
      throw "Must provide an svg element";
    }

    this.marginX = options.marginX || 0;
    this.marginY = options.marginY || 0;
  }

  clean() {
    this.selector.selectAll("*").remove();
    return this;
  }

  withXRange(xmin, xmax) {
    this.xmin = xmin;
    this.xmax = xmax;

    this.xScale = d3
      .scaleLinear()
      .domain([this.xmin, this.xmax])
      // .range([this.marginX, this.width - this.marginX]);
      .range([this.marginX, this.width]);

    return this;
  }

  withYRange(ymin, ymax) {
    this.ymin = ymin;
    this.ymax = ymax;

    this.yScale = d3
      .scaleLinear()
      .domain([this.ymin, this.ymax])
      .range([this.height - this.marginY, 0]);

    return this;
  }

  drawAxes() {
    this.xAxis = d3.axisBottom(this.xScale);
    this.selector
      .append("g")
      .attr("transform", `translate(0, ${this.height - this.marginY})`)
      .call(this.xAxis);

    this.yAxis = d3.axisLeft(this.yScale);
    this.selector
      .append("g")
      .attr("transform", `translate(${this.marginX}, 0)`)
      .call(this.yAxis);

    return this;
  }

  plotLine(data, properties) {
    const line = d3
      .line()
      .x((d, i) => this.xScale(properties["xValue"](d, i)))
      .y((d, i) => this.yScale(properties["yValue"](d, i)));

    if (!properties["color"]) {
      properties["color"] = "steelblue";
    }

    this.selector
      .append("g")
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", properties["color"])
      .attr("stroke-width", 2)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-opacity", properties["opacity"])
      .attr("d", line);
  }
}
