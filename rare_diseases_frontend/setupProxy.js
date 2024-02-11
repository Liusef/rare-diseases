const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: "http://143.215.127.46:5000",
      changeOrigin: true,
    })
  );
};