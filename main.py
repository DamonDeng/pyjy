import boto3
import struct

from pyjy.utils.binary_reader import BinaryReader
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

from pyjy.npcs.xiaoer import Xiaoer


import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

import pygame 
import pygame_gui
import math

class MessageResponder:
    
    def __init__(self, display_text_box):
        
        self.display_text_box = display_text_box
        
    def message_from_npc(self, text_str):
        
        html_format_text = "<font color='#00FF00'> 店小二说: \n" + text_str + "</font>"
        
        self.display_text_box.append_html_text(html_format_text + "\n")

        self.display_text_box.update_text_end_position(1000)
        

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
    WINDOW_SIZE = (1400, 800)



    # Set up display
    main_screen = pygame.display.set_mode(WINDOW_SIZE)

    image = pygame.image.load("./resource/ui/main_ui_bg.png")

    main_screen.blit(image, (0, 0))

    pygame.display.set_caption(GameConfig.SCREEN_TITLE)


    manager = pygame_gui.UIManager((WINDOW_SIZE), starting_language='zh')



    display_html_text = ""

    # Create a UITextBox with HTML-like theming
    text_box = pygame_gui.elements.UITextBox(
        html_text=display_html_text,
        relative_rect=pygame.Rect((1033, 74), (359, 707)),
        manager=manager,
        object_id="#text_box"
    )


    # Create a multi-line UITextEntryBox
    text_entry = pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((380, 577), (640, 180)),
        manager=manager,
        object_id="#text_entry",
        container=manager.get_root_container()
    )

    message_responder = MessageResponder(text_box)

    xiaoer = Xiaoer(message_responder)



    screen = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))



    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Draw the screen
    def draw_the_screen(screen):
        scene_controller.draw(screen)
        
    is_editing = False

    # Main game loop
    # frame_count = 0
    running = True
    prev_time = pygame.time.get_ticks()
    while running:
        time_delta = clock.tick(60) / 1000.0
        
        detected_send_action = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                
                if is_editing == True:
                    if event.key == pygame.K_RETURN:
                        # Check if the Shift key is also pressed
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
                        if shift_pressed:
                            # print("Shift+Enter detected!")
                            
                            detected_send_action = True
                            
                            input_text = text_entry.get_text()
                            
                            html_format_text = "<font color='#FFFFFF'> 你说:\n" + input_text + "</font>"
                            
                            text_box.append_html_text(html_format_text + "\n")
                            
                            text_box.update_text_end_position(1000)
                            
                            text_entry.set_text("")
                            
                            xiaoer.at_msg_receive(input_text)
                            
                elif is_editing == False:
                
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is over the entry textbox
                if text_entry.rect.collidepoint(event.pos):
                    # Stop responding to key down events for the main character
                    is_editing = True
                else:
                    # Allow the main character to respond to key down events
                    is_editing = False
                    
            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object == text_entry:
                # Handle text entry submission
                text = event.text
                # send_text(text)
                # Clear the text entry box
                text_entry.set_text("")
                
            if not detected_send_action:
                manager.process_events(event)
            
        if is_editing == True:
            input_rect = pygame.Rect((380, 577), (640+100, 180-5))
            pygame.key.set_text_input_rect(input_rect)
                
        elif is_editing == False:
                        
            # Move the camera based on key presses
            main_character.tick()
            camera.follow_character(main_character, scene_controller.current_scene_type)
            scene_controller.detect_to_switch()
                
            original_surface.fill(WHITE)
            draw_the_screen(original_surface)

        
        scale_surface = pygame.transform.scale(original_surface, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        
        screen.blit(scale_surface, (0, 0))
        
        main_screen.fill(DARK_GRAY)
        
        main_screen.blit(screen, (381, 84))
        

        
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
