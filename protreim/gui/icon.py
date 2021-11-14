
from pathlib import Path
import base64

with (Path(__file__).parent / 'icon.png').open('rb') as f:
    MAINICON = base64.b64encode(f.read())