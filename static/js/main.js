    document.addEventListener('DOMContentLoaded', function() {
      // Initialize AOS
      AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });


      // Smooth scrolling for links with hash
      document.querySelectorAll('a.scrollto').forEach(link => {
        link.addEventListener('click', function(e) {
          if (document.querySelector(this.hash)) {
            e.preventDefault();
            
            const navbar = document.querySelector('.navbar');
            if (navbar.classList.contains('navbar-mobile')) {
              navbar.classList.remove('navbar-mobile');
              document.querySelector('.mobile-nav-toggle').classList.toggle('bi-list');
              document.querySelector('.mobile-nav-toggle').classList.toggle('bi-x');
            }
            
            const targetElement = document.querySelector(this.hash);
            window.scrollTo({
              top: targetElement.offsetTop,
              behavior: 'smooth'
            });
          }
        });
      });
    });
 
 