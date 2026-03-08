"""
OpenQR: Professional QR Code Generator
Developed by: Pappas Konstantinos (kenpap)
Version: 1.0 (Clean Build)
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk
import qrcode
import os
import ctypes
import re

# --- CONFIGURATION & CONSTANTS ---
WINDOW_TITLE = "OpenQR: QR Code Generator"
WINDOW_SIZE = (1400, 900)
BG_COLOR_DARK = "#1a1a24"
ACCENT_COLOR = "#ff4d4d"
TITLEBAR_HEX_COLOR = 0x00241a1a  # BGR format for Windows API
URL_REGEX = r'^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/?|[/?]\S+)$'

# --- GLOBAL UI HANDLES ---
error_msg_id = None
entry_link = None
entry_filename = None
canvas = None

# --- LOGIC FUNCTIONS ---

def is_valid_url(url):
    """Validate if the provided string matches a URL pattern."""
    if not url: return True
    return re.match(URL_REGEX, url, re.IGNORECASE) is not None

def check_link_live(event=None):
    """Trigger live validation when the user leaves the input field."""
    content = entry_link.get().strip()
    if content and not is_valid_url(content):
        canvas.itemconfig(error_msg_id, text="Wrong Input: Enter a Link!")
    else:
        canvas.itemconfig(error_msg_id, text="")

def generate_qr():
    """Handle QR generation and file saving process."""
    link = entry_link.get().strip()
    filename = entry_filename.get().strip()
    
    # Final validation before proceeding
    if not link or not is_valid_url(link):
        canvas.itemconfig(error_msg_id, text="Wrong Input: Enter a Link!")
        return

    # Directory selection popup
    save_directory = filedialog.askdirectory(title="Select Destination Folder")
    if not save_directory: 
        return

    # File naming handling
    if not filename: 
        filename = "qr_code"
    if not filename.lower().endswith(".png"): 
        filename += ".png"

    try:
        # QR Engine Configuration
        qr = qrcode.QRCode(
            version=2, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=20, 
            border=2
        )
        qr.add_data(link)
        qr.make(fit=True)
        
        # Image creation
        img = qr.make_image(fill_color="black", back_color="white")
        full_path = os.path.join(save_directory, filename)
        img.save(full_path)
        
        # Cleanup and Success Feedback
        messagebox.showinfo("Success", f"QR Code generated successfully!\n\nSaved at: {full_path}")
        entry_link.delete(0, 'end')
        entry_filename.delete(0, 'end')
        canvas.itemconfig(error_msg_id, text="")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"An unexpected error occurred: {e}")

# --- INPUT FIXES & CONTEXT MENU ---

def paste_action(widget):
    """Handle clipboard pasting and trigger validation."""
    try:
        content = root.clipboard_get()
        widget.insert('insert', content)
        check_link_live()
    except tk.TclError: 
        pass

def show_context_menu(event):
    """Display right-click context menu."""
    menu.entryconfigure("Paste", command=lambda: paste_action(event.widget))
    menu.tk_popup(event.x_root, event.y_root)

def global_key_fix(event):
    """Ensure Ctrl+V/C/A work regardless of system keyboard language."""
    if event.state & 0x0004: # Control Mask
        if event.keycode == 86: # 'V' Key
            paste_action(event.widget)
            return "break"
        elif event.keycode == 67: # 'C' Key
            try:
                data = event.widget.get('sel.first', 'sel.last')
                root.clipboard_clear()
                root.clipboard_append(data)
            except: pass
            return "break"
        elif event.keycode == 65: # 'A' Key
            event.widget.selection_range(0, 'end')
            return "break"

# --- UI INITIALIZATION ---

root = tk.Tk()
root.title(WINDOW_TITLE)

# Set Application Icon
try:
    root.iconbitmap("app_logo.ico")
except:
    pass

# Window Positioning
win_w, win_h = WINDOW_SIZE
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w // 2) - (win_w // 2)
y = (screen_h // 2) - (win_h // 2)
root.geometry(f"{win_w}x{win_h}+{x}+{y}")
root.resizable(False, False)

# Right-click Menu Setup
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Paste")

# Windows 11 Dark Titlebar Integration
try:
    root.update()
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(TITLEBAR_HEX_COLOR)), 4)
except:
    pass

# Main Canvas Drawing
canvas = tk.Canvas(root, width=win_w, height=win_h, bd=0, highlightthickness=0)
canvas.place(x=0, y=0)

try:
    # Background Image Handling
    bg_img = Image.open("BACKGROUND_IMAGE.png").convert("RGBA")
    bg_img = bg_img.resize((win_w, win_h), Image.LANCZOS)
    
    # UI Overlay Drawing (Glassmorphism effect)
    overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Main Panel
    draw.rounded_rectangle((300, 280, 1100, 710), radius=25, fill=(0, 0, 0, 100)) 
    # Link Input Box
    draw.rounded_rectangle((400, 380, 1000, 425), radius=10, fill=(26, 26, 36, 255), outline=(85, 85, 102, 255), width=2)
    # Filename Input Box
    draw.rounded_rectangle((400, 500, 1000, 545), radius=10, fill=(26, 26, 36, 255), outline=(85, 85, 102, 255), width=2)
    # Generate Button Box
    draw.rounded_rectangle((525, 610, 875, 665), radius=15, fill=(26, 26, 36, 255), outline=(85, 85, 102, 255), width=2)
    
    # Apply Overlay
    final_bg = ImageTk.PhotoImage(Image.alpha_composite(bg_img, overlay))
    canvas.create_image(0, 0, image=final_bg, anchor="nw")
    canvas.image = final_bg
except:
    canvas.configure(bg="#1a1a1a")

# --- UI TEXT ELEMENTS ---
canvas.create_text(700, 355, text="Enter Link (URL):", fill="white", font=("Arial", 14, "bold"))
canvas.create_text(700, 475, text="Enter QR Code Name:", fill="white", font=("Arial", 14, "bold"))
canvas.create_text(700, 637, text="GENERATE QR CODE", fill="white", font=("Arial", 16, "bold"))

# Inline Error Message Label
error_msg_id = canvas.create_text(990, 402, text="", fill=ACCENT_COLOR, font=("Arial", 11, "bold"), anchor="e")

# --- INPUT FIELDS SETUP ---
entry_link = tk.Entry(root, font=("Arial", 15), bg=BG_COLOR_DARK, fg="white", bd=0, highlightthickness=0, insertbackground="white")
entry_link.place(x=415, y=387, width=380, height=31) 
entry_link.bind("<Key>", global_key_fix)
entry_link.bind("<Button-3>", show_context_menu)
entry_link.bind("<FocusOut>", check_link_live)

entry_filename = tk.Entry(root, font=("Arial", 15), bg=BG_COLOR_DARK, fg="white", bd=0, highlightthickness=0, insertbackground="white")
entry_filename.place(x=415, y=507, width=570, height=31)
entry_filename.bind("<Key>", global_key_fix)
entry_filename.bind("<Button-3>", show_context_menu)

# --- INTERACTIVE EVENT HANDLING ---
def on_click(event):
    """Check if the user clicked inside the 'Generate' button area."""
    if 525 <= event.x <= 875 and 610 <= event.y <= 665: 
        generate_qr()

def on_motion(event):
    """Change cursor to hand pointer when hovering over the button."""
    if 525 <= event.x <= 875 and 610 <= event.y <= 665: 
        canvas.config(cursor="hand2")
    else: 
        canvas.config(cursor="")

canvas.bind("<Button-1>", on_click)
canvas.bind("<Motion>", on_motion)

# Run Application
if __name__ == "__main__":
    root.mainloop()