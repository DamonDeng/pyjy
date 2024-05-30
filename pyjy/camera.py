from pyjy.constants import GameConfig

class Camera:
    def __init__(self):
        self.pixel_x = 0
        self.pixel_y = 0
        
        self.grid_x = 0
        self.grid_y = 0
        
        self.max_screen_x = GameConfig.SCREEN_WIDTH
        self.max_screen_y = GameConfig.SCREEN_HEIGHT
        
    def follow_character(self, character):
        grid_size_w = GameConfig.SUB_SCENE_GRID_SIZE_W
        grid_size_h = GameConfig.SUB_SCENE_GRID_SIZE_H
        
        grid_number_w = GameConfig.SUB_SCENE_GRID_NUMBER_W
        grid_number_h = GameConfig.SUB_SCENE_GRID_NUMBER_H
        
        WIDTH = GameConfig.SUB_SCENE_WIDTH
        HEIGHT = GameConfig.SUB_SCENE_HEIGHT
        
        start_x = (grid_number_w/2) * grid_size_w
        start_y = 0
        
        (grid_x, grid_y) = (character.x, character.y)
        
        # putting the camera view on the center of the character
        grid_x = grid_x - 2
        grid_y = grid_y - 2
        
        #prevent the camera to move outside of designed area
        if grid_x < 12:
            grid_x = 12
        if grid_x > 44:
            grid_x = 44
        if grid_y < 15:
            grid_y = 15
        if grid_y > 45:
            grid_y = 45
        
        # moving with the grid x coordinate
        x = start_x + grid_x * grid_size_w/2
        y = start_y + grid_x * grid_size_h/2
        
        # moving with the grid y coordinate
        x -= grid_y * grid_size_w/2
        y += grid_y * grid_size_h/2
        
        
        x = int(x) - WIDTH/2
        y = int(y) - HEIGHT/2
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        self.pixel_x = x
        self.pixel_y = y
        
        return x, y   

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def set_by_pixel(self, x, y):
        self.pixel_x = x
        self.pixel_y = y
        # todo: calculate grid_x, grid_y
        
    def set_by_grid(self, x, y):
        self.grid_x = x
        self.grid_y = y
        
        # todo: calculate pixel_x, pixel_y

    def __str__(self):
        return f"Camera at ({self.x}, {self.y})"