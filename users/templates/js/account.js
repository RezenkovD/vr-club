function toggleOnePasswordVisibility(fieldId) {
    var field = document.getElementById(fieldId);
    var eyeIcon = document.getElementById('eye-icon-one');

    if (field.type === "password") {
        field.type = "text";
        eyeIcon.innerHTML = '<path d="M12 5.25C4.5 5.25 1.5 12 1.5 12C1.5 12 4.5 18.75 12 18.75C19.5 18.75 22.5 12 22.5 12C22.5 12 19.5 5.25 12 5.25Z" stroke="#4FB4FE" stroke-linecap="round" stroke-linejoin="round"/> <path d="M12 15.75C14.0711 15.75 15.75 14.0711 15.75 12C15.75 9.92893 14.0711 8.25 12 8.25C9.92893 8.25 8.25 9.92893 8.25 12C8.25 14.0711 9.92893 15.75 12 15.75Z" stroke="#4FB4FE" stroke-linecap="round" stroke-linejoin="round"/>';
    }
    else {
        field.type = "password";
        eyeIcon.innerHTML = '<path d="M4.5 3.75L19.5 20.25" /> <path d="M14.522 14.775C13.8338 15.4054 12.9334 15.7535 12.0001 15.75C11.2432 15.7499 10.5041 15.5208 9.87984 15.0928C9.25561 14.6647 8.77551 14.0579 8.50265 13.3519C8.22979 12.6459 8.17695 11.8739 8.35107 11.1373C8.52519 10.4007 8.91812 9.73406 9.47821 9.22498" /> <path d="M6.9375 6.43127C3.1125 8.36252 1.5 12 1.5 12C1.5 12 4.5 18.75 12 18.75C13.7574 18.7643 15.4929 18.3594 17.0625 17.5688" /> <path d="M19.5562 15.8531C21.6 14.025 22.5 12 22.5 12C22.5 12 19.5 5.25002 12 5.25002C11.3498 5.24874 10.7006 5.30205 10.0593 5.4094" /> <path d="M12.7031 8.31567C13.5006 8.46678 14.2273 8.87317 14.7735 9.47353C15.3198 10.0739 15.6559 10.8356 15.7313 11.6438" />';
    }
}
function toggleTwoPasswordVisibility(fieldId) {
    var field = document.getElementById(fieldId);
    var eyeIcon = document.getElementById('eye-icon-two');

    if (field.type === "password") {
        field.type = "text";
        eyeIcon.innerHTML = '<path d="M12 5.25C4.5 5.25 1.5 12 1.5 12C1.5 12 4.5 18.75 12 18.75C19.5 18.75 22.5 12 22.5 12C22.5 12 19.5 5.25 12 5.25Z" stroke="#4FB4FE" stroke-linecap="round" stroke-linejoin="round"/> <path d="M12 15.75C14.0711 15.75 15.75 14.0711 15.75 12C15.75 9.92893 14.0711 8.25 12 8.25C9.92893 8.25 8.25 9.92893 8.25 12C8.25 14.0711 9.92893 15.75 12 15.75Z" stroke="#4FB4FE" stroke-linecap="round" stroke-linejoin="round"/>';
    }
    else {
        field.type = "password";
        eyeIcon.innerHTML = '<path d="M4.5 3.75L19.5 20.25" /> <path d="M14.522 14.775C13.8338 15.4054 12.9334 15.7535 12.0001 15.75C11.2432 15.7499 10.5041 15.5208 9.87984 15.0928C9.25561 14.6647 8.77551 14.0579 8.50265 13.3519C8.22979 12.6459 8.17695 11.8739 8.35107 11.1373C8.52519 10.4007 8.91812 9.73406 9.47821 9.22498" /> <path d="M6.9375 6.43127C3.1125 8.36252 1.5 12 1.5 12C1.5 12 4.5 18.75 12 18.75C13.7574 18.7643 15.4929 18.3594 17.0625 17.5688" /> <path d="M19.5562 15.8531C21.6 14.025 22.5 12 22.5 12C22.5 12 19.5 5.25002 12 5.25002C11.3498 5.24874 10.7006 5.30205 10.0593 5.4094" /> <path d="M12.7031 8.31567C13.5006 8.46678 14.2273 8.87317 14.7735 9.47353C15.3198 10.0739 15.6559 10.8356 15.7313 11.6438" />';
    }
}
