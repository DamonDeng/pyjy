import boto3
import struct

from pyjy.utils import BinaryReader
from pyjy.texture import TextureManager, MainCharacterTextureManager
from pyjy.constants import GameConfig
from pyjy.sub_scene import SceneMapData
from pyjy.sub_scene import SubSceneDrawer
from pyjy.character import MainCharacter
from pyjy.camera import Camera
from pyjy.data_loader import RangerLoader

import pygame

def main():

    ranger_loader = RangerLoader()
    ranger_loader.load("./original_resource/save/ranger.idx32", \
                        "./original_resource/save/ranger.grp32")

    scene_texture_manager = TextureManager()
    # scene_texture_manager.load_from_folder('../original_resource/resource/smap/')
    scene_texture_manager.load_from_zip_file('./original_resource/resource/smap.zip')

    main_character_texture_manager = MainCharacterTextureManager(scene_texture_manager)
    # main_character_texture_manager.load('../original_resource/resource/chara/')
    # 

    current_scene_map_data = SceneMapData(ranger_loader.submaps)
    current_scene_map_data.load_data(sin_file_name="./original_resource/save/allsin.grp",
                            def_file_name="./original_resource/save/alldef.grp")

    current_scene_map_data.switch_scene_data_by_id(1)
    
    main_character = MainCharacter(32, 32, \
                main_character_texture_manager, \
                current_scene_map_data, \
                current_scene_map_data)

    main_character.set_scene_status(MainCharacter.InSub)
    x = current_scene_map_data.scene_map_info["EntranceX"]
    y = current_scene_map_data.scene_map_info["EntranceY"]
    main_character.set_location(x, y)
    
    camera = Camera()

    camera.follow_character(main_character)

    subscene_drawer = SubSceneDrawer(main_character, current_scene_map_data, scene_texture_manager, camera)


    # Initialize Pygame
    pygame.init()
    
    pygame.mixer.init()

    # Load the MIDI music file
    pygame.mixer.music.load("./original_resource/music/1.mid")

    # Play the music in an infinite loop
    pygame.mixer.music.play(-1)
    
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
                    
                elif event.key == pygame.K_x:
                    # switch to the next scene
                    current_scene_id = current_scene_map_data.scene_id
                    current_scene_id = current_scene_id + 1
                    if current_scene_id >= GameConfig.SUB_SCENE_NUMBER:
                        current_scene_id = 0
                    current_scene_map_data.switch_scene_data_by_id(current_scene_id)
                    x = current_scene_map_data.scene_map_info["EntranceX"]
                    y = current_scene_map_data.scene_map_info["EntranceY"]
                    main_character.set_location(x, y)
                    camera.follow_character(main_character)
                    
                    music_id = current_scene_map_data.scene_map_info["EntranceMusic"]
                    
                    if music_id > 0 and music_id < 24:
                    
                        music_file_path = "../original_resource/music/" + str(music_id) + ".mid"
                        
                        pygame.mixer.music.load(music_file_path)

                        # Play the music in an infinite loop
                        pygame.mixer.music.play(-1)
                    
                elif event.key == pygame.K_z:
                    # switch to the previous scene
                    current_scene_id = current_scene_map_data.scene_id
                    current_scene_id = current_scene_id - 1
                    if current_scene_id < 0:
                        current_scene_id = GameConfig.SUB_SCENE_NUMBER - 1
                    current_scene_map_data.switch_scene_data_by_id(current_scene_id)
                    x = current_scene_map_data.scene_map_info["EntranceX"]
                    y = current_scene_map_data.scene_map_info["EntranceY"]
                    main_character.set_location(x, y)
                    camera.follow_character(main_character)
                    
                    music_id = current_scene_map_data.scene_map_info["EntranceMusic"]
                    
                    if music_id > 0 and music_id < 24:
                    
                        music_file_path = "../original_resource/music/" + str(music_id) + ".mid"
                        
                        pygame.mixer.music.load(music_file_path)

                        # Play the music in an infinite loop
                        pygame.mixer.music.play(-1)
                    
                
                    
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
