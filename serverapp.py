from flask import Flask, render_template_string
import os

app = Flask(__name__)
LOG_FILE = '/tmp/shadow_trace.log'

HTML = """
<!DOCTYPE html>
<html>
<head><title>Shadow Trace</title></head>
<body>
<h1>Tracked Devices</h1>
<div id="map"></div>
<script>
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), { zoom: 3, center: {lat: 0, lng: 0} });
    var devices = {{ devices|tojson }};
    devices.forEach(d => {
        var parts = d.split('|');
        var loc = parts[2].split(':')[1]; // GPS or IPGeo
        var latlng = loc.split(',');
        new google.maps.Marker({ position: {lat: parseFloat(latlng[0]), lng: parseFloat(latlng[1])}, map: map, title: parts[0] });
    });
}
</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=initMap"></script>
</body>
</html>
"""

@app.route('/')
def index():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            lines = f.readlines()
    else:
        lines = []
    return render_template_string(HTML, devices=lines)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)