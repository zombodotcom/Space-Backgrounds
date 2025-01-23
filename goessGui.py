import os
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from bs4 import BeautifulSoup
import re
import threading
import time

# Constants
BASE_URL = "https://www.star.nesdis.noaa.gov/goes/fulldisk_band.php"
SAVE_DIR = "satellite_images/GeoColor/1808x1808"
PARAMS = {"sat": "G16", "band": "GEOCOLOR", "length": 240, "dim": 1}
ANIMATION_INTERVAL = .2  # Seconds per wallpaper change

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)


def change_wallpaper(image_path, style):
    """Set the desktop wallpaper on Windows with the selected style."""
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02

    # Map style names to corresponding registry values
    style_map = {
        "Stretch": 2,
        "Center": 0,
        "Tile": 1,
        "Fit": 6,
        "Fill": 10,
    }

    try:
        # Validate the image path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Update the registry with the wallpaper style
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, str(style_map[style]))
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0" if style != "Tile" else "1")

        # Call Windows API to change wallpaper
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, os.path.abspath(image_path),
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )
        return True
    except Exception as e:
        print(f"Error changing wallpaper: {e}")
        messagebox.showerror("Error", f"Failed to set wallpaper: {e}")
        return False


def fetch_image_urls():
    """Fetch Astro image URLs from the NOAA website."""
    try:
        response = requests.get(BASE_URL, params=PARAMS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the script tag containing animationImages
        script_tag = soup.find("script", text=re.compile(r"animationImages\s*=\s*\["))
        if not script_tag:
            raise ValueError("GeoColor animationImages not found on the page.")

        # Extract animationImages array
        animation_images_match = re.search(r"animationImages\s*=\s*(\[[^\]]+\])", script_tag.string)
        if animation_images_match:
            animation_images_str = animation_images_match.group(1)
            image_urls = re.findall(r"'(https://[^']+)'", animation_images_str)
            return image_urls
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch images: {e}")
        return []


def download_images(image_urls):
    """Download Astro images and skip existing ones."""
    downloaded = []
    for url in image_urls:
        local_path = os.path.join(SAVE_DIR, os.path.basename(url))
        if os.path.exists(local_path):
            print(f"Image already exists: {local_path}")
            continue
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(response.content)
            downloaded.append(local_path)
            print(f"Downloaded: {url} -> {local_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    return downloaded


def get_existing_images():
    """Retrieve a list of existing images in the directory."""
    return [
        os.path.join(SAVE_DIR, file)
        for file in os.listdir(SAVE_DIR)
        if file.endswith((".jpg", ".jpeg", ".png"))
    ]


class WallpaperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astro Wallpaper Manager")
        self.selected_style = tk.StringVar(value="Fit")
        self.image_paths = []
        self.animating = False
        self.animation_thread = None

        self.create_gui()
        self.update_image_list()

    def create_gui(self):
        """Create the GUI layout."""
        tk.Label(
            self.root, text="Astro Wallpaper Manager", font=("Arial", 16), pady=10
        ).pack()

        # Dropdown for styles
        tk.Label(self.root, text="Choose a wallpaper style:", font=("Arial", 12)).pack(pady=5)
        style_dropdown = ttk.Combobox(
            self.root, textvariable=self.selected_style, state="readonly",
            values=["Stretch", "Center", "Tile", "Fit", "Fill"]
        )
        style_dropdown.pack(pady=5)

        # Image Listbox
        tk.Label(self.root, text="Available Images:", font=("Arial", 12)).pack(pady=5)
        self.image_listbox = tk.Listbox(self.root, height=10, width=60)
        self.image_listbox.pack(pady=5)

        # Buttons
        tk.Button(
            self.root, text="Set Selected Wallpaper", command=self.set_wallpaper, padx=20, pady=5
        ).pack(pady=5)

        tk.Button(
            self.root, text="Fetch and Download Images", command=self.fetch_and_download_images, padx=20, pady=5
        ).pack(pady=5)

        tk.Button(
            self.root, text="Start Animation", command=self.start_animation, padx=20, pady=5
        ).pack(pady=5)

        tk.Button(
            self.root, text="Stop Animation", command=self.stop_animation, padx=20, pady=5
        ).pack(pady=5)

        tk.Button(self.root, text="Exit", command=self.root.quit, padx=20, pady=10).pack()

    def update_image_list(self):
        """Update the listbox with available images."""
        self.image_listbox.delete(0, tk.END)
        self.image_paths = get_existing_images()
        for img in self.image_paths:
            self.image_listbox.insert(tk.END, os.path.basename(img))

    def fetch_and_download_images(self):
        """Fetch and download Astro images."""
        image_urls = fetch_image_urls()
        if image_urls:
            downloaded = download_images(image_urls)
            if downloaded:
                messagebox.showinfo("Download Complete", f"{len(downloaded)} new images downloaded.")
            else:
                messagebox.showinfo("No New Images", "All images are already downloaded.")
            self.update_image_list()

    def set_wallpaper(self):
        """Set the selected image as the wallpaper."""
        selected_index = self.image_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("No Selection", "Please select an image from the list.")
            return
        selected_image = self.image_paths[selected_index[0]]
        if change_wallpaper(selected_image, self.selected_style.get()):
            messagebox.showinfo("Success", "Wallpaper changed successfully!")

    def start_animation(self):
        """Start the animated wallpaper."""
        if not self.image_paths:
            messagebox.showinfo("No Images", "No images available to animate.")
            return

        if self.animating:
            messagebox.showinfo("Animation Running", "Animation is already running.")
            return

        self.animating = True
        self.animation_thread = threading.Thread(target=self.animate_wallpapers)
        self.animation_thread.start()

    def stop_animation(self):
        """Stop the animated wallpaper."""
        self.animating = False
        if self.animation_thread:
            self.animation_thread.join()
            self.animation_thread = None
        messagebox.showinfo("Animation Stopped", "Wallpaper animation stopped.")

    def animate_wallpapers(self):
        """Cycle through wallpapers in a loop."""
        while self.animating:
            for image in self.image_paths:
                if not self.animating:
                    break
                change_wallpaper(image, self.selected_style.get())
                time.sleep(ANIMATION_INTERVAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = WallpaperApp(root)
    root.mainloop()
