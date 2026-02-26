// Artwork preview
const artworkUpload = document.getElementById('artwork-upload');
const artworkPreview = document.getElementById('artwork-preview');
const approveBtn = document.getElementById('approve-btn');
const amendBtn = document.getElementById('amend-btn');
const amendText = document.getElementById('amend-text');
const submitBtn = document.getElementById('submit-btn');
const clientEmail = document.getElementById('client-email');
const formMessage = document.getElementById('form-message');
const fileChosen = document.getElementById('file-chosen');
const customFileLabel = document.getElementById('custom-file-label');

let approvalStatus = '';

artworkUpload.addEventListener('change', function() {
  artworkPreview.innerHTML = '';
  const file = this.files[0];
  if (customFileLabel) customFileLabel.textContent = file ? file.name : 'Choose Artwork File';
  if (!file) return;
  if (file.type.startsWith('image/')) {
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.onload = () => URL.revokeObjectURL(img.src);
    img.style.objectFit = 'contain';
    artworkPreview.appendChild(img);
  } else if (file.type === 'application/pdf') {
    const embed = document.createElement('embed');
    embed.src = URL.createObjectURL(file);
    embed.type = 'application/pdf';
    embed.width = '100%';
    embed.height = '100%';
    artworkPreview.appendChild(embed);
  } else {
    artworkPreview.textContent = 'Preview not available for this file type.';
  }
});

approveBtn.addEventListener('click', function() {
  approvalStatus = 'approved';
  approveBtn.classList.add('active');
  amendBtn.classList.remove('active');
  amendText.style.display = 'none';
});

amendBtn.addEventListener('click', function() {
  approvalStatus = 'amend';
  amendBtn.classList.add('active');
  approveBtn.classList.remove('active');
  amendText.style.display = 'block';
  amendText.focus();
});

submitBtn.addEventListener('click', function() {
  formMessage.textContent = '';
  const email = clientEmail.value.trim();
  if (!email) {
    formMessage.textContent = 'Please enter your email.';
    formMessage.style.color = '#e74c3c';
    return;
  }
  if (!approvalStatus) {
    formMessage.textContent = 'Please select Approve or Amend.';
    formMessage.style.color = '#e74c3c';
    return;
  }
  let subject = 'Artwork Approval Response';
  let body = `Client Email: ${email}%0D%0A`;
  if (approvalStatus === 'approved') {
    body += 'Status: Approved%0D%0A';
  } else {
    body += 'Status: Amend Requested%0D%0A';
    body += `Requested Changes: ${encodeURIComponent(amendText.value)}%0D%0A`;
  }
  // Optionally include artwork file name
  if (artworkUpload.files[0]) {
    body += `Artwork File: ${artworkUpload.files[0].name}%0D%0A`;
  }
  // Replace with your client's email address
  const recipient = 'yourclient@email.com';
  window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${body}`;
  formMessage.textContent = 'Thank you! Your response has been prepared in your email client.';
  formMessage.style.color = '#27ae60';
}); 