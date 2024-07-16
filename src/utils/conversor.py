# src\utils\conversor.py
# conversor de coordenadas pymunk -> pygame

from utils import values

def pymunk_to_pygame(p):
    return int(p.x), int(values.HEIGHT - p.y)