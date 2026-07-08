from systems.game_panel import GamePanel

def main():
    # HYPERPARAMS
    WIDTH = 1280
    HEIGHT = 720
    CAPTION = "SOME RANDOM GAME BY PATRICK"

    print("[LAUNCHER] Launching engine...")
    game = GamePanel(WIDTH, HEIGHT, CAPTION)
    game.start()
    print("[LAUNCHER] Engine shutdown complete.")

if __name__ == "__main__":
    main()