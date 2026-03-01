// Gestion de l'animation du hamburger
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger-btn');
    const navCollapse = document.querySelector('#navbarContent');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (hamburger && navCollapse) {
        // Écouter les événements Bootstrap collapse
        navCollapse.addEventListener('show.bs.collapse', function() {
            hamburger.setAttribute('aria-expanded', 'true');
        });
        
        navCollapse.addEventListener('hide.bs.collapse', function() {
            hamburger.setAttribute('aria-expanded', 'false');
        });
        
        // Fermer le menu au clic sur un lien (mobile)
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992 && navCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navCollapse, {
                        toggle: true
                    });
                }
            });
        });
    }
});