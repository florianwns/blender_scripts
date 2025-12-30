# blender_scripts
Blender Scripts


## A small collection of Blender automation scripts

This repository contains simple Python scripts to automate common Blender tasks.

### Setup
Create and activate a virtual environment pointing to Blender's Python:

```bash
uv venv .venv --python "$(find /Applications/Blender.app -type f -path '*python/bin/python*' -maxdepth 6 | head -n 1)"
source .venv/bin/activate
```

### VS Code Configuration
For a quick VS Code setup related to Blender development, see this video:

https://www.youtube.com/watch?v=_0srGXAzBZE

You can add a `.vscode` folder in the project to store workspace-specific settings, tasks, and notes.

### Usage
Run a script directly with Blender:

```bash
/Applications/Blender.app/Contents/MacOS/blender --python src/001_add_cube.py
```

### Notes
- Scripts assume Blender is installed in `/Applications/Blender.app` on macOS.
- Keep scripts small and focused for easier testing inside Blender.


### Addons

Addons are installed using a symbolic link to `/Users/florian/Library/Application Support/Blender/5.0/extensions/vscode_development`