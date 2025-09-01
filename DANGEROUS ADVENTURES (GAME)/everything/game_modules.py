import random
import arcade
import math
from pyglet.math import Vec2
import time
import game_modules as gm

# set variables
SPRITE_SCALING_PLAYER = 1.0
TILE_SCALING = 1.1
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 550
MOVEMENT_SPEED = 5
COORD_LIST = [[100,100], [150, 200], [200, 500], [400, 400], [500, 200], [1000, 1000], [800, 800], 
              [600, 700], [-100, -200], [-100, 100], [-200, 250]]
GRAVITY = 0.5
JUMP_SPEED = 10
TILE_SCALING = 0.5
global last_attack
last_attack = 0
attack_delay = 2

class Room:
    ''' holds information about the different rooms '''
    
    def __init__(self):
        ''' initalize variables for this class '''
        self.wall_list = None
        self.floor_list = None
        self.exit_list = None
        self.enemies_list = None
        self.map_name = ''
        enemies_cord_list = []
        self.enemy_id = 1
        self.class_enemies_list = []
        self.up_speed = 5
        self.background_music = ''
    
    def setup_room_1(self):
        ''' Create and return the first level '''
        
        # set a coordinate list for enemies
        enemies_cord_list = [[100,500], [200,530], [105, 190], [300, 50]]
        
        # make the level
        prison_level = Room()
        
        # set the name of map
        prison_level.map_name = "layout/prison_level.json"
        prison_level.background_music = arcade.load_sound("sounds/level1_bm.mp3")
        
        # read in the tiled map
        self.tile_map = arcade.load_tilemap(prison_level.map_name, scaling = TILE_SCALING)
        
        # set up the different layers for the level
        prison_level.wall_list = self.tile_map.sprite_lists["Solid"]
        prison_level.floor_list = self.tile_map.sprite_lists["Floor"]
        prison_level.exit_list = self.tile_map.sprite_lists["Exit"]
        prison_level.gate1_list = self.tile_map.sprite_lists["Gate1"]
        prison_level.gate2_list = self.tile_map.sprite_lists["Gate2"]
        prison_level.event1_list = self.tile_map.sprite_lists["Event1"]
        prison_level.event2_list = self.tile_map.sprite_lists["Event2"]
        
        # make the list for the enemies
        prison_level.enemies_list = arcade.SpriteList()
        
        for enemy in enemies_cord_list:
            # create the enemy instance, sprite drawn by me
            guard = Enemy()
            guard.make_sprite("sprites/enemies/guard.png")
            guard.id = self.enemy_id
            
            # position enemy
            guard.sprite.center_x = enemy[0]
            guard.sprite.center_y = enemy[1]
            
            # add the enemy to the lists
            prison_level.enemies_list.append(guard.sprite)
            prison_level.class_enemies_list.append(guard)
            
            # increase id
            self.enemy_id += 1
            
        # set to background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
      
        # score
        self.score = 0
        
        # return level
        return prison_level
    
    def setup_room_2(self):
        """
        Create and return room 2.
        """
        # make the level
        castle_level = Room()
        # set a coordinate list for enemies
        enemies_cord_list = [[100,500], [200,300], [105, 190], [300, 100]]
        # set the name of map
        castle_level.map_name = "layout/hallway_level2.json"
        castle_level.background_music = arcade.load_sound("sounds/lonely_castle.mp3")
        
        # read in the tiled map
        self.tile_map = arcade.load_tilemap(castle_level.map_name, scaling = TILE_SCALING)
        
        # set up the different layers for the level
        castle_level.wall_list = self.tile_map.sprite_lists["Solid"]
        castle_level.floor_list = self.tile_map.sprite_lists["Floor"]
        castle_level.exit_list = self.tile_map.sprite_lists["Exit"]
        castle_level.gate1_list = self.tile_map.sprite_lists["Gate1"]
        castle_level.gate2_list = self.tile_map.sprite_lists["Gate2"]
        castle_level.event1_list = self.tile_map.sprite_lists["Event1"]
        castle_level.event2_list = self.tile_map.sprite_lists["Event2"]
        # make the list for the enemies
        castle_level.enemies_list = arcade.SpriteList()
        
        for enemy in enemies_cord_list:
            # create the enemy instance, sprite drawn by me
            guard = Enemy()
            guard.make_sprite("sprites/enemies/skeleton.png")
            # set enemy id and damage dealt
            guard.id = self.enemy_id
            guard.damage = 2
            # position enemy
            guard.sprite.center_x = enemy[0]
            guard.sprite.center_y = enemy[1]
            
            # add the enemy to the lists
            castle_level.enemies_list.append(guard.sprite)
            castle_level.class_enemies_list.append(guard)
        
            # increase id
            self.enemy_id += 1                               
        
        # set to background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
            
        # return the level
        return castle_level
    
    def setup_room_3(self):
        ''' create and return level 3 '''
        
        # make the level
        sewer_level = Room()
        
        # set map name
        sewer_level.map_name = "layout/sewer_level.json"
        self.tile_map = arcade.load_tilemap(sewer_level.map_name, scaling = TILE_SCALING)
        
        # make sprite lists for each layer
        sewer_level.wall_list = self.tile_map.sprite_lists["solid"]
        sewer_level.floor_list = self.tile_map.sprite_lists["floor"]
        sewer_level.exit_list = self.tile_map.sprite_lists["exit"]
        sewer_level.gate1_list = self.tile_map.sprite_lists["gate1"]
        sewer_level.gate2_list = self.tile_map.sprite_lists["gate2"]
        sewer_level.event1_list = self.tile_map.sprite_lists["event1"]
        sewer_level.event2_list = self.tile_map.sprite_lists["event2"]
        
        # set a coordinate list for enemies
        enemies_cord_list = [[100,500], [200,300], [105, 190], [300, 100]]
        
        # make an enemy sprite list
        sewer_level.enemies_list = arcade.SpriteList()
        
        # set the speed that the player goes up when up arrow pressed
        self.up_speed = 15
        
        # set to background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
           
        for enemy in enemies_cord_list:
            # make enemy instance, drawn by me
            guard = Enemy()
            guard.make_sprite("sprites/enemies/skeleton.png")
            
            # set id and damage
            guard.id = self.enemy_id
            guard.damage = 2
            
            # position enemy
            guard.sprite.center_x = enemy[0]
            guard.sprite.center_y = enemy[1]
            
            # add the enemy to lists
            sewer_level.enemies_list.append(guard.sprite)
            sewer_level.class_enemies_list.append(guard)
            
            # increase id by one
            self.enemy_id += 1             
        
        # return the level
        return sewer_level
    
    def setup_room_4(self):
        """
        Create and return room 4.
        """
        library_level = Room()
        enemies_cord_list = [[100,500], [200,300], [105, 190], [300, 100]]
        # set the name of map
        library_level.map_name = "layout/library_level.json"
        
        # read in the tiled map
        self.tile_map = arcade.load_tilemap(library_level.map_name, scaling = TILE_SCALING)
        
        # set different sprite lists
        library_level.wall_list = self.tile_map.sprite_lists["solid"]
        library_level.floor_list = self.tile_map.sprite_lists["floor"]
        library_level.exit_list = self.tile_map.sprite_lists["exit"]
        library_level.gate1_list = self.tile_map.sprite_lists["gate1"]
        library_level.gate2_list = self.tile_map.sprite_lists["gate2"]
        library_level.event1_list = self.tile_map.sprite_lists["event1"]
        library_level.event2_list = self.tile_map.sprite_lists["event2"]
        library_level.enemies_list = arcade.SpriteList()
        
        for enemy in enemies_cord_list:
            
            # make enemt
            guard = Enemy()
            guard.make_sprite("sprites/enemies/ghost.png")
            
            # set enemy id, damage, speed
            guard.id = self.enemy_id
            guard.damage = 2
            guard.move_speed = 1
            
            # position enemy
            guard.sprite.center_x = enemy[0]
            guard.sprite.center_y = enemy[1]
            
            # add the enemt to the lists
            library_level.enemies_list.append(guard.sprite)
            library_level.class_enemies_list.append(guard)
                      
            self.enemy_id += 1                               
        
        # set to background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
      
        return library_level
    
    def setup_room_5(self):
        """
        Create and return room 4.
        """
        maze_level = Room()
        enemies_cord_list = [[100,500], [200,300], [105, 190], [300, 100]]
        # set the name of map
        maze_level.map_name = "layout/maze_level.json"
        
        # read in the tiled map
        self.tile_map = arcade.load_tilemap(maze_level.map_name, scaling = TILE_SCALING)
        
        # set different sprite lists
        maze_level.wall_list = self.tile_map.sprite_lists["solids"]
        maze_level.floor_list = self.tile_map.sprite_lists["floor"]
        maze_level.exit_list = self.tile_map.sprite_lists["exit"]
        maze_level.gate1_list = self.tile_map.sprite_lists["gate1"]
        maze_level.gate2_list = self.tile_map.sprite_lists["gate2"]
        maze_level.event1_list = self.tile_map.sprite_lists["event1"]
        maze_level.event2_list = self.tile_map.sprite_lists["event2"]
        maze_level.enemies_list = arcade.SpriteList()
        
        for enemy in enemies_cord_list:
            # make enemy
            guard = Enemy()
            guard.make_sprite("sprites/enemies/ghost.png")
            
            # set enemy id, damage, speed
            guard.id = self.enemy_id
            guard.damage = 2
            guard.move_speed = 1
            # position enemy
            guard.sprite.center_x = enemy[0]
            guard.sprite.center_y = enemy[1]
            
            # add the star to the lists
            maze_level.enemies_list.append(guard.sprite)
            maze_level.class_enemies_list.append(guard)
            
            # increase enemy id         
            self.enemy_id += 1                               
        
        # set to background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
      
        return maze_level
    
    def setup_room_6(self):
        """
        Create and return room 4.
        """
        boss_level = Room()
        enemies_cord_list = [[100,500], [200,300], [105, 190], [300, 100]]
        # set the name of map
        boss_level.map_name = "layout/boss_room.json"
        
        # read in the tiled map
        self.tile_map = arcade.load_tilemap(boss_level.map_name, scaling = TILE_SCALING)
        
        # set different sprite lists
        boss_level.wall_list = self.tile_map.sprite_lists["solids"]
        boss_level.floor_list = self.tile_map.sprite_lists["floor"]
        boss_level.exit_list = self.tile_map.sprite_lists["exit"]
        boss_level.gate1_list = self.tile_map.sprite_lists["gate1"]
        boss_level.gate2_list = self.tile_map.sprite_lists["gate2"]
        boss_level.event1_list = self.tile_map.sprite_lists["event1"]
        boss_level.event2_list = self.tile_map.sprite_lists["event2"]
        boss_level.enemies_list = arcade.SpriteList()
        
        for enemy in enemies_cord_list:
            # make enemy
            guard = Enemy()
            guard.make_sprite("sprites/enemies/ghost.png")
            
            # set enemy id, damage, speed
            guard.id = self.enemy_id
            guard.damage = 2
            guard.move_speed = 1
            
            # position enemy
            guard.sprite.center_x = enemy[0]
            guard.sprite.center_y = enemy[1]
            
            # add the star to the lists
            boss_level.enemies_list.append(guard.sprite)
            boss_level.class_enemies_list.append(guard)
            
            # increase id          
            self.enemy_id += 1
        
        # set to background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
      
        return boss_level        
    
    
class Enemy(arcade.Sprite):
    ''' a class dedicated to the game's enemies'''
    
    def __init__(self):
        ''' initalize variables '''
        self.health = 0
        self.damage = 1
        self.id = 0
        self.distance = 0
        self.move_speed = 0.3
    
    def make_sprite(self, sprite):
        ''' makes sprite'''
        self.sprite = arcade.Sprite(sprite)
    
    def set_physics_engine(self, wall_list):
        '''sets physics engine '''
        self.physics_engine = arcade.PhysicsEngineSimple(self.sprite,
                                                                wall_list)
    def find_player(self, player_sprite):
        ''' find player and follow '''
        
        # find the (absolute) distance between player and enemy
        self.distance = abs(self.sprite.center_y-player_sprite.center_y) 
        
        # only follow player if distance is between 0 and 90
        if 0 <= self.distance <= 90:
            # move enemy in approprite directions
            if self.sprite.center_y < player_sprite.center_y:
                self.sprite.center_y += min(self.move_speed, player_sprite.center_y - self.sprite.center_y)
            elif self.sprite.center_y > player_sprite.center_y:
                self.sprite.center_y -= min(self.move_speed, self.sprite.center_y - player_sprite.center_y)
            if self.sprite.center_x < player_sprite.center_x:
                self.sprite.center_x += min(self.move_speed, player_sprite.center_x - self.sprite.center_x)
            elif self.sprite.center_x > player_sprite.center_x:
                self.sprite.center_x -= min(self.move_speed, self.sprite.center_x - player_sprite.center_x)
                
                
class Pet(arcade.AnimatedTimeBasedSprite):
    ''' a class dedicated to the pet following the player '''
    
    def follow_sprite(self, player_sprite):
        ''' see where the player is and follow them '''

        # see where the player is, and follow them a little bit behind
        # (see where the player's center is, and mive there but trail behind by 40 pixels)
        # use the animated sprite drawn by me (it's so cute)
        if self.center_y < player_sprite.center_y - 40:
            self.center_y += min(MOVEMENT_SPEED, player_sprite.center_y - 40)
            self.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\dog.png", x = i * 32, y = 32, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.frames.append(anim)
                
        elif self.center_y > player_sprite.center_y + 40:
            self.center_y -= min(MOVEMENT_SPEED, player_sprite.center_y + 40)
            self.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\dog.png", x = i * 32, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.frames.append(anim)                
        
        if self.center_x < player_sprite.center_x - 40:
            self.center_x += min(MOVEMENT_SPEED, player_sprite.center_x - 40)
            self.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\dog.png", x = i * 32, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.frames.append(anim)
                
        elif self.center_x > player_sprite.center_x + 40:
            self.center_x -= min(MOVEMENT_SPEED, player_sprite.center_x + 40)
            self.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\dog.png", x = i * 32, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.frames.append(anim)            
    
class Boss(arcade.Sprite):
    ''' a class dedicated to the boss of the game '''
    
    def __init__(self):
        ''' initalize variables '''
        self.bullet_list = arcade.SpriteList()
        self.bullet = None
        self.bullet_speed = 4
        
    def make_sprite(self, sprite):
        ''' make sprite and set angle'''
        self.sprite = arcade.Sprite(sprite)   
        self.sprite.angle = 180