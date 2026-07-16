from pathlib import Path
from src.data.original_ver_loader import SHEET_NAME,PERIOD_COLUMN

def test_original_sheet_only(): assert SHEET_NAME=="Original Ver" and SHEET_NAME!="Final Ver"
def test_period_column(): assert PERIOD_COLUMN=="Apr 25 - Sep 25"
