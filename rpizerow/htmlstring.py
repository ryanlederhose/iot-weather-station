html = """<!DOCTYPE html>
<html>

<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html {
            font-family: Helvetica;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .buttonClass {
            background-color: rgb(12, 24, 185);
            border: 3px solid #000000;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .buttonClass.on {
            background-color: green;
        }

        .buttonClass.off {
            background-color: red;
        }

        p {
            font-size: large;
        }
    </style>
    <title>Ryan's IoT Weather Project</title>

<body style="background-color: rgb(255, 255, 255);">
    <h1 style="text-align: center;">Ryan's IoT Weather Project</h1>
    <form>
        <button class="buttonClass" name="update" value="on" type="submit">Update Data</button>
    </form>
    <br>
    <br>
    <hr>
    <h2>Outside Node</h2>
    <p>As of <b>%s</b>,</p>
    <p>
        <b>Temperature</b>: %s<sup>o</sup>C<br>
        <b>Humidity</b>: %sg/m<sup>3</sup><br>
        <b>Pressure</b>: %skPa<br>
        <b>Soil Moisture</b>: %s&percnt;<br>
        <b>Lux</b>: %slm/m<sup>3</sup><br>
    </p>
    <br>
    <h2>Inside Node</h2>
    <p>As of <b>%s</b>,</p>
    <p>
        <b>Temperature</b>: <br>
        <b>Humidity</b>: <br>
        <b>Pressure</b>: <br>
        <b>Lux</b>: <br>
    </p>
    <br>
    <br>
    <hr>
    <h1>Time-series Graph</h1>
    <form>
        <br>
        <button id="insideButton" class="buttonClass off" name="inside" value="on" type="submit">Plot Inside
            Node</button>
        <button id="outsideButton" class="buttonClass off" name="outside" value="on" type="submit">Plot Outside
            Node</button>
        <br>
        <button id="luxButton" class="buttonClass off" name="lux" value="on" type="submit">Plot Lux</button>
        <button id="moistureButton" class="buttonClass off" name="moisture" value="on" type="submit">Plot Soil
            Moisture</button>
        <button id="temperatureButton" class="buttonClass off" name="temperature" value="on" type="submit">Plot
            Temperature</button>
        <button id="humidityButton" class="buttonClass off" name="humidity" value="on" type="submit">Plot
            Humidity</button>
        <button id="pressureButton" class="buttonClass off" name="pressure" value="on" type="submit">Plot
            Pressure</button>
        <br>
        <button id="button30" class="buttonClass off" name="30mins" value="on" type="submit">30 mins</button>
        <button id="button2" class="buttonClass off" name="2hours" value="on" type="submit">2 hours</button>
        <button id="button12" class="buttonClass off" name="12hours" value="on" type="submit">12 hours</button>
        <button id="button24" class="buttonClass off" name="24hours" value="on" type="submit">24 hours</button>
    </form>

    <br>
    <br>

    <canvas id="myChart"></canvas>
    <script> // Sample data
var timeLabels = %s;
var variableData = %s;
var variableString = localStorage.getItem("variableString");

// Create the chart
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [{
            label: variableString,
            data: variableData,
            borderColor: 'blue',
            fill: false
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: variableString
                }
            }
        }
    }
});

// Preserve scroll position after form submission
window.onload = function() {
    var scrollPos = sessionStorage.getItem('scrollPosition');
    if (scrollPos) {
        window.scrollTo(0, scrollPos);
        sessionStorage.removeItem('scrollPosition');
    }
};

window.onbeforeunload = function() {
    sessionStorage.setItem('scrollPosition', window.scrollY);
};

var insideButton = document.getElementById("insideButton");
var outsideButton = document.getElementById("outsideButton");
var humidityButton = document.getElementById("humidityButton");
var moistureButton = document.getElementById("moistureButton");
var pressureButton = document.getElementById("pressureButton");
var temperatureButton = document.getElementById("temperatureButton");
var luxButton = document.getElementById("luxButton");
var button30 = document.getElementById("button30");
var button2 = document.getElementById("button2");
var button12 = document.getElementById("button12");
var button24 = document.getElementById("button24");

button30.addEventListener("click", function() {
    if (button30.classList.contains('on')) {
        localStorage.setItem('button30State', 'off');
    } else {
        localStorage.setItem('button30State', 'on');
        if (button2.classList.contains('on')) {
            localStorage.setItem('button2State', 'off');
        }
        if (button12.classList.contains('on')) {
            localStorage.setItem('button12State', 'off');
        }
        if (button24.classList.contains('on')) {
            localStorage.setItem('button24State', 'off');
        }
    }
})

button2.addEventListener("click", function() {
    if (button2.classList.contains('on')) {
        localStorage.setItem('button2State', 'off');
    } else {
        localStorage.setItem('button2State', 'on');
        if (button30.classList.contains('on')) {
            localStorage.setItem('button30State', 'off');
        }
        if (button12.classList.contains('on')) {
            localStorage.setItem('button12State', 'off');
        }
        if (button24.classList.contains('on')) {
            localStorage.setItem('button24State', 'off');
        }
    }
})

button12.addEventListener("click", function() {
    if (button12.classList.contains('on')) {
        localStorage.setItem('button12State', 'off');
    } else {
        localStorage.setItem('button12State', 'on');
        if (button2.classList.contains('on')) {
            localStorage.setItem('button2State', 'off');
        }
        if (button30.classList.contains('on')) {
            localStorage.setItem('button30State', 'off');
        }
        if (button24.classList.contains('on')) {
            localStorage.setItem('button24State', 'off');
        }
    }
})

button24.addEventListener("click", function() {
    if (button24.classList.contains('on')) {
        localStorage.setItem('button24State', 'off');
    } else {
        localStorage.setItem('button24State', 'on');
        if (button2.classList.contains('on')) {
            localStorage.setItem('button2State', 'off');
        }
        if (button12.classList.contains('on')) {
            localStorage.setItem('button12State', 'off');
        }
        if (button30.classList.contains('on')) {
            localStorage.setItem('button30State', 'off');
        }
    }
})

insideButton.addEventListener("click", function() {
    if (insideButton.classList.contains('on')) {
        localStorage.setItem('insideButtonState', 'off');
    } else {
        localStorage.setItem('insideButtonState', 'on');
        if (outsideButton.classList.contains('on')) {
            localStorage.setItem('outsideButtonState', 'off');
        }
        if (moistureButton.classList.contains('on')) {
            localStorage.setItem('moistureButtonState', 'off');
            localStorage.setItem('variableString', 'null');
        }
    }
});

outsideButton.addEventListener("click", function() {
    if (outsideButton.classList.contains('on')) {
        localStorage.setItem('outsideButtonState', 'off');
    } else {
        localStorage.setItem('outsideButtonState', 'on');
        if (insideButton.classList.contains('on')) {
            localStorage.setItem('insideButtonState', 'off');
        }
    }
});

luxButton.addEventListener("click", function() {
    if (luxButton.classList.contains('on')) {
        localStorage.setItem('luxButtonState', 'off');
        localStorage.setItem('variableString', 'null')
    } else {
        localStorage.setItem('luxButtonState', 'on')
        localStorage.setItem('variableString', 'Lux')
        if (moistureButton.classList.contains('on')) {
            localStorage.setItem('moistureButtonState', 'off');
        }
        if (pressureButton.classList.contains('on')) {
            localStorage.setItem('pressureButtonState', 'off');
        }
        if (humidityButton.classList.contains('on')) {
            localStorage.setItem('humidityButtonState', 'off');
        }
        if (temperatureButton.classList.contains('on')) {
            localStorage.setItem('temperatureButtonState', 'off');
        }
    }
});

moistureButton.addEventListener("click", function() {
    if (moistureButton.classList.contains('on')) {
        localStorage.setItem('moistureButtonState', 'off');
        localStorage.setItem('variableString', 'null')
    } else {
        if (insideButton.classList.contains('on')) {
            localStorage.setItem('moistureButtonState', 'off');
        } else {
            localStorage.setItem('moistureButtonState', 'on')
            localStorage.setItem('variableString', 'Soil Moisture')
            if (luxButton.classList.contains('on')) {
                localStorage.setItem('luxButtonState', 'off');
            }
            if (pressureButton.classList.contains('on')) {
                localStorage.setItem('pressureButtonState', 'off');
            }
            if (humidityButton.classList.contains('on')) {
                localStorage.setItem('humidityButtonState', 'off');
            }
            if (temperatureButton.classList.contains('on')) {
                localStorage.setItem('temperatureButtonState', 'off');
            }
        }
    }
});

temperatureButton.addEventListener("click", function() {
    if (temperatureButton.classList.contains('on')) {
        localStorage.setItem('temperatureButtonState', 'off');
        localStorage.setItem('variableString', 'null')
    } else {
        localStorage.setItem('temperatureButtonState', 'on')
        localStorage.setItem('variableString', 'Temperature')
        if (moistureButton.classList.contains('on')) {
            localStorage.setItem('moistureButtonState', 'off');
        }
        if (pressureButton.classList.contains('on')) {
            localStorage.setItem('pressureButtonState', 'off');
        }
        if (humidityButton.classList.contains('on')) {
            localStorage.setItem('humidityButtonState', 'off');
        }
        if (luxButton.classList.contains('on')) {
            localStorage.setItem('luxButtonState', 'off');
        }
    }
});

pressureButton.addEventListener("click", function() {
    if (pressureButton.classList.contains('on')) {
        localStorage.setItem('pressureButtonState', 'off');
        localStorage.setItem('variableString', 'null')
    } else {
        localStorage.setItem('pressureButtonState', 'on')
        localStorage.setItem('variableString', 'Pressure')
        if (moistureButton.classList.contains('on')) {
            localStorage.setItem('moistureButtonState', 'off');
        }
        if (luxButton.classList.contains('on')) {
            localStorage.setItem('luxButtonState', 'off');
        }
        if (humidityButton.classList.contains('on')) {
            localStorage.setItem('humidityButtonState', 'off');
        }
        if (temperatureButton.classList.contains('on')) {
            localStorage.setItem('temperatureButtonState', 'off');
        }
    }
});

humidityButton.addEventListener("click", function() {
    if (humidityButton.classList.contains('on')) {
        localStorage.setItem('humidityButtonState', 'off');
        localStorage.setItem('variableString', 'null')
    } else {
        localStorage.setItem('humidityButtonState', 'on')
        localStorage.setItem('variableString', 'Humidity')
        if (moistureButton.classList.contains('on')) {
            localStorage.setItem('moistureButtonState', 'off');
        }
        if (pressureButton.classList.contains('on')) {
            localStorage.setItem('pressureButtonState', 'off');
        }
        if (luxButton.classList.contains('on')) {
            localStorage.setItem('luxButtonState', 'off');
        }
        if (temperatureButton.classList.contains('on')) {
            localStorage.setItem('temperatureButtonState', 'off');
        }
    }
});

// Restore the style changes on page load
document.addEventListener('DOMContentLoaded', function() {
    var insideButtonState = localStorage.getItem('insideButtonState');
    var outsideButtonState = localStorage.getItem('outsideButtonState');
    var luxButtonState = localStorage.getItem('luxButtonState');                
    var pressureButtonState = localStorage.getItem('pressureButtonState');
    var humidityButtonState = localStorage.getItem('humidityButtonState');
    var moistureButtonState = localStorage.getItem('moistureButtonState');
    var temperatureButtonState = localStorage.getItem('temperatureButtonState');
    var button30State = localStorage.getItem('button30State');
    var button2State = localStorage.getItem('button2State');
    var button12State = localStorage.getItem('button12State');
    var button24State = localStorage.getItem('button24State');

    if (outsideButtonState == 'on') {
        outsideButton.classList.remove('off')
        outsideButton.classList.add('on')
    } else if (outsideButtonState == 'off') {
        outsideButton.classList.add('off')
        outsideButton.classList.remove('on')
    }
    if (insideButtonState == 'on') {
        insideButton.classList.remove('off')
        insideButton.classList.add('on')
    } else if (insideButtonState == 'off') {
        insideButton.classList.add('off')
        insideButton.classList.remove('on')
    }
    if (luxButtonState == 'on') {
        luxButton.classList.remove('off')
        luxButton.classList.add('on')
    } else if (luxButtonState == 'off') {
        luxButton.classList.add('off')
        luxButton.classList.remove('on')
    }
    if (pressureButtonState == 'on') {
        pressureButton.classList.remove('off')
        pressureButton.classList.add('on');
    } else if (pressureButtonState == 'off') {
        pressureButton.classList.add('off')
        pressureButton.classList.remove('on')
    }
    if (moistureButtonState == 'on') {
        moistureButton.classList.remove('off')
        moistureButton.classList.add('on')
    } else if (moistureButtonState == 'off') {
        moistureButton.classList.add('off')
        moistureButton.classList.remove('on')
    }
    if (temperatureButtonState == 'on') {
        temperatureButton.classList.remove('off')
        temperatureButton.classList.add('on')
    } else if (temperatureButtonState == 'off') {
        temperatureButton.classList.add('off')
        temperatureButton.classList.remove('on')
    }
    if (humidityButtonState == 'on') {
        humidityButton.classList.remove('off')
        humidityButton.classList.add('on')
    } else if (humidityButtonState == 'off') {
        humidityButton.classList.add('off')
        humidityButton.classList.remove('on')
    }               
    if (button2State == 'on') {
        button2.classList.remove('off')
        button2.classList.add('on')
    } else if (button2State == 'off') {
        button2.classList.remove('on')
        button2.classList.add('off')
    }              
    if (button12State == 'on') {
        button12.classList.remove('off')
        button12.classList.add('on')
    } else if (button12State == 'off') {
        button12.classList.remove('on')
        button12.classList.add('off')
    }              
    if (button24State == 'on') {
        button24.classList.remove('off')
        button24.classList.add('on')
    } else if (button24State == 'off') {
        button24.classList.remove('on')
        button24.classList.add('off')
    }              
    if (button30State == 'on') {
        button30.classList.remove('off')
        button30.classList.add('on')
    } else if (button30State == 'off') {
        button30.classList.remove('on')
        button30.classList.add('off')
    }
});</script>
    <br>
    <br>
    <hr>
</body>
</head>

</html>
"""

def get_html_string():
    return html
