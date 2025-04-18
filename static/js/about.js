// Contact form submission
document.querySelector('.php-email-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const loading = form.querySelector('.loading');
    const errorMessage = form.querySelector('.error-message');
    const sentMessage = form.querySelector('.sent-message');
    const statusDiv = form.querySelector('.my-3'); // Get the parent div
  
    statusDiv.style.display = 'block'; // Show the parent div
    loading.style.display = 'block';
    errorMessage.style.display = 'none';
    sentMessage.style.display = 'none';
  
    fetch('/contact', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        if (data.success) {
            sentMessage.style.display = 'block';
            form.reset();
        } else {
            errorMessage.textContent = data.error || 'An error occurred';
            errorMessage.style.display = 'block';
        }
    })
    .catch(() => {
        loading.style.display = 'none';
        errorMessage.textContent = 'An error occurred. Please try again.';
        errorMessage.style.display = 'block';
    });
  });


  // FAQ TimeOut Simulator ! 
  document.addEventListener('DOMContentLoaded', function () {
    const faqLink = document.getElementById('faq-link'); // The FAQ link in the header
    const faqButton = document.getElementById('faq-question-1'); // First FAQ question button

    faqLink.addEventListener('click', function (event) {
      setTimeout(() => {
        faqButton.click(); // Simulate a click on the first FAQ question button
      }, 500); // Delay to allow smooth scrolling before clicking
    });
  });

