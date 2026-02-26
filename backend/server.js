const express = require('express');
const multer = require('multer');
const nodemailer = require('nodemailer');
const { v4: uuidv4 } = require('uuid');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3001;

// Storage for uploaded files
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => cb(null, uuidv4() + path.extname(file.originalname))
});
const upload = multer({ storage });

// In-memory DB for demo (replace with real DB for production)
const artworkDB = {};

app.use(express.json());
app.use('/uploads', express.static(uploadDir));

// Admin uploads artwork and sends to client
app.post('/api/upload', upload.single('artwork'), (req, res) => {
  const { clientEmail } = req.body;
  if (!req.file || !clientEmail) return res.status(400).json({ error: 'Missing file or client email' });
  const id = uuidv4();
  artworkDB[id] = {
    file: req.file.filename,
    clientEmail,
    status: 'pending',
    notes: ''
  };
  // Send email to client with review link
  sendClientEmail(clientEmail, id, req.file.filename)
    .then(() => res.json({ success: true, reviewUrl: `/review/${id}` }))
    .catch(err => res.status(500).json({ error: 'Failed to send email', details: err.message }));
});

// Serve review page (for demo, just returns JSON; replace with HTML in production)
app.get('/review/:id', (req, res) => {
  const { id } = req.params;
  const record = artworkDB[id];
  if (!record) return res.status(404).send('Not found');
  res.json({
    artworkUrl: `/uploads/${record.file}`,
    status: record.status,
    notes: record.notes
  });
});

// Client submits approval or amendment
app.post('/api/review/:id', (req, res) => {
  const { id } = req.params;
  const { action, notes, clientEmail } = req.body;
  const record = artworkDB[id];
  if (!record) return res.status(404).json({ error: 'Not found' });
  record.status = action;
  record.notes = notes || '';
  // Send email to admin
  sendAdminEmail(action, notes, record, clientEmail)
    .then(() => res.json({ success: true }))
    .catch(err => res.status(500).json({ error: 'Failed to send email', details: err.message }));
});

// Email sending functions (placeholders)
function sendClientEmail(clientEmail, id, filename) {
  // TODO: Replace with your domain
  const reviewUrl = `https://yourdomain.com/review/${id}`;
  const transporter = nodemailer.createTransport({
    host: 'smtp.example.com',
    port: 465,
    secure: true,
    auth: {
      user: 'your@email.com',
      pass: 'yourpassword'
    }
  });
  return transporter.sendMail({
    from: 'no-reply@yourdomain.com',
    to: clientEmail,
    subject: 'Artwork Approval Request',
    html: `<p>Please review your artwork:</p><a href="${reviewUrl}">${reviewUrl}</a>`
  });
}

function sendAdminEmail(action, notes, record, clientEmail) {
  const transporter = nodemailer.createTransport({
    host: 'smtp.example.com',
    port: 465,
    secure: true,
    auth: {
      user: 'your@email.com',
      pass: 'yourpassword'
    }
  });
  let subject = 'Artwork Approval Response';
  let html = `<p>Client: ${clientEmail || record.clientEmail}</p>`;
  html += `<p>Status: ${action}</p>`;
  if (notes) html += `<p>Notes: ${notes}</p>`;
  html += `<p>Artwork: <a href="https://yourdomain.com/uploads/${record.file}">${record.file}</a></p>`;
  return transporter.sendMail({
    from: 'no-reply@yourdomain.com',
    to: 'contact@paperboyja.com',
    subject,
    html
  });
}

app.listen(PORT, () => console.log(`Server running on port ${PORT}`)); 