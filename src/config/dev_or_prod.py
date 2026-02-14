import sys

def is_development() -> bool:
    return not getattr(sys, 'frozen', False)