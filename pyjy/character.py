from pyjy.texture import TextureManager, MainCharacterTextureLoader
from pyjy.constants import GameConfig
from pyjy.constants import SceneType
from pyjy.constants import Direction

import pygame

class MainCharacter:
    
    def __init__(self, x, y, texture_manager, main_scene_data, sub_scene_data):
        # self.scene_status = MainCharacter.InMain
        
        self.main_x = x
        self.main_y = y
        self.sub_x = 0
        self.sub_y = 0
        self.fight_x = 0
        self.fight_y = 0
        
        self.x = x
        self.y = y
        
        self.prev_x = x
        self.prev_y = y
        
        self.current_scene_type = SceneType.MAIN_SCENE
        
        self.texture_manager = texture_manager
        self.main_scene_data = main_scene_data
        self.sub_scene_data = sub_scene_data
        
        
        self.current_direction = Direction.DOWN
        self.current_pic_index = 0
        
        self.move_pic_delay = 5 # how many frame to change the pic
        self.move_count = 0
        
        
    def set_scene(self, scene_type):
        self.current_scene_type = scene_type
        
    def set_location(self, x, y):
        if self.current_scene_type == SceneType.MAIN_SCENE:
            self.main_x = x
            self.main_y = y
        elif self.current_scene_type == SceneType.SUB_SCENE:
            self.sub_x = x
            self.sub_y = y
        elif self.current_scene_type == SceneType.FIGHT_SCENE:
            self.fight_x = x
            self.fight_y = y
            
        self.x = x
        self.y = y
        
    def get_current_texture(self):
        
        # print('self.current_scene_type: ', self.current_scene_type)
        texture = self.texture_manager.get_main_character_texture(self.current_scene_type, self.current_direction, self.current_pic_index)
        
        if len(texture) == 0:
            return None
        
        return texture[0]
    
    def get_current_offset(self):
        
        
        offset = self.texture_manager.get_main_character_offset(self.current_scene_type, self.current_direction, self.current_pic_index)
        
        return offset
        
    def remember_prev_location(self):
        self.prev_x = self.x
        self.prev_y = self.y
    
    def tick(self):
        keys = pygame.key.get_pressed()
        
        input_move_direction = None
        if keys[pygame.K_UP]:
            input_move_direction = Direction.UP
        if keys[pygame.K_DOWN]:
            input_move_direction = Direction.DOWN
        if keys[pygame.K_LEFT]:
            input_move_direction = Direction.LEFT
        if keys[pygame.K_RIGHT]:
            input_move_direction = Direction.RIGHT
            
        if input_move_direction != None:
            if input_move_direction != self.current_direction:
                self.current_direction = input_move_direction
                self.current_pic_index = 0
                self.move_count = 0
            
            
            if self.move_count % self.move_pic_delay == 0:
                if self.current_scene_type == SceneType.MAIN_SCENE:
                    can_move = False
                    # print('self.x: ', self.x, 'self.y: ', self.y)
                    MAIN_SCENE_UP_BOUND = 15
                    MAIN_SCENE_LEFT_BOUND = 15
                    MAIN_SCENE_DOWN_BOUND = GameConfig.MAIN_SCENE_GRID_NUMBER_H - 18
                    MAIN_SCENE_RIGHT_BOUND = GameConfig.MAIN_SCENE_GRID_NUMBER_W - 18
                    
                    # print('self.x: ', self.x, 'self.y: ', self.y)
                    # print("UP BOUND: ", MAIN_SCENE_UP_BOUND)
                    # print("DOWN BOUND: ", MAIN_SCENE_DOWN_BOUND)
                    # print("LEFT BOUND: ", MAIN_SCENE_LEFT_BOUND)
                    # print("RIGHT BOUND: ", MAIN_SCENE_RIGHT_BOUND)
                    
                    if input_move_direction == Direction.UP:
                        if self.y - 1 >= MAIN_SCENE_UP_BOUND:
                            if self.main_scene_data.walkable_map[self.y - 1][self.x]:
                                can_move = True
                                self.remember_prev_location()
                                self.y -= 1
                    elif input_move_direction == Direction.DOWN:
                        if self.y + 1 < MAIN_SCENE_DOWN_BOUND:
                            if self.main_scene_data.walkable_map[self.y + 1][self.x]:
                                can_move = True
                                self.remember_prev_location()
                                self.y += 1
                    elif input_move_direction == Direction.LEFT:
                        if self.x - 1 >= MAIN_SCENE_LEFT_BOUND:
                            if self.main_scene_data.walkable_map[self.y][self.x - 1]:
                                can_move = True
                                self.remember_prev_location()
                                self.x -= 1
                    elif input_move_direction == Direction.RIGHT:
                        if self.x + 1 < MAIN_SCENE_RIGHT_BOUND:
                            if self.main_scene_data.walkable_map[self.y][self.x + 1]:
                                can_move = True
                                self.remember_prev_location()
                                self.x += 1
                elif self.current_scene_type == SceneType.SUB_SCENE:
                    can_move = False
                    # print('self.x: ', self.x, 'self.y: ', self.y)
                    if input_move_direction == Direction.UP:
                        if self.sub_scene_data.walkable_map[self.y - 1][self.x]:
                            can_move = True
                            self.remember_prev_location()
                            self.y -= 1
                    elif input_move_direction == Direction.DOWN:
                        if self.sub_scene_data.walkable_map[self.y + 1][self.x]:
                            can_move = True
                            self.remember_prev_location()
                            self.y += 1
                    elif input_move_direction == Direction.LEFT:
                        if self.sub_scene_data.walkable_map[self.y][self.x - 1]:
                            can_move = True
                            self.remember_prev_location()
                            self.x -= 1
                    elif input_move_direction == Direction.RIGHT:
                        if self.sub_scene_data.walkable_map[self.y][self.x + 1]:
                            can_move = True
                            self.remember_prev_location()
                            self.x += 1
                else:
                    can_move = False
                            
                if can_move:
                    self.current_pic_index += 1
                    if self.current_pic_index >= MainCharacterTextureLoader.PIC_NUMBER:
                        self.current_pic_index = 1
                    # self.moving_x = self.x
                    # self.moving_y = self.y
                
            self.move_count += 1
                
            
    def set_direction(self, direction):
        self.current_direction = direction
        
    def set_pic_index(self, index):
        self.current_pic_index = index