const navbar = document.getElementById('navbar');
const right = document.getElementById('right-screen');
navbar.addEventListener('click', () => {
    right.classList.toggle('right');
});