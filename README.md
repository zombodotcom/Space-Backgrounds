# 🌌 Astro Wallpaper Manager 🚀

Turn your desktop into a **real-time celestial masterpiece** with the Astro Wallpaper Manager! ✨ Fetch high-quality satellite images, customize your wallpaper style, and even animate your desktop background for a dynamic, out-of-this-world experience. 🌠

---

## 🌟 Features

- **Fetch Stunning Satellite Images** 🌍  
  Automatically download the latest GeoColor images from the NOAA GOES satellite.

- **Customizable Wallpaper Styles** 🎨  
  Choose from:
  - `Stretch`
  - `Center`
  - `Tile`
  - `Fit`
  - `Fill`

- **Dynamic Animation** 🎥  
  Animate your desktop background with seamless transitions between images. Adjust the speed to your liking, from as fast as `0.01` seconds to a leisurely `30` seconds.

- **Efficient Design** ⚡  
  - Skips downloading images you already have.  
  - Uses the lightweight and responsive `tkinter` GUI.  
  - No resource-hungry processes—everything runs smoothly!

---

## 🛠️ How to Use

1. **Clone the Repository**  
```
   git clone https://github.com/yourusername/astro-wallpaper-manager.git
   cd astro-wallpaper-manager

    Install Dependencies
    Install the required Python libraries:
```

```
pip install requests beautifulsoup4
```

Run the Application
```
    python astro_wallpaper_manager.py
```
    Enjoy the Universe! 🌌
        Fetch and download the latest satellite images.
        Select a wallpaper style.
        Animate your desktop background with celestial beauty.

## 📋 Controls
- Fetch and Download Images 🌐
Fetch the latest GeoColor images and save them locally.

- Set Selected Wallpaper 🖼️
Choose an image from the list and set it as your desktop background.

- Start/Stop Animation 🎬
Animate your background with a custom speed.

- Adjust Animation Speed ⏱️
Use the slider or enter a precise value to control the animation interval.

## 📂 File Structure
```
astro-wallpaper-manager/
│
├── satellite_images/      # Downloaded satellite images
│   └── GeoColor/1808x1808 # Default resolution folder
│
├── astro_wallpaper_manager.py  # Main Python script
└── README.md             # This file
```


## ⚙️ Tech Stack
- Python 🐍
    - ctypes for Windows API integration.
    - tkinter for a lightweight GUI.
    - requests and BeautifulSoup4 for fetching satellite data.

## 📦 Future Features

- 🌈 Support for More Image Formats
 Add support for additional resolutions and formats.

- 🕶️ Dark Mode
A dark theme for night owls. 🦉

- 🌌 More Satellite Feeds
Explore other bands and satellite sources.

## 💖 Contributions

Want to make this better? Contributions are always welcome!
Fork the repo, create a pull request, and let's make it stellar. 🌟

## 🌍 Credits

    Satellite images from the NOAA GOES Viewer.
    Built with ❤️ by space enthusiasts.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

Have fun exploring the universe from your desktop! 🌌✨