from datetime import datetime
import pytz

BG = '#F9F5F6'  # Background
FG = '#333333'  # Foreground
PRIM = '#FFFFFF'  # Primary
SCD = '#606060'  # Secondary
ACT = '#8CC0DE'  # Accent

MOBILE_HEIGHT = 728
MOBILE_WIDTH = 430

APP_FONTS = {
    'QS Light': './fonts/Quicksand-Light.ttf',
    'QS Regular': './fonts/Quicksand-Regular.ttf',
    'QS Medium': './fonts/Quicksand-Medium.ttf',
    'QS SemiBold': './fonts/Quicksand-SemiBold.ttf',
    'QS Bold': './fonts/Quicksand-Bold.ttf',
}

ph_time_zone = pytz.timezone('Asia/Manila')

current_time = datetime.now(ph_time_zone).strftime('%I:%M %p')
current_date = datetime.now(ph_time_zone).strftime('%B %d, %Y')
