async function loadWeather() {
    // this function tries to load weather parameters and update them on the website
    try {
        const response = await fetch("/api/weather");
        const data = await response.json();

        document.getElementById("temp").textContent = data.temperature;
        document.getElementById("humi").textContent = data.humidity;
    } catch (error) {
        console.error("Error while loading data", error);
    }
}

// starts on the webpage load
loadWeather();

// delay of 5 seconds - the same as with the update calls of the server
setInterval(loadWeather, 5000);