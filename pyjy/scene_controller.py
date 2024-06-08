from pyjy.constants import SceneType, Direction
from pyjy.music_player import MusicPlayer
import pygame

class SceneController:
    
    def __init__(self, submaps, main_scene_drawer, sub_scene_drawer, music_player):
        
        self.current_scene_type = SceneType.MAIN_SCENE
        
        self.submaps = submaps
        self.main_scene_drawer = main_scene_drawer
        self.sub_scene_drawer = sub_scene_drawer
        self.music_player = music_player
        
        self.sub_scene_info = {}
        
        for submap in submaps:
            sub_scene_id = submap["ID"]
            self.sub_scene_info[sub_scene_id] = submap
        
        self.main_entrance_set = {}
        
        for submap in submaps:
            sub_scene_id = submap["ID"]
            entrance_x = submap["MainEntranceX1"]
            entrance_y = submap["MainEntranceY1"]
            
            self.main_entrance_set[(entrance_x, entrance_y)] = sub_scene_id
            
            self.main_scene_drawer.scene_map_data.walkable_map[entrance_y][entrance_x] = True
            
        self.current_sub_scene_id = 1
        self.current_sub_scene_info = self.sub_scene_info[self.current_sub_scene_id]
            
            
    def draw(self, screen):
        # print("SceneController draw")
        # print("current_scene_type: ", self.current_scene_type)
        
        if self.current_scene_type == SceneType.MAIN_SCENE:
            self.main_scene_drawer.draw(screen)
        elif self.current_scene_type == SceneType.SUB_SCENE:
            self.sub_scene_drawer.draw(screen)
            
        # drawing a rectangle into the screen for debug:
        # pygame.draw.rect(screen, (255, 0, 0), (0, 0, 100, 100), 0)
            
    def detect_to_switch(self):
        
        if self.current_scene_type == SceneType.MAIN_SCENE:
            x = self.main_scene_drawer.main_character.x
            y = self.main_scene_drawer.main_character.y
            
            # print("x, y: ", x, y)
            
            if (x, y) in self.main_entrance_set:
                # entering the sub scene connected by entrance x and y
                self.current_scene_type = SceneType.SUB_SCENE
                sub_scene_id = self.main_entrance_set[(x, y)]
                self.current_sub_scene_id = sub_scene_id
                self.current_sub_scene_info = self.sub_scene_info[sub_scene_id]
                self.sub_scene_drawer.scene_map_data.switch_scene_data_by_id(sub_scene_id)
                
                init_x = self.current_sub_scene_info["EntranceX"]
                init_y = self.current_sub_scene_info["EntranceY"]
                
                self.main_scene_drawer.main_character.set_location(init_x, init_y)
                self.main_scene_drawer.main_character.current_scene_type = SceneType.SUB_SCENE
                
                enter_music_id = self.current_sub_scene_info["EntranceMusic"]
                
                self.music_player.play_mid_by_id(enter_music_id)
                
                
                
        elif self.current_scene_type == SceneType.SUB_SCENE:
            x = self.sub_scene_drawer.main_character.x
            y = self.sub_scene_drawer.main_character.y
            
            exit_x_list = self.current_sub_scene_info["ExitX"]
            exit_y_list = self.current_sub_scene_info["ExitY"]
            
            exit_position_list = [(exit_x_list[0], exit_y_list[0]), (exit_x_list[1], exit_y_list[1]), (exit_x_list[2], exit_y_list[2])]
            
            if (x, y) in exit_position_list:
                self.current_scene_type = SceneType.MAIN_SCENE
                
                # find out the entrance from the main scene to the sub scene
                # which should be the location main character should be placed
                # in order to avoid hitting the entrance event again. 
                # we need to move the main character one grid away from the entrance.
                # the first try is to move the main character one grid following his/her current direction.
                # if the grid is not walkable, then we need to try the other three directions.
                
                main_entrance_x = self.current_sub_scene_info["MainEntranceX1"]
                main_entrance_y = self.current_sub_scene_info["MainEntranceY1"]
                
                current_direction = self.sub_scene_drawer.main_character.current_direction
                
                # try to move one grid away from the entrance
                if current_direction == Direction.UP:
                    new_entrance_x = main_entrance_x
                    new_entrance_y = main_entrance_y - 1
                elif current_direction == Direction.DOWN:
                    new_entrance_x = main_entrance_x
                    new_entrance_y = main_entrance_y + 1
                elif current_direction == Direction.LEFT:
                    new_entrance_x = main_entrance_x - 1
                    new_entrance_y = main_entrance_y
                elif current_direction == Direction.RIGHT:
                    new_entrance_x = main_entrance_x + 1
                    new_entrance_y = main_entrance_y
                    
                found_walkable = False
                
                if self.main_scene_drawer.scene_map_data.walkable_map[new_entrance_x][new_entrance_y] == False:
                    position_to_try = [(main_entrance_x, main_entrance_y - 1), \
                                        (main_entrance_x, main_entrance_y + 1), \
                                        (main_entrance_x - 1, main_entrance_y), \
                                        (main_entrance_x + 1, main_entrance_y)]
                    
                    for (x, y) in position_to_try:
                        if self.main_scene_drawer.scene_map_data.walkable_map[x][y] == True:
                            new_entrance_x = x
                            new_entrance_y = y
                            found_walkable = True
                            break
                else:
                    found_walkable = True
                    
                if found_walkable == False:
                    # if no walkable grid is found, we keep in the sub scene
                    self.current_scene_type = SceneType.SUB_SCENE
                    
                else:
                    
                    enter_music_id = self.current_sub_scene_info["ExitMusic"]
                
                    self.music_player.play_mid_by_id(enter_music_id)
                
                    self.sub_scene_drawer.main_character.set_location(new_entrance_x, new_entrance_y)
                    self.sub_scene_drawer.main_character.current_scene_type = SceneType.MAIN_SCENE
    
        
    
        