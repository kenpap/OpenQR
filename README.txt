=====================================================
          OpenQR: QR Code Generator 🚀
=====================================================

OpenQR is a professional, lightweight, and user-friendly 
desktop application designed to generate high-quality 
QR codes instantly. Built with Python and featuring 
a modern "glassmorphism" interface.

-----------------------------------------------------
✨ MAIN FEATURES
-----------------------------------------------------
* Modern UI: Sleek dark-themed interface.
* Live Validation: Instant feedback for invalid URLs.
* Smart Export: Auto-prompts for destination folder.
* Multi-Language Fix: Ctrl+C/V/A work in any language.
* Context Menu: Right-click "Paste" functionality.
* High Quality: Clean .png files (optimized border=2).

-----------------------------------------------------
🛠️ INSTALLATION & REQUIREMENTS
-----------------------------------------------------
To run the source code, you need Python 3.x and:
> pip install pillow qrcode

Required Assets in the same folder:
- OpenQR.py
- BACKGROUND_IMAGE.png
- app_logo.ico

-----------------------------------------------------
🚀 HOW TO USE
-----------------------------------------------------
1. Launch the application (OpenQR.py or OpenQR.exe).
2. Enter the Link: Paste your URL in the first box.
3. Name the File: Enter the desired name for your QR.
4. Generate: Click the "GENERATE QR CODE" button.
5. Save: Select your folder in the popup window.

-----------------------------------------------------
📦 BUILDING THE EXE
-----------------------------------------------------
To create a standalone .exe, use PyInstaller:
> pyinstaller --noconsole --onefile --icon=app_logo.ico OpenQR.py

-----------------------------------------------------
👤 CREDITS
-----------------------------------------------------
Developed by: Pappas Konstantinos (kenpap)
Version: 1.0
=====================================================