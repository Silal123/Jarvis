import win32api
import win32con
import win32gui
import win32ui
import os
from PIL import Image

def extract_icon(exe_path):
    try:
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

        large, small = win32gui.ExtractIconEx(exe_path,0)
        win32gui.DestroyIcon(small[0])

        hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_x )
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject( hbmp )
        hdc.DrawIcon( (0,0), large[0] )

        bmpstr = hbmp.GetBitmapBits(True)

        icon = Image.frombuffer(
            'RGBA',
            (32,32),
            bmpstr, 'raw', 'BGRA', 0, 1
        )

        if not os.path.exists("icons/apps"): os.makedirs("icons/apps")
        full_outpath = os.path.join("icons/apps", "{}.ico".format(get_exe_name(exe_path)))
        icon.resize((100, 100))
        icon.save(full_outpath)
    except:
        if not os.path.exists("icons/apps"): os.makedirs("icons/apps")
        full_outpath = os.path.join("icons/apps", "{}.ico".format(get_exe_name(exe_path)))
        img = Image.open("icons/icon2.ico")
        img.save(full_outpath)
        return

def get_exe_name(file_path):
    return os.path.basename(file_path)