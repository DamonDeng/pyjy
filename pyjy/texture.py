import os
import io
import pygame

import zipfile

from PIL import Image
from pyjy.utils.binary_reader import BinaryReader
from pyjy.constants import Direction
from pyjy.constants import SceneType



class TextureLoader:
    
    def __init__ (self):
        self.textures = {}
        self.texture_png = {}
        self.texture_pygame = {}
        
    def load_from_zip_file(self, zip_file_name):
        
        # Load the entire ZIP file into memory
        with open(zip_file_name, 'rb') as zip_file:
            zip_data = zip_file.read()

        # Create a BytesIO object from the ZIP data
        zip_bytes = io.BytesIO(zip_data)
        
        with zipfile.ZipFile(zip_bytes) as zip_ref:
        
            offset_index_file = zip_ref.open('index.ka')
            offset_index_data = offset_index_file.read()
            
            offset_result = BinaryReader.read_data_to_vector(offset_index_data, "h")
            
        
            # get all the file names in the folder, and sort them
            # the file name format is 0.png, 1.png, 2.png, ..., for some textures with multiple images, the format is something like 168_0.png, 168_1.png, 168_2.png, 168_3.png, ...
            # the offset index file is a list of offsets, which is the x, y offset of the texture in the texture atlas
            # we need to build a dictionary of texture name to offset, put it in self.textures
            
            # for example, if the folder has 3 textures, 0.png, 1.png, 2.png, and the offset index file is [0,0, 30, 20, 67, 84]
            # then self.textures should be {0: {"file_name_list":["0.png"], "offset": (0,0)}, 
            #                              1: {"file_name_list":["1.png"], "offset": (30,20)},
            #                              2: {"file_name_list":["2.png"], "offset": (67,84)}}
            
            # if the folder has 3 textures, 0.png, 1.png, 168_0.png, 168_1.png, 168_2.png, 168_3.png, and the offset index file is [0,0, 30, 20, 77, 99]
            # then self.textures should be {0: {"file_name_list":["0.png"], "offset": (0,0)},
            #                              1: {"file_name_list":["1.png"], "offset": (30,20)},
            #                              168: {"file_name_list":["168_0.png", "168_1.png", "168_2.png", "168_3.png"], "offset": (77,99)}}
        
            # Get a list of all file names in the ZIP archive
            file_names = zip_ref.namelist()
            
            for file_name in file_names:
                if file_name.endswith(".png"):
                    if "-" in file_name:
                        # skip the files that contain "-", which should be backup files
                        continue
                    if "/" in file_name:
                        # it is a folder, skip it
                        continue
                    
                    if "_" in file_name:
                        texture_number = int(os.path.splitext(file_name.split("_")[0])[0])
                    else:
                        texture_number = int(os.path.splitext(file_name.split(".")[0])[0])
                    # print(texture_number)
                    
                    if texture_number not in self.textures:
                        texture_file_name_list = []
                        texture_file_name_list.append(file_name)
                        offset = (offset_result[texture_number * 2], offset_result[texture_number * 2 + 1])
                        self.textures[texture_number] = {"file_name_list": texture_file_name_list, "offset": offset}
                    else:
                        self.textures[texture_number]["file_name_list"].append(file_name)


            # load all the textures into memory, and put them in self.texture_png

            for texture_name in self.textures:
                texture_file_name_list = self.textures[texture_name]["file_name_list"]
                texture_png = []
                texture_pygame = []
                
                
                for texture_file_name in texture_file_name_list:
                    # Read the file from the ZIP archive
                    with zip_ref.open(texture_file_name) as texture_file:
                        texture = Image.open(texture_file).convert("RGBA")
                        texture_png.append(texture)
                        
                        mode = texture.mode
                        size = texture.size
                        data = texture.tobytes()

                        map_surface = pygame.image.fromstring(data, size, mode)
                        
                        texture_pygame.append(map_surface)
            
                self.texture_png[texture_name] = texture_png
                self.texture_pygame[texture_name] = texture_pygame
			
			
			
        
    def load_from_folder(self, folder_name):
        
        offset_index_file_name = folder_name + 'index.ka'
        
        offset_result = BinaryReader.read_file_to_vector(offset_index_file_name, "H")
        
        # get all the file names in the folder, and sort them
        # the file name format is 0.png, 1.png, 2.png, ..., for some textures with multiple images, the format is something like 168_0.png, 168_1.png, 168_2.png, 168_3.png, ...
        # the offset index file is a list of offsets, which is the x, y offset of the texture in the texture atlas
        # we need to build a dictionary of texture name to offset, put it in self.textures
        
        # for example, if the folder has 3 textures, 0.png, 1.png, 2.png, and the offset index file is [0,0, 30, 20, 67, 84]
        # then self.textures should be {0: {"file_name_list":["0.png"], "offset": (0,0)}, 
        #                              1: {"file_name_list":["1.png"], "offset": (30,20)},
        #                              2: {"file_name_list":["2.png"], "offset": (67,84)}}
        
        # if the folder has 3 textures, 0.png, 1.png, 168_0.png, 168_1.png, 168_2.png, 168_3.png, and the offset index file is [0,0, 30, 20, 77, 99]
        # then self.textures should be {0: {"file_name_list":["0.png"], "offset": (0,0)},
        #                              1: {"file_name_list":["1.png"], "offset": (30,20)},
        #                              168: {"file_name_list":["168_0.png", "168_1.png", "168_2.png", "168_3.png"], "offset": (77,99)}}
        
        file_names = os.listdir(folder_name)
            
        for file_name in file_names:
            if file_name.endswith(".png"):
                if "-" in file_name:
                    # skip the files that contain "-", which should be backup files
                    continue
                if "/" in file_name:
                    # it is a folder, skip it
                    continue
                
                if "_" in file_name:
                    texture_number = int(os.path.splitext(file_name.split("_")[0])[0])
                else:
                    texture_number = int(os.path.splitext(file_name.split(".")[0])[0])
                # print(texture_number)
                
                if texture_number not in self.textures:
                    texture_file_name_list = []
                    texture_file_name_list.append(file_name)
                    offset = (offset_result[texture_number * 2], offset_result[texture_number * 2 + 1])
                    self.textures[texture_number] = {"file_name_list": texture_file_name_list, "offset": offset}
                else:
                    self.textures[texture_number]["file_name_list"].append(file_name)
                    
            
        # load all the textures into memory, and put them in self.texture_png
        
        for texture_name in self.textures:
            texture_file_name_list = self.textures[texture_name]["file_name_list"]
            texture_png = []
            texture_pygame = []
            for texture_file_name in texture_file_name_list:
                texture = Image.open(folder_name + texture_file_name).convert("RGBA")
                texture_png.append(texture)
                
                mode = texture.mode
                size = texture.size
                data = texture.tobytes()

                map_surface = pygame.image.fromstring(data, size, mode)
                
                texture_pygame.append(map_surface)
            
            self.texture_png[texture_name] = texture_png
            self.texture_pygame[texture_name] = texture_pygame
         
    def get_texture_pygame (self, texture_name):
        if texture_name not in self.texture_pygame:
            return []
        return self.texture_pygame[texture_name]
       
    def get_texture (self, texture_name):
        if texture_name not in self.texture_png:
            return []
        return self.texture_png[texture_name]
    
    def get_offset (self, texture_name):
        if texture_name not in self.textures:
            return (0, 0)
        return self.textures[texture_name]["offset"]
    
    def get_image_size(self, texture_name):
        if texture_name not in self.texture_png:
            return (0, 0)
        return self.texture_png[texture_name][0].size
        
        
class MainCharacterTextureLoader():
    
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    
    START_INDEX = 2501
    PIC_NUMBER = 7
    
    UP_OFF_SET = 0
    RIGHT_OFF_SET = 7
    LEFT_OFF_SET = 14
    DOWN_OFF_SET = 21
    
    def __init__(self, scene_texture_manager):
        self.up_texture = []
        self.down_texture = []
        self.left_texture = []
        self.right_texture = []
        
        self.up_offset = []
        self.down_offset = []
        self.left_offset = []
        self.right_offset = []
        
        self.scene_texture_manager = scene_texture_manager
        
        for i in range(self.PIC_NUMBER):
            self.up_texture.append(self.scene_texture_manager.get_texture_pygame(self.START_INDEX + i + self.UP_OFF_SET))
            self.down_texture.append(self.scene_texture_manager.get_texture_pygame(self.START_INDEX + i + self.DOWN_OFF_SET))
            self.left_texture.append(self.scene_texture_manager.get_texture_pygame(self.START_INDEX + i + self.LEFT_OFF_SET))
            self.right_texture.append(self.scene_texture_manager.get_texture_pygame(self.START_INDEX + i + self.RIGHT_OFF_SET))
            
            self.up_offset.append(self.scene_texture_manager.get_offset(self.START_INDEX + i + self.UP_OFF_SET))
            self.down_offset.append(self.scene_texture_manager.get_offset(self.START_INDEX + i + self.DOWN_OFF_SET))
            self.left_offset.append(self.scene_texture_manager.get_offset(self.START_INDEX + i + self.LEFT_OFF_SET))
            self.right_offset.append(self.scene_texture_manager.get_offset(self.START_INDEX + i + self.RIGHT_OFF_SET))
            
            
    def get_texture(self, direction, index):
        
        if index < 0 or index >= self.PIC_NUMBER:
            return None
        
        if direction == Direction.UP:
            return self.up_texture[index]
        elif direction == Direction.DOWN:
            return self.down_texture[index]
        elif direction == Direction.LEFT:
            return self.left_texture[index]
        elif direction == Direction.RIGHT:
            return self.right_texture[index]
        
        return None
    
    def get_offset(self, direction, index):
            
        if index < 0 or index >= self.PIC_NUMBER:
            return None
        
        if direction == Direction.UP:
            return self.up_offset[index]
        elif direction == Direction.DOWN:
            return self.down_offset[index]
        elif direction == Direction.LEFT:
            return self.left_offset[index]
        elif direction == Direction.RIGHT:
            return self.right_offset[index]
        
        return None
    
    def get_texture_id(self, direction, index):
        
        if index < 0 or index >= self.PIC_NUMBER:
            return None
        
        if direction == Direction.UP:
            return self.START_INDEX + index + self.UP_OFF_SET
        elif direction == Direction.DOWN:
            return self.START_INDEX + index + self.DOWN_OFF_SET
        elif direction == Direction.LEFT:
            return self.START_INDEX + index + self.LEFT_OFF_SET
        elif direction == Direction.RIGHT:
            return self.START_INDEX + index + self.RIGHT_OFF_SET
        
        return None
        
class TextureManager:
    
    def __init__(self, root_folder):
        self.main_scene_loader = TextureLoader()
        self.main_scene_loader.load_from_zip_file(root_folder + "/original_resource/resource/mmap.zip")
        
        self.sub_scene_loader = TextureLoader()
        self.sub_scene_loader.load_from_zip_file(root_folder + '/original_resource/resource/smap.zip')
        
        self.main_scene_main_character_loader = MainCharacterTextureLoader(self.main_scene_loader)
        self.sub_scene_main_character_loader = MainCharacterTextureLoader(self.sub_scene_loader) 
        
    def get_texture_pygame (self, scene_type, texture_name):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_loader
        else:
            return []
        
        if texture_name not in loader.texture_pygame:
            return []
        return loader.texture_pygame[texture_name]
       
    def get_texture (self, scene_type, texture_name):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_loader
        else:
            return []
        if texture_name not in loader.texture_png:
            return []
        return loader.texture_png[texture_name]
    
    
    def get_offset (self, scene_type, texture_name):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_loader
        else:
            return (0, 0)
        if texture_name not in loader.textures:
            return (0, 0)
        return loader.textures[texture_name]["offset"]
    
    
    def get_image_size(self, scene_type, texture_name):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_loader
        else:
            return (0, 0)
        
        if texture_name not in loader.texture_png:
            return (0, 0)
        return loader.texture_png[texture_name][0].size
    
    def get_main_character_texture(self, scene_type, direction, index):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_main_character_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_main_character_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_main_character_loader
        else:
            return []
        
        return loader.get_texture(direction, index)
    
    def get_main_character_offset(self, scene_type, direction, index):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_main_character_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_main_character_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_main_character_loader
        else:
            return None
        
        return loader.get_offset(direction, index)
    
    
    def get_main_character_texture_id(self, scene_type, direction, index):
        if scene_type == SceneType.MAIN_SCENE:
            loader = self.main_scene_main_character_loader
        elif scene_type == SceneType.SUB_SCENE:
            loader = self.sub_scene_main_character_loader
        elif scene_type == SceneType.FIGHT_SCENE:
            loader = self.sub_scene_main_character_loader
        else:
            return None
        
        return loader.get_texture_id(direction, index)
    
    
        