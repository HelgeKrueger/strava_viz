const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
  context: __dirname,
  entry: "./src/index.js",
  output: {
    path: path.resolve("./strava_viz/app/static/"),
    filename: "[name]-[hash].js"
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"]
          }
        }
      },
      {
        test: /\.vue$/,
        loader: "vue-loader"
      },
      {
        test: /\.css$/,
        use: [
          "vue-style-loader",
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              modules: false
            }
          }
        ]
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        use: [
          {
            loader: "file-loader"
          }
        ]
      }
    ]
  },
  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new webpack.ProvidePlugin({
      d3: "d3"
    }),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: "styles-[hash].css"
    }),
    new CleanWebpackPlugin()
  ]
};
