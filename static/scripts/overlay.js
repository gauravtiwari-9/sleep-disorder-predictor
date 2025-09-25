const images = document.querySelectorAll('.analysis-container img');
const overlay = document.getElementById('overlay');
const popupImage = document.getElementById('popup-image');

// Function to show the image in the overlay
images.forEach(image => {
  image.addEventListener('click', () => {
    overlay.style.display = 'flex';
    popupImage.src = image.src;
  });
});

// Close the overlay when clicking outside the image (on the overlay background)
overlay.addEventListener('click', (e) => {
  if (e.target === overlay) {
    overlay.style.display = 'none';
  }
});
