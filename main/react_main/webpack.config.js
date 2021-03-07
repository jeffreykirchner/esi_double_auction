// frontend/webpack.config.js
const path = require('path')
const webpack = require('webpack')
module.exports = {
  // Where Webpack looks to load your JavaScript
  entry: {
    staff_home: path.resolve(__dirname, 'src/staff_home.js'),
    staff_session: path.resolve(__dirname, 'src/staff_session.js'),
  },
  mode: 'development',
  // Where Webpack spits out the results (the myapp static folder)
  output: {
    path: path.resolve(__dirname, '../static/'),
    filename: '[name].js',
  },
  plugins: [
    // Don't output new files if there is an error
    new webpack.NoEmitOnErrorsPlugin(),
  ],
  // Where find modules that can be imported (eg. React) 
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: [
        path.resolve(__dirname, 'src'),
        path.resolve(__dirname, 'node_modules'),
    ],
  },
  //babel rules
  module: { rules: [
    {
      test: /\.js$/,
      exclude: /node_modules/,
      use: ['babel-loader'],
    },
    {
      test: /\.css$/i,
      use: ["style-loader", "css-loader"],
    },
  ]},

}