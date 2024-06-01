import numpy as np
from pyjy.constants import GameConfig
from pyjy.utils import BinaryReader

class MainSceneMapData:
    
    grid_number_width  = GameConfig.MAIN_SCENE_GRID_NUMBER_W
    grid_number_height = GameConfig.MAIN_SCENE_GRID_NUMBER_H
    
    def __init__(self, main_scene_texture_manager):
        self.main_scene_texture_manager = main_scene_texture_manager
         
    def load_data(self, \
        folder_name = "./original_resource/resource/"):
        
        earch_file_name = folder_name + "earth.002"
        surface_file_name = folder_name + "surface.002"
        building_file_name = folder_name + "building.002"
        buidx_file_name = folder_name + "buildx.002"
        buidy_file_name = folder_name + "buildy.002"
        
        # earth_result = BinaryReader.read_file_to_vector(earch_file_name, "H")
        # surface_result = BinaryReader.read_file_to_vector(surface_file_name, "H")
        # building_result = BinaryReader.read_file_to_vector(building_file_name, "H")
        # buidx_result = BinaryReader.read_file_to_vector(buidx_file_name, "H")
        # buidy_result = BinaryReader.read_file_to_vector(buidy_file_name, "H")
        
        earth_result = BinaryReader.read_file_to_vector(earch_file_name, "h")
        surface_result = BinaryReader.read_file_to_vector(surface_file_name, "h")
        building_result = BinaryReader.read_file_to_vector(building_file_name, "h")
        # buidx_result = BinaryReader.read_file_to_vector(buidx_file_name, "h")
        # buidy_result = BinaryReader.read_file_to_vector(buidy_file_name, "h")
        
        earth_result_np = np.array(earth_result)
        surface_result_np = np.array(surface_result)
        building_result_np = np.array(building_result)
        # buidx_result_np = np.array(buidx_result)
        # buidy_result_np = np.array(buidy_result)

        earch_result_reshaped = earth_result_np.reshape((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H))
        surface_result_reshaped = surface_result_np.reshape((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H))
        building_result_reshaped = building_result_np.reshape((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H))
        
        # # seems that the buidx and buidy are not used.
        # buidx_result_reshaped = buidx_result_np.reshape((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H))
        # buidy_result_reshaped = buidy_result_np.reshape((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H))
        
        # self.adjust_building_map = building_result_reshaped.copy()
        # build a int np array to store the adjusting value.
        # self.adjust_gride_number = np.zeros((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H), dtype=int)
        # self.original_building_i = np.zeros((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H), dtype=int)
        # self.original_building_j = np.zeros((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H), dtype=int)
        
        self.building_everage = np.zeros((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H), dtype=int)
        
        self.walkable_map = np.ones((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H), dtype=bool)
        for i in range(GameConfig.MAIN_SCENE_GRID_NUMBER_W):
            for j in range(GameConfig.MAIN_SCENE_GRID_NUMBER_H):
                # average of the top left corner and bottom right corner.
                # no need to dive by 2 or 4, because the value is int.
                self.building_everage[i][j] = i + j + i + j
                
        for i in range(GameConfig.MAIN_SCENE_GRID_NUMBER_W):
            for j in range(GameConfig.MAIN_SCENE_GRID_NUMBER_H):
                if building_result_reshaped[i][j] != 0:
                    texture_width, texture_height = self.main_scene_texture_manager.get_image_size(building_result_reshaped[i][j]//2)
                    
                    # 10 is the edge of the building.
                    # adding the texture width with one grid size
                    # to make the building with less than one gride size to be adjusted to be one grid size.
                    # minus 10 to make sure that building exactly be one grid to be adjusted to be more than one grid.
                    gride_width = (texture_width+GameConfig.MAIN_SCENE_GRID_SIZE_W-10)// GameConfig.MAIN_SCENE_GRID_SIZE_W
                    
                    # print("i, j, gride_width", i, j, gride_width)
                    
                    # building the walkable map.
                    for target_i in range(i - gride_width + 1, i + 1):
                        for target_j in range(j - gride_width + 1, j + 1):
                            if target_i > 0 and target_j > 0:
                                # self.adjust_building_map[target_i][target_j] = building_result_reshaped[i][j]
                                # self.adjust_gride_number[target_i][target_j] = gride_width - 1
                                self.walkable_map[target_i][target_j] = False
                                
                    target_i = i - gride_width + 1
                    target_j = j - gride_width + 1
                    
                    if target_i < 0:
                        target_i = 0
                    if target_j < 0:
                        target_j = 0
                        
                    # self.adjust_building_map[target_i][target_j] = building_result_reshaped[i][j]
                    # self.original_building_i[target_i][target_j] = i
                    # self.original_building_j[target_i][target_j] = j
                    
                    self.building_everage[i][j] = i + j + target_i + target_j
            
        # self.draw_sequence = self.building_everage.copy()        
        # self.drawing_sequence = np.zeros((GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H), dtype=int)
        
        # number_to_generate = min(GameConfig.MAIN_SCENE_GRID_NUMBER_W, GameConfig.MAIN_SCENE_GRID_NUMBER_H)
        
        # for i in range(GameConfig.MAIN_SCENE_GRID_NUMBER_H):
        #     for j in range(GameConfig.MAIN_SCENE_GRID_NUMBER_W):
        #         self.drawing_sequence[i][j] = i * GameConfig.MAIN_SCENE_GRID_NUMBER_W*GameConfig.MAIN_SCENE_GRID_NUMBER_H + j + 1
        
        # for i in range(GameConfig.MAIN_SCENE_GRID_NUMBER_H):
        #     for j in range(GameConfig.MAIN_SCENE_GRID_NUMBER_W):
        #         if self.adjust_building_map[i][j] != 0:
        #             original_i = self.original_building_i[i][j]
        #             original_j = self.original_building_j[i][j]
        #             self.drawing_sequence[original_i][original_j] = i * GameConfig.MAIN_SCENE_GRID_NUMBER_W*GameConfig.MAIN_SCENE_GRID_NUMBER_H + j + 1

        # current_seq = 1
        
        # for n in range(number_to_generate): 
        #     for m_h in range(n, GameConfig.MAIN_SCENE_GRID_NUMBER_W):
        #         self.drawing_sequence[n][m_h] = current_seq
        #         current_seq += 1
                
        #     for m_v in range(n+1, GameConfig.MAIN_SCENE_GRID_NUMBER_H):
        #         self.drawing_sequence[m_v][n] = current_seq
        #         current_seq += 1
        
        # current_seq = 1
        
        # for n in range(number_to_generate): 
        #     for m_h in range(n, GameConfig.MAIN_SCENE_GRID_NUMBER_W):
        #         if self.adjust_building_map[n][m_h] != 0:
        #             original_i = self.original_building_i[n][m_h]
        #             original_j = self.original_building_j[n][m_h]
        #             self.drawing_sequence[original_i][original_j] = current_seq
        #         current_seq += 1
                
        #     for m_v in range(n+1, GameConfig.MAIN_SCENE_GRID_NUMBER_H):
        #         if self.adjust_building_map[m_v][n] != 0:
        #             original_i = self.original_building_i[m_v][n]
        #             original_j = self.original_building_j[m_v][n]
        #             self.drawing_sequence[original_i][original_j] = current_seq
        #         current_seq += 1
        
        self.earth_map = earch_result_reshaped
        self.surface_map = surface_result_reshaped
        self.building_map = building_result_reshaped
        # self.buidx_map = buidx_result_reshaped
        # self.buidy_map = buidy_result_reshaped
        
        # self.walkable_map = self.adjust_building_map == 0

            
class MainSceneDrawer:
    
    def __init__(self, main_character, scene_map_data, texture_manager, camera):
        self.main_character = main_character
        self.scene_map_data = scene_map_data
        self.texture_manager = texture_manager
        self.camera = camera
        
        self.grid_size_w = GameConfig.MAIN_SCENE_GRID_SIZE_W
        self.grid_size_h = GameConfig.MAIN_SCENE_GRID_SIZE_H
        
        self.grid_number_w = GameConfig.MAIN_SCENE_GRID_NUMBER_W
        self.grid_number_h = GameConfig.MAIN_SCENE_GRID_NUMBER_H
        
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
            
        self.lower_bound = 15
        self.upper_bound = 15
        
        
            
    def draw_texture(self, texture, screen, i, j, camera, offset_data=(0,0), object_height=0):
            
            
            x = self.grid_offset[i, j, 0]
            y = self.grid_offset[i, j, 1]
            
            x -= camera.pixel_x
            y -= camera.pixel_y
            
            if x + self.grid_number_w < 0  or y + self.grid_number_h < 0 :
                # out of camera screen
                # print("out of camera screen: ", x, y)
                return
            
            x = x - offset_data[0] 
            y = y - offset_data[1] - object_height
            
            if x > camera.max_screen_x or y > camera.max_screen_y:
                # print("larger than screen: ", x, y)
                return
                
            screen.blit(texture, (x, y))
        
    def draw_earth(self, screen, i, j, camera):
            
        # print("draw earth at: ", i, j)
        earth_value = self.scene_map_data.earth_map[i, j]
        earth_value = earth_value //2
        
        # print("earth_value: ", earth_value)
        earth_texture = self.texture_manager.get_texture_pygame(earth_value)
        
        if len(earth_texture) == 0:
            return
        
        offset_data = self.texture_manager.get_offset(earth_value)
        
        self.draw_texture(earth_texture[0], screen, i, j, camera, offset_data)
            
            
    def draw_surface(self, screen, i, j, camera):
        
        
        surface_value = self.scene_map_data.surface_map[i, j]
        surface_value = surface_value //2 # because of the original data was doubled in original project
        
        if surface_value == 0:
            # print("surface_value is 0, i, j: ", i, j)
            return
        
        surface_texture = self.texture_manager.get_texture_pygame(surface_value)
        
        if len(surface_texture) == 0:
            print("surface not found: ", surface_value)
            return
        
        offset_data = self.texture_manager.get_offset(surface_value)
        
        self.draw_texture(surface_texture[0], screen, i, j, camera, offset_data)
        
    def draw_element(self, screen, i, j, camera):
        
        # draw building
        building_texture_id = self.scene_map_data.building_map[i][j]//2
        # building_height = self.scene_map_data.building_hight_map[i][j]
        
        if building_texture_id != 0:
            building_texture = self.texture_manager.get_texture_pygame(building_texture_id)
            if len(building_texture) != 0:
                building_offset_data = self.texture_manager.get_offset(building_texture_id)
                self.draw_texture(building_texture[0], screen, i, j, camera, building_offset_data)
                
                # debug_grid_texture = self.texture_manager.get_texture_pygame(1)
                # debug_grid_offset_data = self.texture_manager.get_offset(1)
                # self.draw_texture(debug_grid_texture[0], screen, i, j, camera, debug_grid_offset_data)
                
                # adjust_grid_texture = self.texture_manager.get_texture_pygame(0)
                # adjust_grid_offset_data = self.texture_manager.get_offset(0)
                
                # adjust_value = self.scene_map_data.adjust_gride_number[i][j]
                
                # if adjust_value != 0:
                #     self.draw_texture(adjust_grid_texture[0], screen, i-adjust_value, j-adjust_value, camera, adjust_grid_offset_data)
        
        
        # draw main character
        
        if j == self.main_character.x and i == self.main_character.y:
            character_texture = self.main_character.get_current_texture()
            character_offset_data = self.main_character.get_current_offset()
            # print('try to draw the character at : ', i, j)
            # print('character_texture: ', character_texture)
            # print('character_offset_data: ', character_offset_data)
            # print('building_height: ', building_height)
            # print('camera: ', camera.pixel_x, camera.pixel_y)
            self.draw_texture(character_texture, screen, i, j, camera, character_offset_data)
        
        # if j == self.main_character.x and i == self.main_character.y + 1:
        #     character_texture = self.main_character.get_current_texture()
        #     character_offset_data = self.main_character.get_current_offset()
        #     # print('try to draw the character at : ', i, j)
        #     # print('character_texture: ', character_texture)
        #     # print('character_offset_data: ', character_offset_data)
        #     # print('building_height: ', building_height)
        #     # print('camera: ', camera.pixel_x, camera.pixel_y)
        #     self.draw_texture(character_texture, screen, i-1, j, camera, character_offset_data)
        
           
    
    def draw(self, screen):
        
        # print("Character x, y: ", self.main_character.x, self.main_character.y)
        
        # as the main scene is a large scene, we need to draw part of the scene, to make the drawing faster
        # we need to calculate the start and end of the scene to draw
        # based on the location of main character, 
        # only grid around the main character will be drawn
        # the boundry is x-5, x+5, y-5, y+5, x y from main character
        
        loop_start_x = self.main_character.x - self.lower_bound
        loop_end_x = self.main_character.x + self.upper_bound
        loop_start_y = self.main_character.y - self.lower_bound
        loop_end_y = self.main_character.y + self.upper_bound
        
        # print("loop_start_x: ", loop_start_x)
        # print("loop_end_x: ", loop_end_x)
        # print("loop_start_y: ", loop_start_y)
        # print("loop_end_y: ", loop_end_y)
        
        # for (dx, dy) in self.drawing_sequence:
        #     i = loop_start_y + dy
        #     j = loop_start_x + dx
        #     if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
        #         continue
        #     self.draw_earth(screen, i, j, self.camera)
            
        # for (dx, dy) in self.drawing_sequence:
        #     i = loop_start_y + dy
        #     j = loop_start_x + dx
        #     if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
        #         continue
        #     self.draw_surface(screen, i, j, self.camera)
            
        # for (dx, dy) in self.drawing_sequence:
        #     i = loop_start_y + dy
        #     j = loop_start_x + dx
        #     if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
        #         continue
        #     self.draw_element(screen, i, j, self.camera)
        
        for i in range(loop_start_y, loop_end_y):
            for j in range(loop_start_x, loop_end_x):
                if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
                    continue
                self.draw_earth(screen, i, j, self.camera)
        
        for i in range(loop_start_y, loop_end_y):
            for j in range(loop_start_x, loop_end_x):
                if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
                    continue
                self.draw_surface(screen, i, j, self.camera)
                
        # for i in range(loop_start_y, loop_end_y):
        #     for j in range(loop_start_x, loop_end_x):
        #         if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
        #             continue
        #         self.draw_element(screen, i, j, self.camera)
        
        # elements_to_draw = []
        
        # for i in range(loop_start_y, loop_end_y):
        #     for j in range(loop_start_x, loop_end_x):
        #         if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
        #             continue
        #         # self.draw_element(screen, i, j, self.camera)
        #         # draw_sequence = self.scene_map_data.drawing_sequence[i][j]
        #         # print(draw_sequence, i, j)
        #         if self.scene_map_data.adjust_building_map[i][j] != 0:
        #             original_i = self.scene_map_data.original_building_i[i][j]
        #             original_j = self.scene_map_data.original_building_j[i][j]
        #             sequence = self.scene_map_data.building_everage[i][j]
        #             elements_to_draw.append((sequence, original_i, original_j))
                
        # elements_to_draw.sort(key=lambda x: x[0])
        
        # for (draw_sequence, i, j) in elements_to_draw:
        #     self.draw_element(screen, i, j, self.camera)
                
        elements_to_draw = []
        
        for i in range(loop_start_y, loop_end_y):
            for j in range(loop_start_x, loop_end_x):
                if i < 0 or j < 0 or i >= self.grid_number_h or j >= self.grid_number_w:
                    continue
                # self.draw_element(screen, i, j, self.camera)
                # draw_sequence = self.scene_map_data.drawing_sequence[i][j]
                draw_sequence = self.scene_map_data.building_everage[i][j]
                # print(draw_sequence, i, j)
                elements_to_draw.append((draw_sequence, i, j))
                
        elements_to_draw.sort(key=lambda x: x[0])
        
        for (draw_sequence, i, j) in elements_to_draw:
            self.draw_element(screen, i, j, self.camera)
        
        
        
 