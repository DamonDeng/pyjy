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
import pygame_gui
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
    DARK_GRAY = (30, 29, 32)

    original_surface = pygame.Surface((GameConfig.SUB_SCENE_WIDTH, GameConfig.SUB_SCENE_HEIGHT))
    # scale_surface = pygame.transform.scale(original_surface, (SCALE_WIDTH, SCALE_HEIGHT))
    WINDOW_SIZE = (1600, 960)


    # Set up display
    main_screen = pygame.display.set_mode((1600, 960))

    image = pygame.image.load("./resource/ui/main_ui_bg.png")

    main_screen.blit(image, (0, 0))

    pygame.display.set_caption(GameConfig.SCREEN_TITLE)


    manager = pygame_gui.UIManager((WINDOW_SIZE))

    display_html_text = """
    <font color='#FF0000' face='arial'>This is a <b>wrapped</b> text box</font> and somthing out of the font tag

    very very long text , something like this is a very long text that will be wrapped in the text box

    <font color='#00FF00'>This is a <i>wrapped</i> text box</font>

    <font color='#0000FF'>This is a <u>wrapped</u> text box</font>
    
    看看中文行不行

    <font color='#FF0000' face='arial'>This is a <b>wrapped</b> text box</font> and somthing out of the font tag

    very very long text , something like this is a very long text that will be wrapped in the text box

    <font color='#00FF00'>This is a <i>wrapped</i> text box</font>

    <font color='#0000FF'>This is a <u>wrapped</u> text box</font>

    <font color='#FF0000' face='arial'>This is a <b>wrapped</b> text box</font> and somthing out of the font tag

    very very long text , something like this is a very long text that will be wrapped in the text box

    <font color='#00FF00'>This is a <i>wrapped</i> text box</font>

    <font color='#0000FF'>This is a <u>wrapped</u> text box</font>

    <font color='#FF0000' face='arial'>This is a <b>wrapped</b> text box</font> and somthing out of the font tag

    very very long text , something like this is a very long text that will be wrapped in the text box

    <font color='#00FF00'>This is a <i>wrapped</i> text box</font>

    <font color='#0000FF'>This is a <u>wrapped</u> text box</font>

    <font color='#FF0000' face='arial'>This is a <b>wrapped</b> text box</font> and somthing out of the font tag

    very very long text , something like this is a very long text that will be wrapped in the text box

    <font color='#00FF00'>This is a <i>wrapped</i> text box</font>

    <font color='#0000FF'>This is a <u>wrapped</u> text box</font>

    <font color='#FF0000' face='arial'>This is a <b>wrapped</b> text box</font> and somthing out of the font tag

    very very long text , something like this is a very long text that will be wrapped in the text box

    <font color='#00FF00'>This is a <i>wrapped</i> text box</font>

    <font color='#0000FF'>This is a <u>wrapped</u> text box</font>


    """

    # Create a UITextBox with HTML-like theming
    text_box = pygame_gui.elements.UITextBox(
        html_text=display_html_text,
        relative_rect=pygame.Rect((1151, 71), (441, 600)),
        manager=manager,
        object_id="#text_box"
    )



    screen = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))



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
        time_delta = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_x:
                    # switch to the next scene
                    current_scene_id = sub_scene_map_data.scene_id
                    current_scene_id = current_scene_id + 1
                    if current_scene_id >= GameConfig.SUB_SCENE_NUMBER:
                        current_scene_id = 0
                    sub_scene_map_data.switch_scene_data_by_id(current_scene_id)
                    x = sub_scene_map_data.scene_map_info["EntranceX"]
                    y = sub_scene_map_data.scene_map_info["EntranceY"]
                    main_character.set_location(x, y)
                    camera.follow_character(main_character)
                    
                    music_id = sub_scene_map_data.scene_map_info["EntranceMusic"]
                    
                    if music_id > 0 and music_id < 24:
                    
                        music_file_path = "../original_resource/music/" + str(music_id) + ".mid"
                        
                        pygame.mixer.music.load(music_file_path)

                        # Play the music in an infinite loop
                        pygame.mixer.music.play(-1)
                    
                elif event.key == pygame.K_z:
                    # switch to the previous scene
                    current_scene_id = sub_scene_map_data.scene_id
                    current_scene_id = current_scene_id - 1
                    if current_scene_id < 0:
                        current_scene_id = GameConfig.SUB_SCENE_NUMBER - 1
                    sub_scene_map_data.switch_scene_data_by_id(current_scene_id)
                    x = sub_scene_map_data.scene_map_info["EntranceX"]
                    y = sub_scene_map_data.scene_map_info["EntranceY"]
                    main_character.set_location(x, y)
                    camera.follow_character(main_character)
                    
                    music_id = sub_scene_map_data.scene_map_info["EntranceMusic"]
                    
                    if music_id > 0 and music_id < 24:
                    
                        music_file_path = "../original_resource/music/" + str(music_id) + ".mid"
                        
                        pygame.mixer.music.load(music_file_path)

                        # Play the music in an infinite loop
                        pygame.mixer.music.play(-1)
                
            manager.process_events(event)
                
                    
                # Move the camera based on key presses
        main_character.tick()
        camera.follow_character(main_character, scene_controller.current_scene_type)
        scene_controller.detect_to_switch()
            
        original_surface.fill(WHITE)
        draw_the_screen(original_surface)

        
        scale_surface = pygame.transform.scale(original_surface, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        
        screen.blit(scale_surface, (0, 0))
        
        main_screen.fill(DARK_GRAY)
        
        main_screen.blit(screen, (481, 165))
        

        
        manager.update(time_delta)
        
        manager.draw_ui(main_screen)
        
        main_screen.blit(image, (0, 0))
        

        
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
