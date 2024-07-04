// validation.js

function validateForm() {
    var yearInput = document.getElementById('year');
    var year = parseInt(yearInput.value);
    var currentYear = parseInt(yearInput.dataset.currentYear); // Read current_year from data attribute

    if (isNaN(year) || year < 1888 || year > currentYear) {
        alert('Please enter a valid release year between 1888 and ' + currentYear + '.');
        return false;
    }

    return true;
}

