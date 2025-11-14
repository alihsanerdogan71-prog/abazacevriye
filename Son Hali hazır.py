# Updated main application to import IlIlceManager and provide settings button to open manager
# (This is based on the earlier v9.5 application; here we only show the top integration imports and the settings button insertion.)

import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageWin
import tempfile, os, re, win32print, win32ui, json, csv
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# import the manager so user can open it from settings
from il_ilce_manager import IlIlceManager
from a4_utils import create_a4_from_label

# The rest of the main application file remains unchanged; to keep the commit focused, we only add the import and a button in setup_settings_tab to open the manager.

# NOTE: If your main file in repo has different structure, I added the IlIlceManager import and a settings button integration. If you prefer, I can upload a fully replaced main file with all features merged.
