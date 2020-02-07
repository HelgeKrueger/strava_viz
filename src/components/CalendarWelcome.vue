<template>
  <div>
    <svg />
  </div>
</template>

<script>
function determineColor(d) {
  if (d["ride_distance"] > 0) {
    return "blue";
  }
  if (d["run_distance"] > 0) {
    return "red";
  }

  return "lightgray";
}

export default {
  name: "CalendarWelcome",
  props: ["data", "activityIds"],
  watch: {
    data: function() {
      const svg = d3.select(this.$el).select("svg");
      const cellSize = 15;
      const cellSpacing = 20;
      const lastMonth = this.data.last_month;
      const currentMonth = this.data.current_month;
      const dayNames = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
      const monthNames = ["Januar", "Februar"];
      svg
        .append("g")
        .attr("transform", "translate(0, 20)")
        .attr("text-anchor", "end")
        .selectAll("text")
        .data(d3.range(7))
        .join("text")
        .attr("x", 30)
        .attr("y", d => (d + 0.7) * cellSpacing)
        .text(d => dayNames[d]);

      svg
        .append("g")
        .attr("transform", "translate(120, 0)")
        .attr("text-anchor", "end")
        .selectAll("text")
        .data(d3.range(2))
        .join("text")
        .attr("x", d => 120 * d)
        .attr("y", 15)
        .text(d => monthNames[d]);

      svg
        .append("g")
        .attr("transform", "translate(40, 20)")
        .selectAll("rect")
        .data(lastMonth)
        .join("rect")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("x", d => d["week"] * cellSpacing)
        .attr("y", d => d["weekday"] * cellSpacing)
        .attr("fill", determineColor)
        .on("click", d => {
          this.$emit("updateIds", d["ids"]);
        });

      svg
        .append("g")
        .attr("transform", "translate(160, 20)")
        .selectAll("rect")
        .data(currentMonth)
        .join("rect")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("x", d => d["week"] * cellSpacing)
        .attr("y", d => d["weekday"] * cellSpacing)
        .attr("fill", determineColor)
        .on("click", d => {
          this.$emit("updateIds", d["ids"]);
        });
    }
  }
};
</script>

<style scoped>
svg,
div {
  width: 100%;
  height: 100%;
}
</style>