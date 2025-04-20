// Mobile Menu Functions
function toggleMobileMenu() {
    const nav = document.getElementById('mobileNav');
    nav.classList.toggle('active');
    
    // Animate hamburger menu
    const menuBtn = document.querySelector('.mobile-menu-btn');
    menuBtn.classList.toggle('active');
}

function closeMobileMenu() {
    const nav = document.getElementById('mobileNav');
    nav.classList.remove('active');
    
    // Reset hamburger menu
    const menuBtn = document.querySelector('.mobile-menu-btn');
    menuBtn.classList.remove('active');
}

function toggleDropdown(event) {
    event.preventDefault();
    const dropdownMenu = event.target.nextElementSibling;
    dropdownMenu.classList.toggle('show');
}

// Close mobile menu when clicking outside
document.addEventListener('click', (event) => {
    const nav = document.getElementById('mobileNav');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (!nav.contains(event.target) && !menuBtn.contains(event.target)) {
        closeMobileMenu();
    }
});