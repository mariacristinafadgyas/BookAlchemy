document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        var messages = flashMessages.querySelectorAll('.flash-message');
        if (messages.length === 0) {
            flashMessages.style.display = 'none'; // Hide if no messages are present
        } else {
            flashMessages.style.display = 'block'; // Show if messages are present
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const hueSlider = document.getElementById('hue-slider');
    const hueValue = document.getElementById('hue-value');

    function updateHue() {
        const hue = hueSlider.value;
        hueValue.textContent = hue;

        // When the user changes the hue it is being saved to localStorage
        localStorage.setItem('hue', hue);

        // Update CSS variables for the overall design
        document.documentElement.style.setProperty('--hue-color', hue);
        document.documentElement.style.setProperty('--light-background', `hsl(${hue}, 90%, 96%)`);
        document.documentElement.style.setProperty('--mid-background', `hsl(${hue}, 80%, 85%)`);
        document.documentElement.style.setProperty('--dark-text', `hsl(${hue}, 40%, 10%)`);
        document.documentElement.style.setProperty('--darker-text', `hsl(${hue}, 30%, 5%)`);
        document.documentElement.style.setProperty('--button-color', `hsl(${hue}, 80%, 50%)`);
        document.documentElement.style.setProperty('--button-hover-color', `hsl(${hue}, 80%, 45%)`);
        document.documentElement.style.setProperty('--flash-bg-color', `hsl(${hue}, 90%, 95%)`);
        document.documentElement.style.setProperty('--flash-border-color', `hsl(${hue}, 80%, 75%)`);
        document.documentElement.style.setProperty('--del-button-color', `hsl(${hue}, 10%, 40%)`);
        document.documentElement.style.setProperty('--del-button-hover-color', `hsl(${hue}, 30%, 20%)`);

        // Update the thumb color directly using CSS injected into the page
        hueSlider.style.setProperty('--thumb-color', `hsl(${hue}, 80%, 50%)`);

        // Apply inline styles to update the slider track and thumb colors
        hueSlider.style.background = `linear-gradient(to right, white, hsl(${hue}, 80%, 50%))`;
        hueSlider.style.setProperty('--webkit-slider-thumb', `hsl(${hue}, 80%, 50%)`);
        hueSlider.style.setProperty('--moz-range-thumb', `hsl(${hue}, 80%, 50%)`);
        hueSlider.style.setProperty('--ms-thumb', `hsl(${hue}, 80%, 50%)`);
    }

    hueSlider.addEventListener('input', updateHue);

    // Initialize with the saved hue or default
    const savedHue = localStorage.getItem('hue') || 58;
    hueSlider.value = savedHue;
    updateHue();
});

// Add custom styles for range slider directly via JS
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.innerHTML = `
        #hue-slider::-webkit-slider-runnable-track {
            background: white; /* Change the track color to white */
        }
        #hue-slider::-moz-range-track {
            background: white; /* Change the track color to white for Firefox */
        }
        #hue-slider::-ms-track {
            background: white; /* Change the track color to white for IE */
            border-color: transparent; /* Remove border */
            color: transparent; /* Remove color */
        }
        #hue-slider::-webkit-slider-thumb {
            background: var(--thumb-color); /* Dynamically set thumb color */
        }
        #hue-slider::-moz-range-thumb {
            background: var(--thumb-color); /* Dynamically set thumb color */
        }
        #hue-slider::-ms-thumb {
            background: var(--thumb-color); /* Dynamically set thumb color */
        }
    `;
    document.head.appendChild(style);
});
