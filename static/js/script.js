function validatePassword() {
    var passwordInput = document.getElementById('password');
    var password = passwordInput.value;

    // Asegura que la contraseña tenga al menos una mayúscula
    if (!/[A-Z]/.test(password)) {
        alert('La contraseña debe contener al menos una mayúscula.');
        passwordInput.value = '';
        return false;
    }

    return true;
}
function appendToDisplay(value) {
    document.getElementById('display').value += value;
}

function clearDisplay() {
    document.getElementById('display').value = '';
}

function calculateResult() {
    var result = eval(document.getElementById('display').value);
    document.getElementById('display').value = result;
}