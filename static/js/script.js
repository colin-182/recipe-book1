/* 1. MOBILE NAV TOGGLE - Toggles the .is-open class on the nav links when the hamburger button is clicked */
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('is-open');

        // Animate the hamburger into an X when open
        const isOpen = navLinks.classList.contains('is-open');
        const spans  = navToggle.querySelectorAll('span');

        if (isOpen) {
            spans[0].style.transform = 'translateY(7px) rotate(45deg)';
            spans[1].style.opacity   = '0';
            spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
        } else {
            spans[0].style.transform = '';
            spans[1].style.opacity   = '';
            spans[2].style.transform = '';
        }
    });

    // Close the mobile nav if user clicks outside of it
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('is-open');
            navToggle.querySelectorAll('span').forEach(s => {
                s.style.transform = '';
                s.style.opacity   = '';
            });
        }
    });
}

/* 2. FLASH MESSAGE AUTO-DISMISS Flash messages fade out automatically after 4 seconds so they don't clutter the screen */
document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
        flash.style.transition = 'opacity 0.5s ease';
        flash.style.opacity    = '0';
        setTimeout(() => flash.remove(), 500);
    }, 4000);
});

/* 3. LIVE SEARCH FILTER - On the recipes page, filters the visible cards in real time as the user types — without a full page reload */
const searchInput = document.querySelector('.filters__input');

if (searchInput) {
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.recipe-card');

        cards.forEach(card => {
            const title    = card.querySelector('.recipe-card__title')?.textContent.toLowerCase() || '';
            const tags     = card.querySelector('.recipe-card__tags')?.textContent.toLowerCase()  || '';
            const category = card.dataset.category?.toLowerCase() || '';

            const matches = title.includes(query) || tags.includes(query) || category.includes(query);
            card.style.display = matches ? '' : 'none';
        });

        // Show empty state message if no cards are visible
        const grid       = document.querySelector('.recipe-grid');
        const visibleCards = grid ? [...grid.querySelectorAll('.recipe-card')]
                                        .filter(c => c.style.display !== 'none') : [];

        let noResults = document.getElementById('no-results-msg');

        if (visibleCards.length === 0 && grid) {
            if (!noResults) {
                noResults = document.createElement('p');
                noResults.id        = 'no-results-msg';
                noResults.className = 'empty-state__text';
                noResults.style.padding = '24px 0';
                noResults.textContent   = 'No recipes match your search.';
                grid.after(noResults);
            }
        } else if (noResults) {
            noResults.remove();
        }
    });
}

/* 4. DELETE CONFIRMATION - Adds a confirmation prompt before any delete form is submitted — prevents accidental deletes */
document.querySelectorAll('.form--delete').forEach(form => {
    form.addEventListener('submit', (e) => {
        const confirmed = window.confirm('Are you sure you want to delete this recipe? This cannot be undone.');
        if (!confirmed) {
            e.preventDefault();
        }
    });
});

/* 5. INGREDIENT CHECKBOX TOGGLE - On the recipe detail page, lets users tick off ingredients as they cook — purely cosmetic, no data is saved */
document.querySelectorAll('.ingredients-list__item').forEach(item => {
    item.style.cursor = 'pointer';

    item.addEventListener('click', () => {
        item.classList.toggle('is-checked');

        const icon = item.querySelector('.ingredients-list__check');

        if (item.classList.contains('is-checked')) {
            item.style.opacity        = '0.45';
            item.style.textDecoration = 'line-through';
            if (icon) icon.style.color = 'var(--green)';
        } else {
            item.style.opacity        = '';
            item.style.textDecoration = '';
            if (icon) icon.style.color = '';
        }
    });
});

/* 6. SMOOTH SCROLL - Smooth scrolls to any anchor link on the page */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

/* 
   7. FORM CHARACTER COUNTERS - Shows a live character count under the description textarea on the add/edit form */
const descriptionField = document.getElementById('description');

if (descriptionField) {
    const counter       = document.createElement('small');
    counter.className   = 'form-hint';
    counter.style.textAlign = 'right';
    counter.style.display   = 'block';
    descriptionField.after(counter);

    const updateCounter = () => {
        const len = descriptionField.value.length;
        const max = 300;
        counter.textContent = `${len} / ${max} characters`;
        counter.style.color = len > max ? 'var(--red)' : 'var(--brown-muted)';
    };

    descriptionField.addEventListener('input', updateCounter);
    updateCounter(); // run on page load in case of pre-filled edit form
}