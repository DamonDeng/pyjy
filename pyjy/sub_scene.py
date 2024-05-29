import numpy as np
from pyjy.constants import GameConfig
from pyjy.utils import BinaryReader



class SceneMapData:
    
    grid_number_width = GameConfig.SUB_SCENE_GRID_NUMBER_W
    grid_number_height = GameConfig.SUB_SCENE_GRID_NUMBER_H
    
    def __init__(self):
        self.scene_layer_np = None
        self.event_data_np = None
        
        self.scene_id = 0
    
    
    def load_data(self, \
        sin_file_name = "./original_resource/save/allsin.grp", \
        def_file_name = "./original_resource/save/alldef.grp"):

        scene_layer_result = BinaryReader.read_file_to_vector(sin_file_name, "H")
        event_data_result = BinaryReader.read_file_to_vector(def_file_name, "h")

        self.scene_layer_np = np.array(scene_layer_result[:GameConfig.SUB_SCENE_ALL_LAYER_DATA_LENGTH]) \
                                    .reshape(GameConfig.SUB_SCENE_NUMBER, \
                                            GameConfig.SUB_SCENE_DATA_LAYER_NUMBER, \
                                            GameConfig.SUB_SCENE_LAYER_DATA_LENGTH)
                                    
        self.event_data_np = np.array(event_data_result[:GameConfig.SUB_SCENE_ALL_EVENT_DATA_LENGTH]) \
                                    .reshape(GameConfig.SUB_SCENE_NUMBER, \
                                            GameConfig.SUB_SCENE_EVENT_NUMBER_PER_SCENE, \
                                            GameConfig.SUB_SCENE_EVENT_DATA_LENGTH)
                                    
        self.switch_scene_data_by_id(1)
    
    
    def switch_scene_data_by_id(self, scene_id):
        self.scene_id = scene_id
        
        self.surface_map = self.scene_layer_np[scene_id][0].reshape(SceneMapData.grid_number_width, SceneMapData.grid_number_height)
        self.building_map = self.scene_layer_np[scene_id][1].reshape(SceneMapData.grid_number_width, SceneMapData.grid_number_height)
        self.decoration_map = self.scene_layer_np[scene_id][2].reshape(SceneMapData.grid_number_width, SceneMapData.grid_number_height)
        self.event_id_map = self.scene_layer_np[scene_id][3].reshape(SceneMapData.grid_number_width, SceneMapData.grid_number_height)
        self.building_hight_map = self.scene_layer_np[scene_id][4].reshape(SceneMapData.grid_number_width, SceneMapData.grid_number_height)
        self.decoration_hight_map = self.scene_layer_np[scene_id][5].reshape(SceneMapData.grid_number_width, SceneMapData.grid_number_height)
        
        self.event_data = self.event_data_np[scene_id]
        
        self.event_current_pic = np.zeros((SceneMapData.grid_number_width, SceneMapData.grid_number_height))
        self.event_start_pic = np.zeros((SceneMapData.grid_number_width, SceneMapData.grid_number_height))
        self.event_end_pic = np.zeros((SceneMapData.grid_number_width, SceneMapData.grid_number_height))
        
        self.walkable_map = self.building_map == 0
        
        # check the surface_map to see if there is any water grid
        # the checking logic is from the above c++ code from original project
        
        for x in range(SceneMapData.grid_number_width):
            for y in range(SceneMapData.grid_number_height):
                num = self.surface_map[x, y] // 2
                if (num >= 179 and num <= 181) or num == 261 or num == 511 or (num >= 662 and num <= 665) or num == 674:
                    self.walkable_map[x, y] = False
        
        
        for i in range(len(self.event_data)):
            if self.event_data[i][9] != 0 and self.event_data[i][10] != 0:
                if self.event_data[i][6] != -1:
                    self.event_current_pic[self.event_data[i][10], self.event_data[i][9]] = self.event_data[i][5]
                    self.event_start_pic[self.event_data[i][10], self.event_data[i][9]] = self.event_data[i][6]
                    self.event_end_pic[self.event_data[i][10], self.event_data[i][9]] = self.event_data[i][7]
                    
                if self.event_data[i][0] == 1:
                    self.walkable_map[self.event_data[i][10], self.event_data[i][9]] = False
            
            
    
class SubSceneDrawer:
    
    def __init__(self, main_character, scene_map_data, texture_manager, camera):
        self.main_character = main_character
        self.scene_map_data = scene_map_data
        self.texture_manager = texture_manager
        self.camera = camera
        
        self.grid_size_w = GameConfig.SUB_SCENE_GRID_SIZE_W
        self.grid_size_h = GameConfig.SUB_SCENE_GRID_SIZE_H
        
        self.grid_number_w = GameConfig.SUB_SCENE_GRID_NUMBER_W
        self.grid_number_h = GameConfig.SUB_SCENE_GRID_NUMBER_H
        
        self.start_x = (self.grid_number_w/2) * self.grid_size_w
        self.start_y = 0
        
        self.grid_offset = np.zeros((self.grid_number_h, self.grid_number_w, 2))
        
        grid_offset_start_x = self.start_x
        grid_offset_start_y = self.start_y
            
        for i in range(self.grid_number_h):
            for j in range(self.grid_number_w):
                
                offset_x = grid_offset_start_x + j * self.grid_size_w/2
                offset_y = grid_offset_start_y + j * self.grid_size_h/2
    
                self.grid_offset[i, j, 0] = offset_x
                self.grid_offset[i, j, 1] = offset_y
                
            grid_offset_start_x -= self.grid_size_w/2
            grid_offset_start_y += self.grid_size_h/2
            
    def draw_texture(self, texture, screen, i, j, camera, offset_data=(0,0), object_height=0):
            
            
            x = self.grid_offset[i, j, 0]
            y = self.grid_offset[i, j, 1]
            
            x -= camera.pixel_x
            y -= camera.pixel_y
            
            if x + self.grid_number_w < 0  or y + self.grid_number_h < 0 :
                # out of camera screen
                return
            
            x = x - offset_data[0] 
            y = y - offset_data[1] - object_height
            
            if x > camera.max_screen_x or y > camera.max_screen_y:
                return
                
            screen.blit(texture, (x, y))
        
        
    def draw_surface(self, screen, i, j, camera):
        
        
        surface_value = self.scene_map_data.surface_map[i, j]
        surface_value = surface_value //2 # because of the original data was doubled in original project
        
        surface_texture = self.texture_manager.get_texture_pygame(surface_value)
        
        if len(surface_texture) == 0:
            return
        
        offset_data = self.texture_manager.get_offset(surface_value)
        
        self.draw_texture(surface_texture[0], screen, i, j, camera, offset_data)
        
    def draw_element(self, screen, i, j, camera):
        
        # draw building
        building_texture_id = self.scene_map_data.building_map[i][j]//2
        building_height = self.scene_map_data.building_hight_map[i][j]
        
        if building_texture_id != 0:
            building_texture = self.texture_manager.get_texture_pygame(building_texture_id)
            if len(building_texture) != 0:
                building_offset_data = self.texture_manager.get_offset(building_texture_id)
                self.draw_texture(building_texture[0], screen, i, j, camera, building_offset_data, building_height)
        
        
        # # draw event, including NPCs
        event_texture_id = self.scene_map_data.event_current_pic[i][j]//2
        if event_texture_id != 0:
            event_texture = self.texture_manager.get_texture_pygame(event_texture_id)
            if len(event_texture) != 0:
                building_offset_data = self.texture_manager.get_offset(event_texture_id)
                # using the building height to draw the event
                self.draw_texture(event_texture[0], screen, i, j, camera, building_offset_data, building_height)
        
        
        # draw main character
        
        if j == self.main_character.x and i == self.main_character.y:
            character_texture = self.main_character.get_current_texture()
            character_offset_data = self.main_character.get_current_offset()
            # print('try to draw the character at : ', i, j)
            # print('character_texture: ', character_texture)
            # print('character_offset_data: ', character_offset_data)
            # print('building_height: ', building_height)
            # print('camera: ', camera.pixel_x, camera.pixel_y)
            self.draw_texture(character_texture, screen, i, j, camera, character_offset_data, building_height)
        
            
        # draw decorations
        decoration_texture_id = self.scene_map_data.decoration_map[i][j]//2
        if decoration_texture_id != 0:
            decoration_height = self.scene_map_data.decoration_hight_map[i][j]
            decoration_texture = self.texture_manager.get_texture_pygame(decoration_texture_id)
            if len(decoration_texture) != 0:
                decoration_offset_data = self.texture_manager.get_offset(decoration_texture_id)
                self.draw_texture(decoration_texture[0], screen, i, j, camera, decoration_offset_data, decoration_height)
        
        
    
    def draw(self, screen):
        
        # print("Character x, y: ", self.main_character.x, self.main_character.y)
        
        # # draw surface at first:
        for i in range(self.grid_number_h):
            for j in range(self.grid_number_w):    
                # print("i, j: ", i, j)
                self.draw_surface(screen, i, j, self.camera)
                

            
            
        # draw others:
        for i in range(self.grid_number_h):
            for j in range(self.grid_number_w):    
                self.draw_element(screen, i, j, self.camera)
        
    
    
        
        
 