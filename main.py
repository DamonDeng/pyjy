import boto3
import struct

from pyjy.utils import BinaryReader
from pyjy.texture import TextureManager
from pyjy.constants import GameConfig
from pyjy.constants import SceneType
from pyjy.constants import Direction
from pyjy.sub_scene import SubSceneMapData
from pyjy.sub_scene import SubSceneDrawer
from pyjy.main_scene import MainSceneMapData
from pyjy.main_scene import MainSceneDrawer
from pyjy.character import MainCharacter
from pyjy.camera import Camera
from pyjy.data_loader import RangerLoader
from pyjy.scene_controller import SceneController
from pyjy.music_player import MusicPlayer


import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

import pygame
import math

def main():
    texture_manager = TextureManager("./")

    ranger_loader = RangerLoader()
    ranger_loader.load("./original_resource/save/ranger.idx32", \
        "./original_resource/save/ranger.grp32")

    main_scene_map_data = MainSceneMapData(texture_manager)
    main_scene_map_data.load_data("./original_resource/resource/")

    sub_scene_map_data = SubSceneMapData(ranger_loader.submaps)
    sub_scene_map_data.load_data(sin_file_name="./original_resource/save/allsin.grp",
                            def_file_name="./original_resource/save/alldef.grp")
    sub_scene_map_data.switch_scene_data_by_id(1)
    x = sub_scene_map_data.scene_map_info["MainEntranceX1"]
    y = sub_scene_map_data.scene_map_info["MainEntranceY1"]
    
    y = y + 1
    
    main_character = MainCharacter(x, y, \
                    texture_manager, \
                    main_scene_map_data, \
                    sub_scene_map_data)
    camera = Camera()
    main_scene_drawer = MainSceneDrawer(main_character, main_scene_map_data, texture_manager, camera)
    sub_scene_drawer = SubSceneDrawer(main_character, sub_scene_map_data, texture_manager, camera)
    music_player = MusicPlayer("./")
    scene_controller = SceneController(ranger_loader.submaps, main_scene_drawer, sub_scene_drawer, music_player)
        
    # Initialize Pygame
    pygame.init()

    music_player.play_mid_by_id(1)

    # Colors
    WHITE = (255, 255, 255)

    original_surface = pygame.Surface((GameConfig.SUB_SCENE_WIDTH, GameConfig.SUB_SCENE_HEIGHT))
    # scale_surface = pygame.transform.scale(original_surface, (SCALE_WIDTH, SCALE_HEIGHT))

    # Set up display
    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))

    pygame.display.set_caption(GameConfig.SCREEN_TITLE)

    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Draw the screen
    def draw_the_screen(screen):
        scene_controller.draw(screen)
        

    # Main game loop
    # frame_count = 0
    running = True
    prev_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                
                    
                # Move the camera based on key presses
        main_character.tick()
        camera.follow_character(main_character, scene_controller.current_scene_type)
        scene_controller.detect_to_switch()
            
        original_surface.fill(WHITE)
        draw_the_screen(original_surface)

        
        scale_surface = pygame.transform.scale(original_surface, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        
        screen.blit(scale_surface, (0, 0))
        
        pygame.display.flip()
        
        clock.tick(GameConfig.FPS)
        
        # frame_count = frame_count + 1
        # if (frame_count > 10000):
        #     frame_count = frame_count - 10000
            
        # print the time delta of the frame
        
        current_time = pygame.time.get_ticks()

        # Calculate the time delta
        time_delta = current_time - prev_time

        # Print the time delta
        # print(f"Time delta: {time_delta} ms")

        # Update the previous time
        prev_time = current_time
        
        # update camera location
        # camera.follow_character(main_character)
        
        # camera_x, camera_y = get_camera_location(main_character)

    pygame.quit()
    # sys.exit()



    
# starting the game by calling main function:
    
if __name__ == "__main__":
    main()
