import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_CENTERED"] = "1"

from src.game import Game


if __name__ == "__main__":
    game = Game()
    game.run()
