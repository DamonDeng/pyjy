from pyjy.texture import MainCharacterTextureManager
from pyjy.constants import GameConfig

import pygame

class MainCharacter:
    
    InMain = 0
    InSub = 1
    InFight = 2
    
    def __init__(self, x, y, main_scene_texture_manager, sub_scene_texture_manager, main_scene_data, sub_scene_data):
        self.scene_status = MainCharacter.InMain
        
        self.main_x = x
        self.main_y = y
        self.sub_x = 0
        self.sub_y = 0
        self.fight_x = 0
        self.fight_y = 0
        
        self.x = x
        self.y = y
        self.main_scene_texture_manager = main_scene_texture_manager
        self.sub_scene_texture_manager = sub_scene_texture_manager
        self.main_scene_data = main_scene_data
        self.sub_scene_data = sub_scene_data
        
        
        self.current_direction = MainCharacterTextureManager.DOWN
        self.current_pic_index = 0
        
        # self.is_moving_to_target = False
        # self.target_x = 0
        # self.target_y = 0
        
        # self.moving_x = x
        # self.moving_y = y
        
        # self.move_speed = 0.1 # percentage of grid moved per second
        self.move_pic_delay = 5 # how many frame to change the pic
        self.move_count = 0
        # self.has_move_action = False
        
    def set_scene_status(self, status):
        self.scene_status = status
        
    def set_location(self, x, y):
        if self.scene_status == MainCharacter.InMain:
            self.main_x = x
            self.main_y = y
        elif self.scene_status == MainCharacter.InSub:
            self.sub_x = x
            self.sub_y = y
        elif self.scene_status == MainCharacter.InFight:
            self.fight_x = x
            self.fight_y = y
            
        self.x = x
        self.y = y
        
    def get_current_texture(self):
        
        if self.scene_status == MainCharacter.InMain:
            texture = self.main_scene_texture_manager.get_texture(self.current_direction, self.current_pic_index)
        elif self.scene_status == MainCharacter.InSub:
            texture = self.sub_scene_texture_manager.get_texture(self.current_direction, self.current_pic_index)
        
        if len(texture) == 0:
            return None
        
        return texture[0]
    
    def get_current_offset(self):
        
        if self.scene_status == MainCharacter.InMain:
            offset = self.main_scene_texture_manager.get_offset(self.current_direction, self.current_pic_index)
        elif self.scene_status == MainCharacter.InSub:
            offset = self.sub_scene_texture_manager.get_offset(self.current_direction, self.current_pic_index)
        
        return offset
        
    
    def tick(self):
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     camera_y -= camera_speed
        # if keys[pygame.K_s]:
        #     camera_y += camera_speed
        # if keys[pygame.K_a]:
        #     camera_x -= camera_speed
        # if keys[pygame.K_d]:
        #     camera_x += camera_speed
            
        # if main_character.is_moving_to_target:
        #     main_character.move(main_character.current_direction, FPS, frame_count)
        # else:
        
        input_move_direction = None
        if keys[pygame.K_UP]:
            input_move_direction = MainCharacterTextureManager.UP
        if keys[pygame.K_DOWN]:
            input_move_direction = MainCharacterTextureManager.DOWN
        if keys[pygame.K_LEFT]:
            input_move_direction = MainCharacterTextureManager.LEFT
        if keys[pygame.K_RIGHT]:
            input_move_direction = MainCharacterTextureManager.RIGHT
            
        if input_move_direction != None:
            if input_move_direction != self.current_direction:
                self.current_direction = input_move_direction
                self.current_pic_index = 0
                self.move_count = 0
            
            
            if self.move_count % self.move_pic_delay == 0:
                if self.scene_status == MainCharacter.InMain:
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
                    
                    if input_move_direction == MainCharacterTextureManager.UP:
                        if self.y - 1 >= MAIN_SCENE_UP_BOUND:
                            if self.main_scene_data.walkable_map[self.y - 1][self.x]:
                                can_move = True
                                self.y -= 1
                    elif input_move_direction == MainCharacterTextureManager.DOWN:
                        if self.y + 1 < MAIN_SCENE_DOWN_BOUND:
                            if self.main_scene_data.walkable_map[self.y + 1][self.x]:
                                can_move = True
                                self.y += 1
                    elif input_move_direction == MainCharacterTextureManager.LEFT:
                        if self.x - 1 >= MAIN_SCENE_LEFT_BOUND:
                            if self.main_scene_data.walkable_map[self.y][self.x - 1]:
                                can_move = True
                                self.x -= 1
                    elif input_move_direction == MainCharacterTextureManager.RIGHT:
                        if self.x + 1 < MAIN_SCENE_RIGHT_BOUND:
                            if self.main_scene_data.walkable_map[self.y][self.x + 1]:
                                can_move = True
                                self.x += 1
                else:
                    can_move = False
                    # print('self.x: ', self.x, 'self.y: ', self.y)
                    if input_move_direction == MainCharacterTextureManager.UP:
                        if self.sub_scene_data.walkable_map[self.y - 1][self.x]:
                            can_move = True
                            self.y -= 1
                    elif input_move_direction == MainCharacterTextureManager.DOWN:
                        if self.sub_scene_data.walkable_map[self.y + 1][self.x]:
                            can_move = True
                            self.y += 1
                    elif input_move_direction == MainCharacterTextureManager.LEFT:
                        if self.sub_scene_data.walkable_map[self.y][self.x - 1]:
                            can_move = True
                            self.x -= 1
                    elif input_move_direction == MainCharacterTextureManager.RIGHT:
                        if self.sub_scene_data.walkable_map[self.y][self.x + 1]:
                            can_move = True
                            self.x += 1
                if can_move:
                    self.current_pic_index += 1
                    if self.current_pic_index >= MainCharacterTextureManager.PIC_NUMBER:
                        self.current_pic_index = 1
                    self.moving_x = self.x
                    self.moving_y = self.y
                
            self.move_count += 1

        
        
    # def move(self, move_direction):
        
    #     if move_direction != self.current_direction:
    #         self.current_direction = move_direction
    #         self.current_pic_index = 1
    #         self.move_count = 0
    #     else:
    #         self.move_count += 1
    #         if self.move_count % self.move_pic_delay == 0:
    #             self.current_pic_index += 1
    #             if self.current_pic_index >= MainCharacterTextureManager.PIC_NUMBER:
    #                 self.current_pic_index = 1

        
    #     if self.is_moving_to_target:
            
    #         if self.current_direction == MainCharacterTextureManager.UP:
                
    #             if self.moving_y < self.y - 0.5:
    #                 self.y = self.target_y
                
    #             if self.moving_y > self.target_y:
    #                 self.moving_y -= self.move_speed
    #             else:
    #                 self.is_moving_to_target = False
    #                 if self.has_move_action == False:
    #                     self.current_pic_index = 0
                    
    #         elif self.current_direction == MainCharacterTextureManager.DOWN:
                
    #             if self.moving_y > self.y + 0.5:
    #                 self.y = self.target_y
                
    #             if self.moving_y < self.target_y:
    #                 self.moving_y += self.move_speed
    #             else:
    #                 self.is_moving_to_target = False
    #                 if self.has_move_action == False:
    #                     self.current_pic_index = 0
                    
    #         elif self.current_direction == MainCharacterTextureManager.LEFT:
                    
    #             if self.moving_x < self.x - 0.5:
    #                 self.x = self.target_x
                
    #             if self.moving_x > self.target_x:
    #                 self.moving_x -= self.move_speed
    #             else:
    #                 self.is_moving_to_target = False
    #                 if self.has_move_action == False:
    #                     self.current_pic_index = 0
                        
    #         elif self.current_direction == MainCharacterTextureManager.RIGHT:
    #             if self.moving_x > self.x + 0.5:
    #                 self.x = self.target_x
                
    #             if self.moving_x < self.target_x:
    #                 self.moving_x += self.move_speed
    #             else:
    #                 self.is_moving_to_target = False
    #                 if self.has_move_action == False:
    #                     self.current_pic_index = 0
                    
            
    #     else:

            
    #         if move_direction == MainCharacterTextureManager.UP:
                
    #             # if current_scene_map_data.walkable_map[self.y - 1, self.x]:
    #                 self.target_y = self.y - 1
    #                 self.target_x = self.x
                    
    #                 self.moving_y = self.y - self.move_speed
    #                 self.moving_x = self.x
                    
    #                 self.is_moving_to_target = True
    #                 self.has_move_action = True
                    
    #         elif move_direction == MainCharacterTextureManager.DOWN:
                
    #             # if current_scene_map_data.walkable_map[self.y + 1, self.x]:
    #                 self.target_y = self.y + 1
    #                 self.target_x = self.x
                    
    #                 self.moving_y = self.y + self.move_speed
    #                 self.moving_x = self.x
                    
    #                 self.is_moving_to_target = True
    #                 self.has_move_action = True
                    
    #         elif move_direction == MainCharacterTextureManager.LEFT:
                
    #             # if current_scene_map_data.walkable_map[self.y, self.x - 1]:
    #                 self.target_y = self.y
    #                 self.target_x = self.x - 1
                    
    #                 self.moving_y = self.y
    #                 self.moving_x = self.x - self.move_speed
                    
    #                 self.is_moving_to_target = True
    #                 self.has_move_action = True
                    
    #         elif move_direction == MainCharacterTextureManager.RIGHT:
                
    #             # if current_scene_map_data.walkable_map[self.y, self.x + 1]:
    #                 self.target_y = self.y
    #                 self.target_x = self.x + 1
                    
    #                 self.moving_y = self.y
    #                 self.moving_x = self.x + self.move_speed
                    
    #                 self.is_moving_to_target = True
    #                 self.has_move_action = True
                
            
    def set_direction(self, direction):
        self.current_direction = direction
        
    def set_pic_index(self, index):
        self.current_pic_index = index