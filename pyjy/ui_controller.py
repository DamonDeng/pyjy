import pygame
import pygame_gui

from pyjy.constants import GameConfig
from pyjy.constants import GameColor
from pyjy.constants import GameStatus

class UIController:
    def __init__(self, root_folder, central_controller):
        
        self.root_folder = root_folder
        self.central_controller = central_controller
        
        pygame.display.set_caption(GameConfig.SCREEN_TITLE)
        
        # the original screen surface to draw original game elements:
        self.original_surface = pygame.Surface((GameConfig.ORIGINAL_SCREEN_W, GameConfig.ORIGINAL_SCREEN_H))
        self.main_screen = pygame.display.set_mode(GameConfig.WINDOW_SIZE)
        
        self.game_content_screen = pygame.Surface((GameConfig.GAME_SCREEN_WIDTH, GameConfig.GAME_SCREEN_HEIGHT))
        
        self.ui_manager = pygame_gui.UIManager((GameConfig.WINDOW_SIZE), starting_language='zh')
        
        self.ui_manager.get_theme().load_theme(root_folder + "/resource/ui/default_theme.json")
        
        # The following UI components are located in the main game window with hard-coded positions.
        # They all fit to the main window background picture.
        # If you want to change the window size, you need to change the background picture size and the following UI components' positions.
        
        # Create a UITextBox with HTML-like theming
        self.system_message_box = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((1033, 74), (359, 707)),
            manager=self.ui_manager,
            object_id="#system_message_box"
        )

        # Create a multi-line UITextEntryBox
        self.text_entry = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((380, 577), (640, 180)),
            manager=self.ui_manager,
            object_id="#text_entry",
            container=self.ui_manager.get_root_container(),
            placeholder_text='面对NPC按回车键开始对话， 按Shift-Enter提交对话，按ESC键退出对话。',
        )

        self.upper_talk_box = pygame_gui.elements.UITextBox(
            html_text = "",
            relative_rect=pygame.Rect((554, 105), (409, 137)),
            manager=self.ui_manager,
            object_id="#talk_box",
            container=self.ui_manager.get_root_container(),
        )


        self.lower_talk_box = pygame_gui.elements.UITextBox(
            html_text = "",
            relative_rect=pygame.Rect((430, 414), (409, 137)),
            manager=self.ui_manager,
            object_id="#talk_box",
            container=self.ui_manager.get_root_container(),
        )


        
        self.game_background_img = pygame.image.load(self.root_folder + "/resource/ui/main_ui_bg.png")

        self.talk_box_img = pygame.image.load(self.root_folder + "/resource/ui/talk_box.png")
        self.talk_box_img_bg = pygame.image.load(self.root_folder + "/resource/ui/talk_box_background.png")

        self.head_box_img = pygame.image.load(self.root_folder + "/resource/ui/head_box.png")
        self.head_box_img_bg = pygame.image.load(self.root_folder + "/resource/ui/head_box_background.png")

    def update(self, time_delta):
        self.ui_manager.update(time_delta)
        
    def draw(self, time_delta):
        
        if self.central_controller.game_status == GameStatus.TALKING:
            input_rect = pygame.Rect((380, 577), (640+100, 180-5))
            pygame.key.set_text_input_rect(input_rect)
                
        elif self.central_controller.game_status == GameStatus.INGAME:
            self.original_surface.fill(GameColor.WHITE)
            self.central_controller.scene_controller.draw(self.original_surface)
            
        
        scaled_surface = pygame.transform.scale(self.original_surface, (GameConfig.GAME_SCREEN_WIDTH, GameConfig.GAME_SCREEN_HEIGHT))
        
        self.game_content_screen.blit(scaled_surface, (0, 0))
        
        # fill the main screen with dark gray color as main window background
        self.main_screen.fill(GameColor.DARK_GRAY_BG)
        
        #draw the game content screen on the main screen, the location is hard-coded based on the main window background picture
        self.main_screen.blit(self.game_content_screen, (381, 84))
        
        UPPER_HEAD_BOX_LOCATION = (406, 106)
        UPPER_TALK_BOX_LOCATION = (545, 96)
        
        LOWER_HEAD_BOX_LOCATION = (870, 419)
        LOWER_TALK_BOX_LOCATION = (423, 406)
        
        if self.central_controller.game_status == GameStatus.TALKING:
            # if the game status is TALKING, draw the talking box and head box
            # draw the talking box and head box background at first, then draw pygame_gui components, 
            #draw the upper head box and talk box
            self.main_screen.blit(self.head_box_img_bg, UPPER_HEAD_BOX_LOCATION)
            self.main_screen.blit(self.talk_box_img_bg, UPPER_TALK_BOX_LOCATION)

            # drwa the lower head box and talk box
            self.main_screen.blit(self.head_box_img_bg, LOWER_HEAD_BOX_LOCATION)
            self.main_screen.blit(self.talk_box_img_bg, LOWER_TALK_BOX_LOCATION)
            
            upper_talker_img = self.central_controller.get_upper_talker_img()
            lower_talker_img = self.central_controller.get_lower_talker_img()
            
            
            # the following offset values are hard-coded based on the background picture
            if upper_talker_img is not None:
                self.main_screen.blit(upper_talker_img, (UPPER_HEAD_BOX_LOCATION[0]+40, UPPER_HEAD_BOX_LOCATION[1]+17))
                
            if lower_talker_img is not None:
                self.main_screen.blit(lower_talker_img, (LOWER_HEAD_BOX_LOCATION[0]+7, LOWER_HEAD_BOX_LOCATION[1]+12))
                
            self.upper_talk_box.show()
            self.lower_talk_box.show()
                
        elif self.central_controller.game_status == GameStatus.INGAME:
            self.upper_talk_box.hide()
            self.lower_talk_box.hide()
            

        
        # self.ui_manager.update(time_delta)
        
        
        self.ui_manager.draw_ui(self.main_screen)
        
        if self.central_controller.game_status == GameStatus.TALKING:
            
        
            #draw the upper head box and talk box
            self.main_screen.blit(self.head_box_img, UPPER_HEAD_BOX_LOCATION)
            self.main_screen.blit(self.talk_box_img, UPPER_TALK_BOX_LOCATION)
            
            # drwa the lower head box and talk box
            self.main_screen.blit(self.head_box_img, LOWER_HEAD_BOX_LOCATION)
            self.main_screen.blit(self.talk_box_img, LOWER_TALK_BOX_LOCATION)
        
        # draw the main window background picture
        # it may look like no sence to draw the background picture at the end of the draw function,
        # but there are some transparent areas in the background picture, which exactly show all components in the main window.
        # drawing this partial transparent background picture make all the UI components look like embedded in the background picture.
        self.main_screen.blit(self.game_background_img, (0, 0))