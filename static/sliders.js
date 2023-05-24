// Function to initialize sliders
// function for the sliders in search_page.html
function initializeSliders() {
    const slider1 = document.getElementById("max_tokens");
    const sliderValue1 = document.getElementById("max_tokens_value");
    const slider2 = document.getElementById("num_results");
    const sliderValue2 = document.getElementById("num_results_value");
    const slider3 = document.getElementById("temperature");
    const sliderValue3 = document.getElementById("temperature_value");
    const slider4 = document.getElementById("frequency_penalty");
    const sliderValue4 = document.getElementById("frequency_penalty_value");

    // Display the default slider values
    sliderValue1.innerHTML = slider1.value;
    sliderValue2.innerHTML = slider2.value;
    sliderValue3.innerHTML = slider3.value;
    sliderValue4.innerHTML = slider4.value;

    // Update the current slider value each time the slider is moved
    slider1.oninput = function() {
        sliderValue1.innerHTML = this.value;
    }
    slider2.oninput = function() {
        sliderValue2.innerHTML = this.value;
    }
    slider3.oninput = function() {
        sliderValue3.innerHTML = this.value;
    }
    slider4.oninput = function() {
        sliderValue4.innerHTML = this.value;
    }
}

// Add event listener to run the script after the document has loaded
document.addEventListener("DOMContentLoaded", initializeSliders);