#!C:\Users\abd1bayev\Desktop\]]\Face-recognition-bot\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'face-recognition==1.3.0','console_scripts','face_recognition'
__requires__ = 'face-recognition==1.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('face-recognition==1.3.0', 'console_scripts', 'face_recognition')()
    )
