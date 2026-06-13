<div align="center">

<h1>🔐 CipherPixel</h1>
<h3>Advanced Image Encryption Tool using Pixel Manipulation</h3>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.4-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-12.2-FF6F61?style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

<br/>

> **CipherPixel** is a cybersecurity-focused web application that encrypts and decrypts images using pixel-level manipulation algorithms — XOR, Pixel Swap, Mathematical Operations, Channel Shift, and Arnold's Cat Map.

<br/>

[🔒 Encrypt](#-how-to-use) · [🔓 Decrypt](#-how-to-use) · [📜 History](#-pages) · [⬡ About](#-encryption-algorithms)

</div>

---

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Encryption Algorithms](#-encryption-algorithms)
- [Tech Stack & Tools](#-tech-stack--tools)
- [Pages](#-pages)
- [Installation & Setup](#-installation--setup)
- [How to Use](#-how-to-use)
- [API Endpoints](#-api-endpoints)
- [Cybersecurity Concepts](#-cybersecurity-concepts)
- [License](#-license)

---

## 📁 Project Structure

```
image-encryption-tool/
│
├── 📄 app.py                    # Flask backend — routes & REST API
├── 📄 encryption.py             # All 5 encryption algorithm implementations
├── 📄 requirements.txt          # Python dependencies
├── 📄 run.bat                   # One-click Windows launch script
│
├── 📂 templates/                # Jinja2 HTML templates
│   ├── base.html                # Base layout (navbar, footer, shared head)
│   ├── index.html               # 🏠 Home/Landing page
│   ├── encrypt.html             # 🔒 Image Encryption page
│   ├── decrypt.html             # 🔓 Image Decryption page
│   ├── history.html             # 📜 Operation History page
│   └── about.html               # ⬡ About & Security Concepts page
│
├── 📂 static/
│   ├── css/
│   │   └── style.css            # Full cyberpunk dark-theme stylesheet
│   └── js/
│       └── main.js              # Global JS — particles, toasts, animations
│
├── 📂 uploads/                  # Temp folder for uploaded images
├── 📂 outputs/                  # Folder for encrypted/decrypted outputs
└── 📄 history.json              # Persistent log of all operations
```

---

## ✨ Key Features

### 🔐 Encryption & Security
- **5 unique pixel manipulation algorithms** — each with full encryption + decryption support
- **Key-based encryption** — numeric key (0–255) seeds all algorithms
- **Lossless & reversible** — every operation has a perfect mathematical inverse
- **Key strength meter** — visual feedback on key security level
- **Key reminder banner** — warns you to save key + method after encryption

### 🖼️ Image Processing
- Supports **PNG, JPG, JPEG, BMP, GIF** formats
- Displays **before/after image comparison** panel
- Shows image **metadata** (dimensions, color mode)
- One-click **encrypted/decrypted file download**
- **Lightbox zoom** — click any result image to view full-size

### 🎨 UI / UX
- **Cyberpunk dark theme** with cyan & purple glow accents
- **Animated particle network** floating in background
- **Drag & drop** file upload zone
- **Glitch text** animation on hero title
- **Toast notification system** for success/warning/error
- **Ripple effects** on all buttons
- **Loading progress bar** on page transitions
- **Fully responsive** — works on desktop, tablet, mobile
- **Mobile hamburger menu**

### 📊 Dashboard
- **Operation History table** — logs every encrypt/decrypt session
- Stats: total operations, total encrypted, total decrypted
- Re-download any previous output directly from history
- Clear history with one click

---

## 🔬 Encryption Algorithms

| Algorithm | Type | Complexity | Security Level |
|-----------|------|-----------|---------------|
| **XOR Cipher** | Bitwise | O(n) | ⭐⭐ Basic |
| **Pixel Swap** | Permutation | O(n) | ⭐⭐⭐ Medium |
| **Math Operations** | Arithmetic | O(n) | ⭐⭐⭐ Medium |
| **Channel Shift** | Color-space | O(n) | ⭐⭐⭐ Medium |
| **Arnold Cat Map** | Chaotic | O(n²) | ⭐⭐⭐⭐ High |

### ⊕ XOR Cipher
Each pixel's RGB channels are XORed with the key byte. Since XOR is self-inverse (`A ⊕ K ⊕ K = A`), the same operation encrypts and decrypts.
```
Encrypt: pixel[i] = pixel[i] XOR key
Decrypt: pixel[i] = encrypted[i] XOR key
```

### ⇄ Pixel Swap (Fisher-Yates Shuffle)
Pixels are shuffled to random positions using a **key-seeded** pseudorandom permutation. Pixel values are unchanged, but positions are scrambled.
```
indices = Fisher-Yates shuffle(seed = key)
encrypted[indices[i]] = original[i]
```

### ∑ Mathematical Operations
Arithmetic (add, subtract, multiply) or bitwise (AND, OR) applied to every pixel with **modular wraparound** at 256.
```
Add:       E[i] = (P[i] + key) mod 256
Subtract:  E[i] = (P[i] - key) mod 256
Multiply:  E[i] = (P[i] × key) mod 256
```

### RGB Channel Shift
RGB channels are **rotated** (R→G, G→B, B→R) and each channel's values are independently shifted by key multiples.
```
R_enc = (G + key)     mod 256
G_enc = (B + key×2)   mod 256
B_enc = (R + key×3)   mod 256
```

### ∞ Arnold's Cat Map
A **chaotic dynamical system** from ergodic theory. Applies a nonlinear matrix transformation to pixel coordinates over `n` iterations.
```
[x']   [1 1] [x]
[y'] = [1 2] [y]  (mod N)

Inverse:  x = 2x' - y'  (mod N)
          y = -x' + y'  (mod N)
```

---

## 🛠️ Tech Stack & Tools

### Backend
| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.10+ | Core language |
| **Flask** | 3.0 | Web framework & REST API server |
| **NumPy** | 2.4 | Vectorized pixel array operations |
| **Pillow (PIL)** | 12.2 | Image I/O — open, convert, save |
| **Werkzeug** | 3.0 | File upload security (`secure_filename`) |
| **hashlib** | stdlib | Key hashing for non-numeric inputs |
| **uuid** | stdlib | Unique file ID generation |

### Frontend
| Tool | Purpose |
|------|---------|
| **HTML5** | Semantic page structure, file input, drag-drop API |
| **CSS3** | Animations, glassmorphism, keyframes, CSS Grid/Flexbox |
| **Vanilla JavaScript (ES6+)** | Async Fetch API, DOM manipulation, Canvas particles |
| **Google Fonts** | Orbitron (display), Inter (body), JetBrains Mono (code) |

### Design Techniques
| Technique | Where Used |
|-----------|-----------|
| **Glassmorphism** | Cards, panels, navbar |
| **CSS Custom Properties** | Entire design token system |
| **Canvas API** | Animated particle network background |
| **IntersectionObserver API** | Entrance animations on scroll |
| **CSS keyframe animations** | Glitch effect, pulse glow, ring rotation |
| **Backdrop-filter blur** | Navbar, toast, lightbox overlay |

### Cybersecurity Concepts Applied
| Concept | Implementation |
|---------|---------------|
| **Symmetric Encryption** | Same key encrypts and decrypts |
| **Shannon's Confusion** | XOR obscures key-ciphertext relationship |
| **Shannon's Diffusion** | Pixel swap spreads plaintext statistics |
| **Pseudorandomness** | Mersenne Twister PRNG (Python `random.Random`) |
| **Modular Arithmetic** | Wrap-around for add/subtract/multiply ops |
| **Chaos Theory** | Arnold Cat Map from ergodic theory |
| **Permutation Cipher** | Fisher-Yates position scrambling |

---

## 📄 Pages

| # | Page | Route | Description |
|---|------|-------|-------------|
| 1 | 🏠 **Home** | `/` | Landing page — hero, features grid, how-it-works, CTA |
| 2 | 🔒 **Encrypt** | `/encrypt` | Upload image, configure algorithm & key, download result |
| 3 | 🔓 **Decrypt** | `/decrypt` | Upload encrypted image, reverse with same key |
| 4 | 📜 **History** | `/history` | Full log of all operations with download links |
| 5 | ⬡ **About** | `/about` | Algorithm docs, security concepts, tech stack |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/image-encryption-tool.git
cd image-encryption-tool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application

**Windows (one-click):**
```
Double-click run.bat
```

**Command line:**
```bash
python app.py
```

### 4. Open in Browser
```
http://127.0.0.1:5000
```

---

## 📖 How to Use

### Encrypting an Image
1. Go to **http://127.0.0.1:5000/encrypt**
2. Drag & drop an image or click to browse
3. Select an **encryption algorithm** from the panel
4. Enter a **numeric key** (0–255) — or click 🎲 for random
5. Click **🔒 Encrypt Image**
6. View the before/after comparison
7. Click **📥 Download Encrypted Image**
8. ⚠️ **Save your key and algorithm** — you need them to decrypt!

### Decrypting an Image
1. Go to **http://127.0.0.1:5000/decrypt**
2. Upload the encrypted image
3. Select the **exact same algorithm** used during encryption
4. Enter the **exact same key**
5. Click **🔓 Decrypt Image** → original image restored!

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page |
| `GET` | `/encrypt` | Encrypt page |
| `GET` | `/decrypt` | Decrypt page |
| `GET` | `/history` | History page |
| `GET` | `/about` | About page |
| `POST` | `/api/encrypt` | Encrypt an image (multipart/form-data) |
| `POST` | `/api/decrypt` | Decrypt an image (multipart/form-data) |
| `GET` | `/api/preview/<filename>` | Preview output image inline |
| `GET` | `/api/download/<filename>` | Download output image |
| `POST` | `/api/history/clear` | Clear operation history |

### POST `/api/encrypt` — Form Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | file | ✅ | Image file (PNG/JPG/BMP) |
| `method` | string | ✅ | `xor` / `pixel_swap` / `math_op` / `channel_shift` / `arnold_cat` |
| `key` | integer | ✅ | Encryption key (0–255) |
| `operation` | string | Only for `math_op` | `add` / `subtract` / `multiply` / `bitwise_and` / `bitwise_or` |
| `iterations` | integer | Only for `arnold_cat` | Number of cat map iterations (1–20) |

---

## 🛡️ Cybersecurity Concepts

This project demonstrates the following cryptographic fundamentals:

- **Symmetric Key Cryptography** — same key for encryption & decryption
- **Confusion** (Shannon, 1949) — XOR obscures the relationship between key and ciphertext
- **Diffusion** (Shannon, 1949) — pixel swap spreads plaintext information across ciphertext
- **Histogram Analysis** — pixel swap preserves histogram; XOR & math ops change it
- **PRNG Seeding** — deterministic but statistically random permutations from a seed
- **Chaos Theory in Cryptography** — chaotic maps for pixel scrambling (Arnold Cat Map)
- **Modular Arithmetic** — all operations wrap safely within 0–255 byte range

> ⚠️ **Disclaimer:** This tool is for **educational purposes only**. For production-grade security, use AES-256, RSA, or ChaCha20 from audited cryptography libraries.

---

## 📦 requirements.txt

```
flask>=3.0.0
pillow>=10.0.0
numpy>=1.26.0
werkzeug>=3.0.0
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-algorithm`)
3. Commit your changes (`git commit -m 'Add new encryption method'`)
4. Push to the branch (`git push origin feature/new-algorithm`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with 🔐 Python · Flask · NumPy · Pillow · CSS3 · JavaScript**

⭐ Star this repo if you found it useful!

</div>
