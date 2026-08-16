window.DASH_LIVE_ENDPOINTS = (function () {
  var list = [];
  for (var i = 100; i <= 110; i += 1) {
    list.push('http://192.168.0.' + i + ':8000/data.js');
  }
  return list;
})();
window.DASH_LIVE_ENDPOINT = window.DASH_LIVE_ENDPOINTS[0];