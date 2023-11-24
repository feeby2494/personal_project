/*

Main OpenLayers js file: base for other page-specific
ol js files.

Hierachy:
  1. ol-main.js (do not depend on ws-main.js)
  2. ws-main.js (do not depend on ol-main.js)
  3. ws-ol-interaction.js (layer that mixes ol and ws apis together)
  4. page-sepecific js files that use the first three js files and build on top

*/

// Declaring view for our map; will need an instance of this View class and call methods later on to change center
const current_view = new ol.View({
  center: ol.proj.fromLonLat([2.333333, 48.866667]), // Defaulting to Paris
  // rotation: Math.PI / 6,
  zoom: 12
})

// Get user's current location

const geolocation = new ol.Geolocation({
  // take the projection to use from the map's view
  // enableHighAccuracy must be set to true to have the heading value.
  trackingOptions: {
    enableHighAccuracy: true,
  },
  projection: current_view.getProjection()
});




function el(id) {
  return document.getElementById(id);
}

// set tracking to true
el('track').addEventListener('change', function () {
  geolocation.setTracking(this.checked);
});



// listen to changes in position
geolocation.on('change', function(evt) {
  console.log("User's Position: ", geolocation.getPosition());
});
// listen to error
geolocation.on('error', function(evt) {
  const info = document.getElementById('info');
  info.innerHTML = error.message;
  info.style.display = '';
  window.console.log(evt.message);
});

const accuracyFeature = new ol.Feature();
geolocation.on('change:accuracyGeometry', function () {
  accuracyFeature.setGeometry(geolocation.getAccuracyGeometry());
});



// Pointer for user's location
const positionFeature = new ol.Feature();
positionFeature.setStyle(
  new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({
        color: '#3399CC',
      }),
      stroke: new ol.style.Stroke({
        color: '#fff',
        width: 2,
      }),
    }),
  })
);



geolocation.on('change:position', function () {
  // setInterval(function () {
  //   const coordinates = geolocation.getPosition();
  //   console.log(`postion update: ${coordinates}`);
  //   positionFeature.setGeometry(coordinates ? new Point(coordinates) : null);
  // }, 5000); //Reading from device every 5 seconds

  setTimeout(function () {
    const coordinates = geolocation.getPosition();
    console.log(`postion update: ${coordinates}`);
    positionFeature.setGeometry(coordinates ? new ol.geom.Point(coordinates) : null);
    document.getElementById('current-postion').removeAttribute('disabled');
  }, 5000); //Reading from device and stop after 5 seconds
});


// Main map creation
var map = new ol.Map({
target: 'map',
layers: [
  new ol.layer.Tile({
    source: new ol.source.OSM()
  }),

],
features: [accuracyFeature, positionFeature],
view: current_view
});


// Add current location to map
new ol.layer.Vector({
  map: map,
  source: new ol.source.Vector({
    features: [accuracyFeature, positionFeature],
  }),
});


// move to current location
el('current-postion').addEventListener('click', function () {
  if (positionFeature.values_) {
    console.log(positionFeature.values_.geometry.flatCoordinates)
    current_view.setCenter(positionFeature.values_.geometry.flatCoordinates);
  } else {
    console.log("Please wait, positionFeature not ready...")
  }
});