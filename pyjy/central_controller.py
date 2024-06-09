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
from pyjy.constants import SceneType
from pyjy.message import Message
from pyjy.npcs.xiaoer import Xiaoer


    

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
        
        xiaoer = Xiaoer()
        
        self.add_npc(xiaoer)
        
        self.talking_npc = None
        self.main_character_head_img = None
        
        
        
        

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
        npc.register_to_controller(self)
        
    def message_from_npc(self, message:Message):
        npc_cn_name = message.sender_cn_name
        message_text = message.text
        
        html_format_text = "<font color='#00FF00'>" + npc_cn_name + "说:\n" + message_text + "</font>"
        
        self.ui_controller.system_message_box.append_html_text(html_format_text + "\n")
        
        display_message_text = "<font color='#00FF00'>" + message_text + "</font>"
        
        self.ui_controller.upper_talk_box.set_text(display_message_text)
    
    def look_for_npc(self, x, y):
        for npc in self.npcs:
            if npc.sub_scene_id == self.scene_controller.current_sub_scene_id:
                if npc.sub_scene_location == (x, y):
                    return npc
                
    def get_upper_talker_img(self):
        if self.talking_npc is None:
            return None
        return self.talking_npc.get_talker_img()
        
    def get_lower_talker_img(self):
        if self.main_character_head_img is None:
            main_character_head_img = pygame.image.load(self.root_folder + "/original_resource/resource/hdgrp/0.png")
            main_character_head_img_scaled = pygame.transform.scale(main_character_head_img,(92, 92))
            self.main_character_head_img = main_character_head_img_scaled
            
        return self.main_character_head_img

        
    def process_events(self, time_delta):
        detected_send_action = False
        event_comsumed = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                
                if self.game_status == GameStatus.TALKING:
                    if event.key == pygame.K_ESCAPE:
                        self.ui_controller.text_entry.unfocus()
                        self.game_status = GameStatus.INGAME
                    elif event.key == pygame.K_RETURN:
                        # Check if the Shift key is also pressed
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
                        if shift_pressed:
                            # print("Shift+Enter detected!")
                            
                            detected_send_action = True
                            event_comsumed = True
                            
                            input_text = self.ui_controller.text_entry.get_text()
                            
                            html_format_text = "<font color='#FFFFFF'> 你说:\n" + input_text + "</font>"
                            
                            self.ui_controller.system_message_box.append_html_text(html_format_text + "\n")
                            
                            self.ui_controller.system_message_box.update_text_end_position(1000)
                            
                            self.ui_controller.text_entry.set_text("")
                            
                            talking_npc_thinking = "<font color='#00FF00>若有所思中...</font>"
                            
                            self.ui_controller.upper_talk_box.set_text(talking_npc_thinking)
                            
                            self.ui_controller.lower_talk_box.set_text(input_text)
                            
                            main_character_cn_name = self.main_character.cn_name
                            main_character_id = self.main_character.id_in_game
                            
                            npc_id = self.talking_npc.id_in_game
                            npc_cn_name = self.talking_npc.cn_name
                            
                            message = Message(main_character_id, main_character_cn_name, npc_id, npc_cn_name, input_text)
                            
                            self.talking_npc.at_msg_receive(message)
                            
                elif self.game_status == GameStatus.INGAME:
                
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_RETURN:
                        if self.scene_controller.current_scene_type == SceneType.SUB_SCENE:
                            (character_facing_x, character_facing_y) = self.main_character.get_facing_grid_location()
                            print('character_facing_x: ', character_facing_x)
                            print('character_facing_y: ', character_facing_y)
                            
                            facing_npc = self.look_for_npc(character_facing_x, character_facing_y)
                            
                            if facing_npc is not None:
                                print('facing_npc: ', facing_npc)
                                self.game_status = GameStatus.TALKING
                                self.talking_npc = facing_npc
                                self.ui_controller.text_entry.focus()
                                event_comsumed = True
                            else:
                                print('no npc found')
                    
                
                    
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
                
            if not event_comsumed:
                self.ui_controller.ui_manager.process_events(event)
                self.ui_controller.ui_manager.update(time_delta)
            
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