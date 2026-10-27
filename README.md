# Spook & Swirl 🎃✨ - Tech Fest Design Menu (Pinterest Style)

A clean, minimalist Pinterest-style image menu designed to showcase festival designs.

## Highlights
- **Pure Visuals**: No prices, no titles/names, and no category badges on the cards — clean, edge-to-edge Pinterest pin aesthetics.
- **Two Distinct Themes**:
  - **Face Paint**: Spooky Halloween theme (Creepster typography, dark violet background with toxic & pumpkin neon glows).
  - **Mehendi**: Royal Festive Henna theme (Cinzel serif typography, warm terracotta and glowing gold tones).
- **Design Numbers & Fast Search**: Every design has a simple round number badge (`#1`, `#2`, `#3`...) on the card and in the modal header. Search bar allows visitors to find any design number instantly.
- **Lightbox & True "Only Image" Fullscreen Mode**: Click/tap any design to view details with zoom controls. Tap the **Fullscreen Button** to enter pure full-screen mode where all toolbars, badges, and controls are hidden, leaving **only the image** filling the entire screen edge-to-edge.
- **GitHub Pages Ready**: Pure static HTML/CSS/JS with zero dependencies. Works directly from GitHub Pages or locally.

---

## 📂 Folder Layout
```
D:\tech_fest\
├── index.html            # Main visual menu
├── gallery-data.js       # List of image filenames
├── update-gallery.ps1    # Auto-updates gallery-data.js when you drop in new photos
├── face paint\           # Put all Halloween face paint photos here
└── mehendi\              # Put all henna/mehendi photos here
```

---

## ⚡ Adding More Photos
Whenever you paste new photos into `face paint` or `mehendi`:
1. Right-click `update-gallery.ps1` and select **Run with PowerShell** (or run `powershell ./update-gallery.ps1`).
2. It will automatically re-index all image files into `gallery-data.js`.
3. Commit and push to GitHub!

---

## 🌐 Deploy to GitHub Pages

1. **Initialize Git**:
   ```bash
   git init
   git add .
   git commit -m "Tech Fest visual menu"
   ```

2. **Push to GitHub**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

3. **Turn on Pages**:
   - Go to your repository on GitHub.
   - Go to **Settings** → **Pages**.
   - Under **Build and deployment > Source**, choose `Deploy from a branch`.
   - Select branch `main` and folder `/ (root)`, then click **Save**.
