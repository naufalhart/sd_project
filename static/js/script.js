document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('[data-collapse-toggle="navbar-default"]');
    const menu = document.getElementById('navbar-default');
    const backdrop = document.getElementById('menu-backdrop');
    
    function toggleMenu() {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
      
      // Remove hidden class and toggle show instead
      menu.classList.remove('hidden');
      menu.classList.toggle('show');
      backdrop.classList.toggle('show');
    }
    
    button.addEventListener('click', toggleMenu);
    backdrop.addEventListener('click', toggleMenu);
  });

  document.addEventListener('DOMContentLoaded', function() {
    const dropdownButtons = document.querySelectorAll('.group button');
    
    dropdownButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        const dropdown = button.nextElementSibling;
        dropdown.classList.toggle('show');
        
        // Close other dropdowns
        document.querySelectorAll('.dropdown-content').forEach(content => {
          if (content !== dropdown) {
            content.classList.remove('show');
          }
        });
      });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.group')) {
        document.querySelectorAll('.dropdown-content').forEach(dropdown => {
          dropdown.classList.remove('show');
        });
      }
    });
  });

  document.getElementById("cart-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Mencegah reload halaman

    let form = event.target;
    let formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        body: formData
    }).then(response => {
        if (response.ok) {
            showSuccessAlert();
        } else {
            alert("Failed to add to cart");
        }
    }).catch(error => {
        console.error("Error:", error);
    });
});

function showSuccessAlert() {
    let alertBox = document.getElementById("success-alert");
    alertBox.style.display = "flex"; // Menampilkan alert
}

function dismissAlert() {
    document.getElementById("success-alert").style.display = "none"; // Menutup alert
}

document.addEventListener("DOMContentLoaded", function () {
  var mainSlider = new Swiper(".main-slider", {
      loop: true,
      spaceBetween: 10,
      navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
      },
      thumbs: {
          swiper: thumbnailSlider,
      },
  });

  var thumbnailSlider = new Swiper(".thumbnail-slider", {
      loop: true,
      spaceBetween: 10,
      slidesPerView: 4,
      freeMode: true,
      watchSlidesProgress: true,
  });

  mainSlider.params.thumbs.swiper = thumbnailSlider;
  mainSlider.init();
});