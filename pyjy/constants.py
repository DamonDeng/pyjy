from enum import Enum

class GameConfig:
    # Game window title
    SCREEN_TITLE = "Py金庸群侠传"
    GAME_TITLE = "Py金庸群侠传"
    
    FPS = 60
    
    # The size of the whole game window
    WINDOW_W = 1400
    WINDOW_H = 800
    
    WINDOW_SIZE = (WINDOW_W, WINDOW_H)
    
    #The size of original game screen, it is 320*240
    
    ORIGINAL_SCREEN_W = 320
    ORIGINAL_SCREEN_H = 240
    
    # Scale original screen by 2, to leverage morden high resolution screen
    GAME_SCREEN_WIDTH = ORIGINAL_SCREEN_W*2
    GAME_SCREEN_HEIGHT = ORIGINAL_SCREEN_H*2
    

    
    # Main Scene setting
    MAIN_SCENE_WIDTH = ORIGINAL_SCREEN_W
    MAIN_SCENE_HEIGHT = ORIGINAL_SCREEN_H
    
    SUB_SCENE_WIDTH = ORIGINAL_SCREEN_W
    SUB_SCENE_HEIGHT = ORIGINAL_SCREEN_H
    
    
    MAIN_SCENE_GRID_NUMBER_W = 480
    MAIN_SCENE_GRID_NUMBER_H = 480
    
    SUB_SCENE_GRID_NUMBER_W = 64
    SUB_SCENE_GRID_NUMBER_H = 64
    
    GRID_SIZE_W = 36
    GRID_SIZE_H = 18
    
    # Sub Scene setting
    

    
    SUB_SCENE_NUMBER = 84
    SUB_SCENE_DATA_LAYER_NUMBER = 6
    SUB_SCENE_LAYER_DATA_LENGTH = 4096
    SUB_SCENE_ALL_LAYER_DATA_LENGTH = SUB_SCENE_NUMBER * SUB_SCENE_DATA_LAYER_NUMBER * SUB_SCENE_LAYER_DATA_LENGTH

    SUB_SCENE_EVENT_NUMBER_PER_SCENE = 200
    SUB_SCENE_EVENT_DATA_LENGTH = 11

    SUB_SCENE_ALL_EVENT_DATA_LENGTH = SUB_SCENE_NUMBER * SUB_SCENE_EVENT_NUMBER_PER_SCENE * SUB_SCENE_EVENT_DATA_LENGTH
    
    

    
    # the following two values can't be changed, it is related to the storage format of the game data
    TEAMMATE_COUNT = 6
    ITEM_IN_BAG_COUNT = 1000
    
    ROLE_MAGIC_COUNT = 10
    ROLE_TAKING_ITEM_COUNT = 4
    
class SceneType(Enum):
    MAIN_SCENE = 0
    SUB_SCENE = 1
    FIGHT_SCENE = 2
    
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
class GameColor:
    WHITE = (255, 255, 255)
    DARK_GRAY_BG = (30, 29, 32)
    
class GameStatus(Enum):
    TALKING = 0
    INGAME = 1