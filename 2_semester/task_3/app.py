import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.Common.PageManager import PageManager

if "__main__" == __name__:
    PageManager().render()