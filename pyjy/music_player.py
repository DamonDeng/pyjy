import pygame
import os

class MusicPlayer:
    
    def __init__(self, root_folder, enable=True):
        self.root_folder = root_folder
        self.music_dict = {}
        pygame.mixer.init()
        self.music_folder = self.root_folder + "/original_resource/music"
        self.enable = enable
        
    def play_mid_by_id(self, mid_id):
        if mid_id <= 0 or mid_id > 23:
            return
        
        if self.enable:
            music_file_path = self.music_folder + "/" + str(mid_id) + ".mid"
            pygame.mixer.music.load(music_file_path)
            # Play the music in an infinite loop
            pygame.mixer.music.play(-1)
            
    def disable(self):
        pygame.mixer.music.fadeout(500)
        # pygame.mixer.music.stop()
        self.enable = False
        