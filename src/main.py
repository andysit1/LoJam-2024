import pygame


from state import DisplayEngine
from states.game import GameState

import os
import sys
# Setup the environment by appending the current directory to the system path.
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

import asyncio
import time

WIDTH, HEIGHT = 1280, 720


async def main():
    running = True
    pygame.init()

    engine = DisplayEngine('A Shy Worm', 60, WIDTH, HEIGHT)
    engine.machine.current = GameState(engine)

    previous_time = time.time()
    while running:

        dt = time.time() - previous_time
        previous_time = time.time()

        engine.machine.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.machine.current.on_event(event)

        engine.machine.current.on_update(dt)
        engine.machine.current.on_draw(engine.surface)

        pygame.display.flip()
        await asyncio.sleep(0)



asyncio.run(main())