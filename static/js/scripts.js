document.addEventListener("DOMContentLoaded", function () {
    // Hamburger Menu Toggle and Navbar
    const menuToggle = document.getElementById('mobile-menu');
    const navbar = document.querySelector('.navbar');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Toggle the main menu (nav items)
    menuToggle.addEventListener('click', () => {
        navbar.classList.toggle('active');
        menuToggle.classList.toggle('open');
    });

    // Toggle dropdowns only in mobile view
    dropdowns.forEach(drop => {
        drop.addEventListener('click', function (e) {
            if (window.innerWidth <= 768) {
                e.preventDefault(); // Prevent parent link
                this.classList.toggle('active');
            }
        });
    });

    // Optional: Close navbar when clicking a link (for single-page or auto-scroll navs)
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                navbar.classList.remove('active');
                menuToggle.classList.remove('open');
            }
        });
    });

    // Slider Functionality for Video/Images
    const slides = document.querySelectorAll('.video-slide');
    let currentIndex = 0;

    function showNextSlide() {
        slides[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % slides.length;
        slides[currentIndex].classList.add('active');
    }

    // Slide change every 3 seconds
    setInterval(showNextSlide, 3000);

    // Dropdown Menu Behavior (Closing if clicked outside)
    document.querySelectorAll('.dropdown').forEach(function(dropdown) {
        dropdown.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
        });
    });

    // Close the dropdown if clicked outside
    window.addEventListener('click', function(e) {
        document.querySelectorAll('.dropdown').forEach(function(dropdown) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    });
});
