const HtmlWebPackPlugin = require('html-webpack-plugin');

module.exports = {
  resolve: {
    extensions: ['*', '.js', '.jsx', '.css', '.svg'],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: { loader: 'babel-loader' },
      },
      {
        test: /\.css$/,
        use: [
          { loader: 'style-loader' },
          { loader: 'css-loader' },
        ],
      },
      {
        test: /\.svg$/,
        use: ['@svgr/webpack', 'file-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebPackPlugin({
      template: './src/index.html',
      filename: 'index.html',
      favicon: './public/favicon.ico',
    }),
  ],
  devServer: {
    hot: true,
    port: 3000,
  },
};
