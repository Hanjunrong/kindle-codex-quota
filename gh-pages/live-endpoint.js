window.DASH_LIVE_ENDPOINTS = (function () {
  var list = [];
  // Keep the existing range first so the current Mac address (192.168.0.105)
  // remains fast, then include the low-address range as additional candidates.
  for (var i = 100; i <= 110; i += 1) {
    list.push('http://192.168.0.' + i + ':8000/data.js');
  }
  for (var j = 1; j <= 20; j += 1) {
    list.push('http://192.168.0.' + j + ':8000/data.js');
  }
  return list;
})();
window.DASH_LIVE_ENDPOINT = window.DASH_LIVE_ENDPOINTS[0];