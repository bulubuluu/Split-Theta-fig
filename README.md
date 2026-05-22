Usage:

```bash
python3 generate_gallery.py /path/to/your/folder --title "My Figures" --output /path/to/your/folder/index.html
```

What it does:

- recursively scans subfolders
- finds image files like `png`, `jpg`, `jpeg`, `gif`, `webp`, `svg`
- groups them by subfolder
- writes a shareable static `index.html`

To share:

- if the folder is on a web server, send the `index.html` URL
- if it is local only, open the HTML in a browser first to check layout
