document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletterForm');
    const newsletterMessage = document.getElementById('newsletterMessage');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
            
            // Clear previous messages
            if (newsletterMessage) {
                newsletterMessage.textContent = '';
                newsletterMessage.className = 'newsletter-message';
            }
            
            // Get form data
            const formData = new FormData(this);
            
            // Send AJAX request
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    if (newsletterMessage) {
                        newsletterMessage.textContent = data.message || 'Thank you for subscribing to our newsletter!';
                        newsletterMessage.className = 'newsletter-message success';
                    }
                    
                    // Reset form
                    newsletterForm.reset();
                    
                    // Hide message after 5 seconds
                    setTimeout(() => {
                        if (newsletterMessage) {
                            newsletterMessage.textContent = '';
                            newsletterMessage.className = 'newsletter-message';
                        }
                    }, 5000);
                } else {
                    // Show error message
                    if (newsletterMessage) {
                        newsletterMessage.textContent = data.message || 'An error occurred. Please try again.';
                        newsletterMessage.className = 'newsletter-message error';
                    }
                    
                    // Show form errors if any
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([field, errors]) => {
                            const input = newsletterForm.querySelector(`[name="${field}"]`);
                            if (input) {
                                const errorDiv = document.createElement('div');
                                errorDiv.className = 'error-message';
                                errorDiv.textContent = errors[0];
                                input.parentNode.insertBefore(errorDiv, input.nextSibling);
                            }
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (newsletterMessage) {
                    newsletterMessage.textContent = 'An error occurred. Please try again later.';
                    newsletterMessage.className = 'newsletter-message error';
                }
            })
            .finally(() => {
                // Reset button state
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            });
        });
    }
});
