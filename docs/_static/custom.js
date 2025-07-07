// Hacker-themed JavaScript for Convergence Documentation

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Enhanced copy feedback with hacker theme
    const copyButtons = document.querySelectorAll('.copybtn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.textContent;
            this.textContent = '✓ Copied!';
            this.style.background = 'rgba(91, 79, 255, 0.2)';
            setTimeout(() => {
                this.textContent = originalText;
                this.style.background = '';
            }, 1500);
        });
    });

    // Enhance search input with hacker-themed placeholder rotation
    const searchInput = document.querySelector('.sidebar-search-container input');
    if (searchInput) {
        const placeholders = [
            'Search the matrix...',
            'Query the convergence...',
            'Find your path...',
            'Enter search term...',
            'Explore the docs...'
        ];
        let currentIndex = 0;
        
        // Set initial placeholder
        searchInput.placeholder = placeholders[0];
        
        // Rotate placeholders on focus
        searchInput.addEventListener('focus', function() {
            currentIndex = (currentIndex + 1) % placeholders.length;
            this.placeholder = placeholders[currentIndex];
        });
    }
});