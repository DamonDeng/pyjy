import pygame

from enum import Enum

from pyjy.texture import TextureManager
from pyjy.main_scene import MainSceneMapData, MainSceneDrawer
from pyjy.sub_scene import SubSceneMapData, SubSceneDrawer
from pyjy.data_loader import RangerLoader
from pyjy.character import MainCharacter
from pyjy.camera import Camera
from pyjy.music_player import MusicPlayer
from pyjy.scene_controller import SceneController
from pyjy.constants import GameConfig, GameStatus
from pyjy.ui_controller import UIController



    

class CentralController:
    
    def __init__(self, root_folder):
        
        self.root_folder = root_folder
        
        
        self.texture_manager = texture_manager = TextureManager(root_folder)
        
        self.ranger_loader = RangerLoader()
        self.ranger_loader.load(self.root_folder + "/original_resource/save/ranger.idx32", \
            self.root_folder + "/original_resource/save/ranger.grp32")

        self.main_scene_map_data = MainSceneMapData(texture_manager)
        self.main_scene_map_data.load_data(self.root_folder + "/original_resource/resource/")

        self.sub_scene_map_data = SubSceneMapData(self.ranger_loader.submaps)
        self.sub_scene_map_data.load_data(sin_file_name=self.root_folder + "/original_resource/save/allsin.grp",
                                def_file_name=self.root_folder + "/original_resource/save/alldef.grp")
        
        self.sub_scene_map_data.switch_scene_data_by_id(1)

        x = self.sub_scene_map_data.scene_map_info["MainEntranceX1"]
        y = self.sub_scene_map_data.scene_map_info["MainEntranceY1"]

        self.main_character = MainCharacter(x, y, \
                        texture_manager, \
                        self.main_scene_map_data, \
                        self.sub_scene_map_data)


        self.camera = Camera()
        
        
        self.main_scene_drawer = MainSceneDrawer(self.main_character, self.main_scene_map_data, texture_manager, self.camera)
        self.sub_scene_drawer = SubSceneDrawer(self.main_character, self.sub_scene_map_data, texture_manager, self.camera)

        self.music_player = MusicPlayer(root_folder)
        
        self.scene_controller = SceneController(self.ranger_loader.submaps, self.main_scene_drawer, self.sub_scene_drawer, self.music_player)
        
        self.ui_controller = UIController(root_folder, self)
        
        self.game_status = GameStatus.INGAME
        
        self.npcs = []
        
        
        
        

    def set_texture_manager(self, texture_manager):
        self.texture_manager = texture_manager
        
    def set_main_character(self, main_character):
        self.main_character = main_character
        
    def set_ui_controller(self, ui_controller):
        self.ui_controller = ui_controller
        
    def set_scene_controller(self, scene_controller):
        self.scene_controller = scene_controller
        
    
        
    def add_npc(self, npc):
        self.npcs.append(npc)
        
    def process_events(self):
        detected_send_action = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                
                if self.game_status == GameStatus.TALKING:
                    if event.key == pygame.K_RETURN:
                        # Check if the Shift key is also pressed
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
                        if shift_pressed:
                            # print("Shift+Enter detected!")
                            
                            detected_send_action = True
                            
                            # input_text = text_entry.get_text()
                            
                            # html_format_text = "<font color='#FFFFFF'> 你说:\n" + input_text + "</font>"
                            
                            # text_box.append_html_text(html_format_text + "\n")
                            
                            # text_box.update_text_end_position(1000)
                            
                            # text_entry.set_text("")
                            
                            # xiaoer.at_msg_receive(input_text)
                            
                elif self.game_status == GameStatus.INGAME:
                
                    if event.key == pygame.K_ESCAPE:
                        return False
                    
                
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is over the entry textbox
                # if text_entry.rect.collidepoint(event.pos):
                #     # Stop responding to key down events for the main character
                #     is_editing = True
                # else:
                #     # Allow the main character to respond to key down events
                #     is_editing = False
                pass
                    
            # elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object == text_entry:
            #     # Handle text entry submission
            #     text = event.text
            #     # send_text(text)
            #     # Clear the text entry box
            #     text_entry.set_text("")
                
            # if not detected_send_action:
            #     manager.process_events(event)
            
        # if is_editing == True:
        #     input_rect = pygame.Rect((380, 577), (640+100, 180-5))
        #     pygame.key.set_text_input_rect(input_rect)
                
        # elif is_editing == False:
                        
            # Move the camera based on key presses
        self.main_character.tick()
        self.camera.follow_character(self.main_character, self.scene_controller.current_scene_type)
        self.scene_controller.detect_to_switch()
        return True
        
    def update(self, time_delta):
        for npc in self.npcs:
            npc.update(time_delta)
            
        self.main_character.update(time_delta)
        
        self.camera.follow_character(self.main_character, self.scene_controller.current_scene_type)
        
    def draw(self, time_delta):
        self.ui_controller.draw(time_delta)