function showLocation() {

    var output = document.getElementById("message");

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

                "📍 CURRENT LOCATION ✅" +

                "<br><br>" +

                "Latitude: " +
                lat +

                "<br>" +

                "Longitude: " +
                lon +

                "<br><br>" +

                "🎯 GPS Accuracy: ±" +
                Math.round(accuracy) +
                " meters" +

                "<br>" +

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
