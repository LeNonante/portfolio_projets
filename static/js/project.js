document.addEventListener('DOMContentLoaded', function () {
    const thumbs = Array.from(document.querySelectorAll('.pd-gallery .thumb img'));
    if (!thumbs.length) return;

    const lightbox = document.getElementById('lightbox');
    const lbImage = document.getElementById('lb-image');
    const lbCaption = document.getElementById('lb-caption');
    const closeBtn = document.querySelector('.lb-close');
    const prevBtn = document.querySelector('.lb-prev');
    const nextBtn = document.querySelector('.lb-next');

    let current = 0;

    function open(index) {
        current = index;
        const img = thumbs[current];
        lbImage.src = img.src;
        lbImage.alt = img.alt || '';
        lbCaption.textContent = '';
        lightbox.classList.add('show');
        lightbox.setAttribute('aria-hidden', 'false');
        // lock scroll
        document.documentElement.style.overflow = 'hidden';
        // focus close for accessibility
        closeBtn.focus();
    }

    function close() {
        lightbox.classList.remove('show');
        lightbox.setAttribute('aria-hidden', 'true');
        document.documentElement.style.overflow = '';
    }

    function showNext(delta) {
        current = (current + delta + thumbs.length) % thumbs.length;
        const img = thumbs[current];
        lbImage.src = img.src;
        lbImage.alt = img.alt || '';
        lbCaption.textContent = '';
    }

    thumbs.forEach((img, i) => {
        const wrapper = img.closest('.thumb');
        if (!wrapper) return;
        wrapper.addEventListener('click', () => open(i));
        wrapper.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(i);
            }
        });
    });

    closeBtn && closeBtn.addEventListener('click', close);
    nextBtn && nextBtn.addEventListener('click', () => showNext(1));
    prevBtn && prevBtn.addEventListener('click', () => showNext(-1));

    lightbox && lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) close();
    });

    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('show')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowRight') showNext(1);
        if (e.key === 'ArrowLeft') showNext(-1);
    });
});
