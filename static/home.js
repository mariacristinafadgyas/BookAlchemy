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