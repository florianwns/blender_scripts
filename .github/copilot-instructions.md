# Copilot instructions for Blender Scripts

This repository contains small Blender automation scripts under `src/` intended to be run with Blender's bundled Python. These instructions describe project-specific conventions and the fastest ways an AI coding agent can be productive.

- **Project layout:** scripts live in `src/`, single-file scripts (e.g. `src/001_add_cube.py`). Packaging metadata is in `pyproject.toml`.
- **Python runtime:** Target Python >= 3.11 (see `pyproject.toml`). Scripts are executed with Blender's Python binary at `/Applications/Blender.app/Contents/MacOS/blender` on macOS.
- **Run scripts:** Use Blender's CLI to run a script. Example:

  /Applications/Blender.app/Contents/MacOS/blender --python src/001_add_cube.py

- **Local testing without Blender UI:** The project depends on `fake-bpy-module-latest` to allow running or linting code outside Blender. Use the virtualenv in this repo `.venv` (see README) and install dependencies from `pyproject.toml`.

- **Conventions and patterns:**
  - Keep scripts small and focused; each file performs a single automation task (e.g. `ensure_cube()` in `001_add_cube.py`).
  - Use `bpy` API directly; functions often return `bpy.types.Object` and raise `RuntimeError` on critical failure.
  - Logging is done with `print()`; do not add heavy logging frameworks.

- **What an AI agent should do first:**
  1. Open `README.md`, `pyproject.toml`, and the target `src/` script to understand execution and dependencies.
  2. If editing scripts, prefer minimal, focused changes and preserve simple CLI/run behavior.
  3. When adding tests or running code locally, rely on `fake-bpy-module-latest` and the repo virtualenv.

- **Editing guidance and examples:**
  - To add a new tool script follow the numeric prefix pattern `src/00X_description.py`.
  - For modifying `src/001_add_cube.py`, keep `ensure_cube(name, location)` signature stable; callers may rely on it.
  - Example: prefer raising `RuntimeError("Failed to create cube object")` rather than returning `None` when Blender operations fail.

- **Build / test / debug commands:**
  - Create and activate venv (README):

    uv venv .venv --python "$(find /Applications/Blender.app -type f -path '*python/bin/python*' -maxdepth 6 | head -n 1)"
    source .venv/bin/activate

  - Run a script in Blender (macOS example):

    /Applications/Blender.app/Contents/MacOS/blender --python src/001_add_cube.py

  - Run linting / static checks inside venv (install tools as needed).

- **Files to inspect for context:** `README.md`, `pyproject.toml`, and `src/001_add_cube.py`.

- **What not to change without asking:**
  - Do not assume another OS or Blender path; the repo assumes macOS `/Applications/Blender.app` unless the user updates README.
  - Avoid adding heavy runtime dependencies; keep scripts runnable inside Blender's bundled Python.

If anything here is unclear or you'd like the agent to follow additional style rules (naming, test style), tell me and I'll update this file.
