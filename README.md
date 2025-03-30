## Inventory Tracker

This project is a small desktop app designed for tracking movement of store inventory between multiple locations.
It uses an unregistered UPCA barcode system (EAN compatible), and expects that the files it generates will be synced between locations using
a cloud storage solution (Google Drive, OneDrive etc.). The .exe file should be placed in a cloud folder and run from
that folder (creating a shortcut to place elsewhere is fine).

Some assumptions are made regarding the use of this app, and must be followed to prevent sync conflicts:
- Only one computer *per location* should use this app to log tracking changes to that location in a short span of time
(this is because tracking logs are split into one file per location)
- Only one computer *total* should use this app to generate new barcodes in a short span of time (since item barcodes are stored in a single file)
