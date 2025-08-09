// Hotdog clicker logic
const hotdogImage = document.getElementById('hotdog-image');
const manageItemsButton = document.getElementById('manage-items-button');
let clickCount = 0;
const requiredClicks = 5;

// Initially hide the button
if (manageItemsButton) {
    manageItemsButton.style.display = 'none';
}

if (hotdogImage) {
    hotdogImage.addEventListener('click', () => {
        clickCount++;
        if (clickCount >= requiredClicks) {
            if (manageItemsButton) {
                manageItemsButton.style.display = 'block'; // Or 'inline-block' depending on layout
            }
        }
    });
}


// Theme toggle logic
const themeToggleBtn = document.getElementById('theme-toggle');
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Set initial icon
if (themeToggleDarkIcon && themeToggleLightIcon) {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        themeToggleLightIcon.classList.remove('hidden');
    } else {
        themeToggleDarkIcon.classList.remove('hidden');
    }
}


if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function() {
        // toggle icons inside button
        if (themeToggleDarkIcon && themeToggleLightIcon) {
            themeToggleDarkIcon.classList.toggle('hidden');
            themeToggleLightIcon.classList.toggle('hidden');
        }


        // if set via local storage previously
        if (localStorage.getItem('theme')) {
            if (localStorage.getItem('theme') === 'light') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            }

        // if NOT set via local storage previously
        } else {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            }
        }
    });
}
