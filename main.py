import boto3
import struct

from pyjy.utils import BinaryReader
from pyjy.texture import TextureManager, MainCharacterTextureManager
from pyjy.constants import GameConfig
from pyjy.sub_scene import SceneMapData
from pyjy.sub_scene import SubSceneDrawer
from pyjy.character import MainCharacter
from pyjy.camera import Camera

import pygame

def main():


    scene_texture_manager = TextureManager()
    # scene_texture_manager.load_from_folder('../original_resource/resource/smap/')
    scene_texture_manager.load_from_zip_file('./original_resource/resource/smap.zip')

    main_character_texture_manager = MainCharacterTextureManager(scene_texture_manager)
    # main_character_texture_manager.load('../original_resource/resource/chara/')
    # 

    current_scene_map_data = SceneMapData()
    current_scene_map_data.load_data(sin_file_name="./original_resource/save/allsin.grp",
                            def_file_name="./original_resource/save/alldef.grp")

    current_scene_map_data.switch_scene_data_by_id(1)
    
    main_character = MainCharacter(32, 32, main_character_texture_manager)
    
    camera = Camera()

    camera.follow_character(main_character)

    subscene_drawer = SubSceneDrawer(main_character, current_scene_map_data, scene_texture_manager, camera)


    # Initialize Pygame
    pygame.init()
    
    # Background color
    WHITE = (255, 255, 255)

    original_surface = pygame.Surface((GameConfig.SUB_SCENE_WIDTH, GameConfig.SUB_SCENE_HEIGHT))
    
    # Set up display
    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))

    pygame.display.set_caption(GameConfig.SCREEN_TITLE)

    # Clock to control frame rate
    clock = pygame.time.Clock()

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
        camera.follow_character(main_character)
            
                    
        # WHITE = (255, 255, 255)
        original_surface.fill(WHITE)
        
        subscene_drawer.draw(original_surface)
        
        # draw_the_screen(original_surface)
        # draw_character()
        
        scale_surface = pygame.transform.scale(original_surface, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        
        screen.blit(scale_surface, (0, 0))
        
        pygame.display.flip()
        
        clock.tick(GameConfig.FPS)
        
        
        current_time = pygame.time.get_ticks()

        time_delta = current_time - prev_time

        prev_time = current_time
        
    pygame.quit()
    # sys.exit()
    
    # starting the game by calling main function:
    
if __name__ == "__main__":
    main()
