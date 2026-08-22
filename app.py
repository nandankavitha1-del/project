from flask import Flask, request, jsonify
import json
import os
import socket

app = Flask(__name__)

CONTACT_FILE = "emergency_contact.json"
LOCATION_FILE = "location.json"


# =========================
# STORAGE
# =========================

def save_contact(name, number):
    data = {
        "name": name,
        "number": number
    }

    with open(CONTACT_FILE, "w") as file:
        json.dump(data, file)


def get_contact():
    if not os.path.exists(CONTACT_FILE):
        return {
            "name": "",
            "number": ""
        }

    try:
        with open(CONTACT_FILE, "r") as file:
            return json.load(file)
    except:
        return {
            "name": "",
            "number": ""
        }


def save_location(lat, lon):
    data = {
        "lat": lat,
        "lon": lon
    }

    with open(LOCATION_FILE, "w") as file:
        json.dump(data, file)


def get_location():
    if not os.path.exists(LOCATION_FILE):
        return None

    try:
        with open(LOCATION_FILE, "r") as file:
            return json.load(file)
    except:
        return None


# =========================
# HTML
# =========================

HTML = """
<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>RakshanBala</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 15px;
    font-family: Arial, sans-serif;
    background: linear-gradient(
        180deg,
        #0f172a,
        #1e293b
    );
    color: white;
}

.container {
    max-width: 480px;
    margin: auto;
}

.header {
    text-align: center;
    padding: 20px 10px;
}

.logo {
    font-size: 50px;
}

.header h1 {
    margin: 5px;
}

.header p {
    color: #cbd5e1;
}

.card {
    background: rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 15px;
}

input {
    width: 100%;
    padding: 14px;
    margin: 7px 0;
    border: none;
    border-radius: 12px;
    font-size: 16px;
}

button {
    width: 100%;
    padding: 15px;
    margin: 7px 0;
    border: none;
    border-radius: 13px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

.sos {
    background: #dc2626;
    color: white;
}

.emergency {
    background: #f97316;
    color: white;
}

.location {
    background: #2563eb;
    color: white;
}

.live {
    background: #059669;
    color: white;
}

.stop {
    background: #475569;
    color: white;
}

.police {
    background: #7c3aed;
    color: white;
}

.share {
    background: #0891b2;
    color: white;
}

.status {
    background: rgba(0,0,0,0.25);
    padding: 15px;
    border-radius: 12px;
    margin-top: 10px;
    line-height: 1.7;
}

.sharebox {
    background: white;
    color: #111827;
    padding: 12px;
    border-radius: 10px;
    word-break: break-all;
    margin-top: 10px;
}

textarea {
    width: 100%;
    min-height: 150px;
    padding: 12px;
    border-radius: 10px;
    border: none;
}

a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 14px;
    margin-top: 10px;
    border-radius: 12px;
    background: rgba(255,255,255,0.12);
}

</style>

</head>

<body>

<div class="container">

<div class="header">

<div class="logo">🚨</div>

<h1>RakshanBala</h1>

<p>Your Personal Safety Companion</p>

</div>


<!-- EMERGENCY CONTACT -->

<div class="card">

<h2>👤 Emergency Contact</h2>

<form method="POST" action="/save">

<input
name="name"
placeholder="Contact Name"
value="CONTACT_NAME"
required
>

<input
name="number"
type="tel"
placeholder="Mobile Number"
value="CONTACT_NUMBER"
required
>

<button type="submit">
💾 SAVE EMERGENCY CONTACT
</button>

</form>

</div>


<!-- EMERGENCY -->

<div class="card">

<h2>🚨 Emergency</h2>

<button class="sos"
onclick="sendSOS()">
🚨 SEND SOS
</button>

<button class="emergency"
onclick="activateEmergency()">
🚨 ACTIVATE EMERGENCY
</button>

<div id="emergencyStatus"
class="status">
🟢 Emergency system ready
</div>

</div>


<!-- LOCATION -->

<div class="card">

<h2>📍 My Location</h2>

<button class="location"
onclick="showLocation()">
📍 SHOW MY LOCATION
</button>

<button class="live"
onclick="startLiveLocation()">
📍 START LIVE LOCATION
</button>

<button class="stop"
onclick="stopLiveLocation()">
⛔ STOP LIVE LOCATION
</button>

<div id="message"
class="status">
Ready for location
</div>

</div>


<!-- FAMILY -->

<div class="card">

<h2>👨‍👩‍👧 Family & Friends</h2>

<button class="share"
onclick="createShareLink()">
🔗 SHARE LIVE LOCATION
</button>

<div id="shareBox"></div>

</div>


<!-- POLICE -->

<div class="card">

<h2>👮 Police Support</h2>

<button class="police"
onclick="findPolice()">
👮 FIND NEAREST POLICE STATION
</button>

</div>


</div>


<script>

var watcher = null;

var sosMessage = "";

var emergencyNumber = "CONTACT_NUMBER";


/* =========================
   GPS
========================= */

function getGPS(callback) {

    if (!navigator.geolocation) {

        alert("GPS is not supported.");

        return;
    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            var lat =
                position.coords.latitude;

            var lon =
                position.coords.longitude;

            callback(lat, lon);
        },

        function() {

            alert(
                "Please allow location permission."
            );
        },

        {
            enableHighAccuracy: true,
            timeout: 30000,
            maximumAge: 0
        }
    );
}


/* =========================
   SHOW MY LOCATION
========================= */

function showLocation() {

    var output =
        document.getElementById("message");

    output.innerHTML =
        "📍 GETTING CURRENT LOCATION...<br>" +
        "⏳ Please wait 5-10 seconds.";

    if (!navigator.geolocation) {

        output.innerHTML =
            "❌ GPS is not supported on this phone.";

        return;
    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            var lat =
                position.coords.latitude;

            var lon =
                position.coords.longitude;

            var accuracy =
                position.coords.accuracy;

            var maps =
                "https://www.google.com/maps?q=" +
                lat + "," + lon;

            var accuracyMessage = "";

            if (accuracy <= 10) {

                accuracyMessage =
                    "🟢 VERY ACCURATE";

            } else if (accuracy <= 30) {

                accuracyMessage =
                    "🟢 GOOD ACCURACY";

            } else if (accuracy <= 100) {

                accuracyMessage =
                    "🟡 MODERATE ACCURACY";

            } else {

                accuracyMessage =
                    "🔴 LOW ACCURACY - Try outside";
            }

            output.innerHTML =
                "📍 CURRENT LOCATION ✅<br><br>" +
                "Latitude: " + lat + "<br>" +
                "Longitude: " + lon + "<br><br>" +
                "🎯 GPS Accuracy: ±" +
                Math.round(accuracy) +
                " meters<br>" +
                accuracyMessage +
                "<br><br>" +
                "<a target='_blank' href='" +
                maps +
                "'>" +
                "🗺️ OPEN GOOGLE MAPS" +
                "</a>";
        },

        function(error) {

            if (error.code === 1) {

                output.innerHTML =
                    "❌ LOCATION PERMISSION DENIED<br><br>" +
                    "Please allow precise location permission.";

            } else if (error.code === 2) {

                output.innerHTML =
                    "❌ LOCATION UNAVAILABLE<br><br>" +
                    "Please turn ON GPS/Location.";

            } else if (error.code === 3) {

                output.innerHTML =
                    "⏳ LOCATION REQUEST TIMEOUT<br><br>" +
                    "Please try again in an open area.";

            } else {

                output.innerHTML =
                    "❌ Unable to get current location.";
            }
        },

        {
            enableHighAccuracy: true,
            timeout: 30000,
            maximumAge: 0
        }
    );
}


/* =========================
   SOS
========================= */

function sendSOS() {

    var output =
        document.getElementById("message");

    output.innerHTML =
        "🚨 SOS ACTIVATED<br>" +
        "📍 Getting GPS location...";

    getGPS(function(lat, lon) {

        var maps =
            "https://www.google.com/maps?q=" +
            lat + "," + lon;

        sosMessage =
            "🚨 SOS ALERT from RakshanBala.\\n\\n" +
            "I need emergency assistance.\\n\\n" +
            "📍 My current location:\\n" +
            maps;

        output.innerHTML =
            "🚨 SOS READY ✅" +
            "<br><br>" +
            "Latitude: " + lat +
            "<br>" +
            "Longitude: " + lon +
            "<br><br>" +
            "<textarea readonly>" +
            sosMessage +
            "</textarea>" +
            "<button class='sos' " +
            "onclick='openSMS()'>" +
            "📱 OPEN SMS & SEND" +
            "</button>";
    });
}


/* =========================
   EMERGENCY
========================= */

function activateEmergency() {

    var status =
        document.getElementById(
            "emergencyStatus"
        );

    status.innerHTML =
        "🔴 EMERGENCY MODE ACTIVE<br>" +
        "📍 Getting location...";

    getGPS(function(lat, lon) {

        var maps =
            "https://www.google.com/maps?q=" +
            lat + "," + lon;

        sosMessage =
            "🚨 EMERGENCY ALERT - RakshanBala\\n\\n" +
            "Emergency assistance is required.\\n\\n" +
            "📍 Current location:\\n" +
            maps;

        status.innerHTML =
            "🔴 EMERGENCY MODE ACTIVE" +
            "<br><br>" +
            "📍 GPS location received" +
            "<br><br>" +
            "<button class='sos' " +
            "onclick='openSMS()'>" +
            "📱 OPEN SMS & SEND" +
            "</button>";
    });
}


/* =========================
   SMS
========================= */

function openSMS() {

    if (!sosMessage) {

        alert(
            "Please activate SOS first."
        );

        return;
    }

    var url =
        "sms:" +
        emergencyNumber +
        "?body=" +
        encodeURIComponent(sosMessage);

    window.location.href = url;
}


/* =========================
   START LIVE LOCATION
========================= */

function startLiveLocation() {

    var output =
        document.getElementById("message");

    output.innerHTML =
        "📍 Starting live location...";

    if (watcher !== null) {

        navigator.geolocation.clearWatch(
            watcher
        );
    }

    watcher =
        navigator.geolocation.watchPosition(

        function(position) {

            var lat =
                position.coords.latitude;

            var lon =
                position.coords.longitude;

            fetch(
                "/update_location",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        lat: lat,
                        lon: lon
                    })
                }
            )
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                console.log(
                    "Location saved:",
                    data
                );
            })
            .catch(function(error) {
                console.log(
                    "Location error:",
                    error
                );
            });

            var maps =
                "https://www.google.com/maps?q=" +
                lat + "," + lon;

            output.innerHTML =
                "📍 LIVE LOCATION ACTIVE ✅" +
                "<br><br>" +
                "Latitude: " + lat +
                "<br>" +
                "Longitude: " + lon +
                "<br><br>" +
                "<a target='_blank' href='" +
                maps +
                "'>" +
                "🗺️ VIEW CURRENT LOCATION" +
                "</a>";
        },

        function(error) {

            console.log(error);

            output.innerHTML =
                "❌ Please allow GPS permission.";
        },

        {
            enableHighAccuracy: true,
            maximumAge: 5000,
            timeout: 15000
        }
    );
}


/* =========================
   STOP LIVE LOCATION
========================= */

function stopLiveLocation() {

    if (watcher !== null) {

        navigator.geolocation.clearWatch(
            watcher
        );

        watcher = null;
    }

    document.getElementById(
        "message"
    ).innerHTML =
        "⛔ LIVE LOCATION STOPPED";
}


/* =========================
   FAMILY SHARE LINK
========================= */

function createShareLink() {

    var link =
        window.location.origin +
        "/family";

    var box =
        document.getElementById(
            "shareBox"
        );

    box.innerHTML =
        "<div class='sharebox'>" +
        "<b>Family Live Location Link:</b>" +
        "<br><br>" +
        link +
        "</div>" +

        "<button class='share' " +
        "onclick='copyShareLink()'>" +
        "📋 COPY SHARE LINK" +
        "</button>" +

        "<button class='share' " +
        "onclick='sendShareLink()'>" +
        "📤 SHARE WITH FAMILY" +
        "</button>";
}


/* =========================
   COPY LINK
========================= */

function copyShareLink() {

    var link =
        window.location.origin +
        "/family";

    if (navigator.clipboard) {

        navigator.clipboard.writeText(
            link
        )
        .then(function() {

            alert(
                "✅ Family Share Link copied!"
            );

        })
        .catch(function() {

            prompt(
                "Copy this link:",
                link
            );
        });

    } else {

        prompt(
            "Copy this link:",
            link
        );
    }
}


/* =========================
   SHARE LINK
========================= */

function sendShareLink() {

    var link =
        window.location.origin +
        "/family";

    if (navigator.share) {

        navigator.share({

            title:
            "RakshanBala Live Location",

            text:
            "View my live location",

            url: link

        }).catch(function(error) {

            console.log(
                "Share cancelled:",
                error
            );
        });

    } else {

        copyShareLink();
    }
}


/* =========================
   POLICE
========================= */

function findPolice() {

    var output =
        document.getElementById("message");

    output.innerHTML =
        "👮 Finding police stations...";

    getGPS(function(lat, lon) {

        var url =
            "https://www.google.com/maps/search/police+station/@" +
            lat + "," +
            lon + ",14z";

        output.innerHTML =
            "👮 POLICE STATIONS FOUND ✅" +
            "<br><br>" +
            "<a target='_blank' href='" +
            url +
            "'>" +
            "🗺️ OPEN NEAREST POLICE STATIONS" +
            "</a>";
    });
}

</script>

</body>

</html>
"""


# =========================
# HOME
# =========================

@app.route("/")
def home():

    contact = get_contact()

    page = HTML

    page = page.replace(
        "CONTACT_NAME",
        contact.get("name", "")
    )

    page = page.replace(
        "CONTACT_NUMBER",
        contact.get("number", "")
    )

    return page


# =========================
# SAVE CONTACT
# =========================

@app.route(
    "/save",
    methods=["POST"]
)
def save():

    name = request.form.get(
        "name",
        ""
    ).strip()

    number = request.form.get(
        "number",
        ""
    ).strip()

    save_contact(
        name,
        number
    )

    return """
<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

</head>

<body style="
font-family:Arial;
text-align:center;
padding:40px;
background:#0f172a;
color:white;
">

<h1>🚨 RakshanBala</h1>

<h2>
✅ CONTACT SAVED PERMANENTLY
</h2>

<p>
👤 Emergency contact saved
</p>

<br>

<a href="/" style="
display:inline-block;
padding:15px;
background:#2563eb;
color:white;
text-decoration:none;
border-radius:10px;
">

⬅️ BACK TO RAKSHANBALA

</a>

</body>

</html>
"""


# =========================
# UPDATE LOCATION
# =========================

@app.route(
    "/update_location",
    methods=["POST"]
)
def update_location():

    data = request.get_json(
        silent=True
    )

    if data is None:

        return jsonify({
            "success": False,
            "message": "No location data"
        })

    lat = data.get("lat")
    lon = data.get("lon")

    if lat is None:
        lat = data.get("latitude")

    if lon is None:
        lon = data.get("longitude")

    if lat is None or lon is None:

        return jsonify({
            "success": False,
            "message":
            "Latitude or longitude missing"
        })

    save_location(
        lat,
        lon
    )

    return jsonify({
        "success": True,
        "message": "Location updated",
        "lat": lat,
        "lon": lon
    })


# =========================
# GET LOCATION API
# =========================

@app.route("/location")
def location():

    data = get_location()

    if data is None:

        return jsonify({
            "success": False,
            "message":
            "Location not available"
        })

    return jsonify({

        "success": True,

        "lat":
        data.get("lat"),

        "lon":
        data.get("lon")

    })


# =========================
# FAMILY LIVE VIEWER
# =========================

@app.route("/family")
def family():

    data = get_location()

    if data is None:

        return """
<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<meta http-equiv="refresh"
content="5">

<title>
RakshanBala Family
</title>

</head>

<body style="
font-family:Arial;
text-align:center;
padding:30px;
background:#0f172a;
color:white;
">

<h1>🚨 RakshanBala</h1>

<h2>
👨‍👩‍👧 Family & Friends
</h2>

<p>
📍 Waiting for live location...
</p>

<p>
Please start Live Location on the main phone.
</p>

<p>
🔄 Checking again in 5 seconds...
</p>

</body>

</html>
"""

    lat = data.get("lat")
    lon = data.get("lon")

    maps = (
        "https://www.google.com/maps?q="
        + str(lat)
        + ","
        + str(lon)
    )

    return """
<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<meta http-equiv="refresh"
content="5">

<title>
RakshanBala Live Location
</title>

<style>

body {

    font-family: Arial;

    background: #0f172a;

    color: white;

    text-align: center;

    padding: 20px;

}

.box {

    max-width: 450px;

    margin: auto;

    background: #1e293b;

    padding: 25px;

    border-radius: 22px;

}

.active {

    color: #4ade80;

    font-size: 18px;

    font-weight: bold;

}

.location {

    background: #2563eb;

    color: white;

    padding: 15px;

    display: block;

    border-radius: 12px;

    text-decoration: none;

    margin-top: 20px;

}

</style>

</head>

<body>

<div class="box">

<h1>
🚨 RakshanBala
</h1>

<h2>
👨‍👩‍👧 Family & Friends
</h2>

<p class="active">
📍 LIVE LOCATION ACTIVE ✅
</p>

<p>
Latitude
<br>
<b>
""" + str(lat) + """
</b>
</p>

<p>
Longitude
<br>
<b>
""" + str(lon) + """
</b>
</p>

<a
class="location"
target="_blank"
href=\"""" + maps + """\">

🗺️ VIEW LOCATION ON GOOGLE MAPS

</a>

<p>
🔄 Location refreshes every 5 seconds
</p>

</div>

</body>

</html>
"""


# =========================
# SERVER
# =========================

if __name__ == "__main__":

    try:

        hostname = socket.gethostname()

        local_ip = socket.gethostbyname(
            hostname
        )

    except:

        local_ip = "127.0.0.1"

    print("")
    print("==============================")
    print("🚨 RakshanBala Flask Working")
    print("==============================")
    print("")

    print(
        "Local: http://127.0.0.1:5001"
    )

    print(
        "Network: http://" +
        local_ip +
        ":5001"
    )

    print("")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
