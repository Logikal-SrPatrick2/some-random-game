import pygame
import sys

def initialize_system():
    print("[SYSTEM] Initializing Pygame framework layers...")
    pygame.init()

def terminate_system():
    print("[SYSTEM] Terminating Pygame framework layers...")
    pygame.quit()

def kill_program():
    print("[SYSTEM] KILL PROGRAM")
    pygame.quit()
    sys.exit()