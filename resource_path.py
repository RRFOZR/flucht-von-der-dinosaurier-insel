"""
Resource path helper for PyInstaller compatibility.

When running as a PyInstaller bundle, files are extracted to a temporary
directory. This module provides functions to correctly locate resource files
whether running from source or as a bundled application.
"""

import sys
import os

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    When running as a PyInstaller bundle, resources are extracted to
    sys._MEIPASS. When running from source, they're in the current directory.

    Args:
        relative_path: Path relative to the app root (e.g., 'konrad_insel/sounds/...')

    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running from source - use current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_base_path():
    """
    Get the base path of the application.

    Returns:
        Base path (sys._MEIPASS for bundled apps, current directory for source)
    """
    try:
        return sys._MEIPASS
    except AttributeError:
        return os.path.abspath(".")


def resource_exists(relative_path):
    """
    Check if a resource file exists.

    Args:
        relative_path: Path relative to app root

    Returns:
        True if file exists
    """
    return os.path.exists(get_resource_path(relative_path))
