// Custom JavaScript for Convergence Documentation

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll behavior for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy feedback for code blocks
    const copyButtons = document.querySelectorAll('.copybtn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.textContent;
            this.textContent = '✓ Copied!';
            setTimeout(() => {
                this.textContent = originalText;
            }, 2000);
        });
    });

    // Add search enhancement
    const searchInput = document.querySelector('.sidebar-search-container input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.parentElement.classList.add('searching');
            } else {
                this.parentElement.classList.remove('searching');
            }
        });
    }

    // Console welcome message
    console.log('%c🚀 Welcome to Convergence! ☀️', 
                'font-size: 20px; font-weight: bold; color: #7C4DFF;');
    console.log('%cWhere minds meet in the digital ether.', 
                'font-size: 14px; font-style: italic; color: #666;');
});