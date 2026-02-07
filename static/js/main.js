document.addEventListener('DOMContentLoaded', function () {
    // --- Category Filtering Logic ---
    const filterButtons = document.querySelectorAll('.filter-btn');
    const categorySections = document.querySelectorAll('section[id^="category-"]');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Manage active button state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const filter = this.getAttribute('data-filter');

            categorySections.forEach(section => {
                if (filter === 'all' || section.id === filter) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        });
    });

    // --- Modal Demo Logic ---
    const demoModal = document.getElementById('demoModal');
    if (demoModal) {
        const iframe = demoModal.querySelector('iframe');
        const modalTitle = demoModal.querySelector('.modal-title');

        demoModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const demoUrl = button.getAttribute('data-demo-url');
            const demoTitle = button.getAttribute('data-demo-title');
            
            modalTitle.textContent = 'Vista Previa: ' + demoTitle;
            iframe.setAttribute('src', demoUrl);
        });

        // Clear iframe src when modal is closed to stop video/audio playback
        demoModal.addEventListener('hidden.bs.modal', function () {
            iframe.setAttribute('src', '');
        });
    }
});
