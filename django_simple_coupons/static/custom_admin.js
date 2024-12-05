document.addEventListener('DOMContentLoaded', (event) => {
    const addButton = document.querySelector('.object-tools .addlink');
    if (addButton) {
        const customButton = document.createElement('a');
        customButton.href = customButtonUrl;
        customButton.className = 'btn btn-primary';
        customButton.textContent = 'Mój przycisk';
        addButton.parentNode.insertBefore(customButton, addButton.nextSibling);
    }
});