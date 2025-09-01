# Animated Sprite
# Julianna Morena
# March 9, 2023

# import modules
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
global boss_attack
last_attack = 0
attack_delay = 2
green_orbs_count = 3
red_orb_count = 4
green_orb_count = 3

class MyGame(arcade.Window):
    ''' our custom window class '''
    
    def __init__(self):
        '''initalizer'''
        # call the parent class initalizer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Dangerous Adventures")
        
        # set location of window to screen
        self.set_location(100,100)
        
        # variables that will hold sprite lists
        self.player_list = None
        self.wall_list = None
        self.exit_list = None
        self.current_room = 0
        self.rooms = None
        self.enemies_hit_list = []
        self.enemies_list = []
        self.solids_list = []
        self.key_holding = False
        self.dog_sprite = None
        self.pet_list = None
        
        # set up player info
        self.player_sprite = None
        self.wall_sprite = None
        self.score = 0
        self.player_health = 25
        self.frame_count = 0
        self.counter = 0
        
        # don't show mouse
        self.set_mouse_visible(False)
        self.facing = ''
        self.attacking = False
        self.game_over = False
        self.starting = True
        self.red_orb_hit = False
        self.boss_defeated = False
        self.restart = False
        
        # initalize physics engine
        self.physics_engine = None
        
        # create cameras for scrolling, one for gui and one for sprites
        self.camera_for_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_for_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def setup(self):
        ''' set up the game and initalize variables '''
       
        # sprite lists
        self.player_list = arcade.SpriteList()
        self.pet_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedTimeBasedSprite()
        
        # load textures
        texture = arcade.load_texture("sprites/player.png", x = 0, y = 0, width = 32, height = 32)
        anim = arcade.AnimationKeyframe(1,10, texture)
        self.player_sprite.frames.append(anim)
        
        # set up the player drawn by me
        self.pet_list = arcade.SpriteList()
        self.dog_sprite = gm.Pet()
        texture = arcade.load_texture("sprites/dog.png", x = 0, y = 0, width = 32, height = 32)
        anim = arcade.AnimationKeyframe(1,10, texture)
        self.dog_sprite.frames.append(anim)        
       
        # make a list of levels
        self.rooms = []
        
        # create the levels and add them to the list
        room = gm.Room()
        prison_level = room.setup_room_1()
        self.rooms.append(prison_level)
        
        room = gm.Room()
        castle_level = room.setup_room_2()
        self.rooms.append(castle_level)
        
        room = gm.Room()
        sewer_level = room.setup_room_3()
        self.rooms.append(sewer_level)
        
        room = gm.Room()
        library_level = room.setup_room_4()
        self.rooms.append(library_level)
        
        room = gm.Room()
        maze_level = room.setup_room_5()
        self.rooms.append(maze_level)
        
        room = gm.Room()
        boss_level = room.setup_room_6()
        self.rooms.append(boss_level)           
        
        # starting level
        self.current_room = 0
        
        # make sure the player starts in the bottom left corner
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50        
        
        # add player to sprite list
        self.player_list.append(self.player_sprite)
      
        # make a list that contains every solid layer that cannot be walked through
        self.solids_list = [self.rooms[self.current_room].wall_list, self.rooms[self.current_room].gate1_list, self.rooms[self.current_room].gate2_list]
        
        # set up physics engine for player and dog
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                self.solids_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.dog_sprite,
                                                                self.solids_list)
        # set up a physics engine for every enemy in the level
        for enemy in self.rooms[self.current_room].class_enemies_list:
            enemy.set_physics_engine(self.solids_list)
    
        # set up the dog sprite drawn by me
        self.dog_sprite.center_x = 100
        self.dog_sprite.center_y = 100
        self.pet_list.append(self.dog_sprite)
        
        # set up the boss sprite drawn by me
        self.boss = gm.Boss()
        self.boss.make_sprite("sprites/enemies/captain.png")
        self.boss.sprite.center_x = 300
        self.boss.sprite.center_y = 300
        self.boss_list.append(self.boss.sprite)
        
        # load all sounds from get sounds and pixabay
        self.enemy_attack_sound = arcade.load_sound("sounds/enemy_growl.wav")
        self.enemy_grunt_sound = arcade.load_sound("sounds/grunt.mp3")
        self.bullet_sound = arcade.load_sound("sounds/CANNON_F.wav")
        self.red_orb_sound = arcade.load_sound("sounds/BOMB_HIT.wav")
        self.green_orb_sound = arcade.load_sound("sounds/coin_collect.mp3")
        self.death_sound = arcade.load_sound("sounds/death_sound.mp3")
        self.boss_death_sound = arcade.load_sound("sounds/death_sound.mp3")
        self.background_sound = arcade.load_sound("sounds/lonely_castle.mp3")
        self.knife_slice = arcade.load_sound("sounds/knife_slice.mp3")
        
        # play background music        
        arcade.play_sound(self.background_sound, 1, 0, True)
           
    def on_draw(self):
        ''' draw the spites and text '''
        
        # clear everything that was drawn before
        self.clear()
        
        # if the boss has been defeated
        if self.boss_defeated == True:
            arcade.set_background_color(arcade.csscolor.BLACK)
            arcade.draw_text("GAME FINISHED",
                             80, 270,
                             arcade.color.BLUE, 40)        
        
        # if the game over state has not been triggered...    
        elif self.game_over == False:
            
            arcade.start_render()
    
            self.clear()            
            
            # select the scrolled cameras for our sprites
            self.camera_for_sprites.use()
            
            # draw each layer, the pet, the enemies, and the player
            self.rooms[self.current_room].floor_list.draw()
            self.rooms[self.current_room].wall_list.draw()
            self.rooms[self.current_room].exit_list.draw()
            self.rooms[self.current_room].gate1_list.draw()
            self.rooms[self.current_room].gate2_list.draw()
            self.rooms[self.current_room].event1_list.draw()
            self.rooms[self.current_room].event2_list.draw()
            self.rooms[self.current_room].enemies_list.draw()
            self.pet_list.draw()
            self.player_list.draw()
            
            # draw the orbs for level 4 or boss for level 5
            if self.current_room == 4:
                self.red_orbs_list.draw()
                self.green_orbs_list.draw()
            elif self.current_room == 5:
                self.boss_list.draw()
                self.boss.bullet_list.draw()
            
            # select the unscolled camera for our GUI
            self.camera_for_gui.use()
            
            # put text on screen (score, health, enemies left)
            output = f"Score: {self.score} Health: {self.player_health} Enemies left: {len(self.rooms[self.current_room].enemies_list)}"
            arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        
        # if game over has been triggered, display game over screen
        else:
            arcade.set_background_color(arcade.csscolor.BLACK)
            arcade.draw_text("GAME OVER",
                             80, 270,
                             arcade.color.RED, 50)
            
        # give instructions the first time that you play
        if self.starting is True:
            arcade.draw_text("Hi! Press space to attack, arrows to move, and w to open SOME gates.",
                             20, 270,
                             arcade.color.RED, 12)
            arcade.draw_text("That guard is standing awfully close to the door...",
                             20, 230,
                             arcade.color.RED, 12)
            arcade.draw_text("Hint: pressing E can help cheat in some situations.",
                             20, 190,
                             arcade.color.RED, 12)                
        
    def update(self, delta_time):
        ''' movement and game logic '''
        
        # call update to all sprites
        self.physics_engine.update()
        self.physics_engine2.update()
        self.player_list.update_animation()
        self.pet_list.update_animation()
        
        # scroll the screen to the player
        self.scroll_to_player()
        
        # check player health
        self.check_health()
        
        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].exit_list) != []) and self.current_room == 0  and len(self.rooms[self.current_room].enemies_list) == 0:
            # set the new room (level 2)
            self.current_room = 1
            
            # set the new solids list
            self.solids_list = [self.rooms[self.current_room].wall_list, self.rooms[self.current_room].gate1_list, self.rooms[self.current_room].gate2_list]
            
            # set the new physics engines
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.solids_list)
            self.physics_engine2 = arcade.PhysicsEngineSimple(self.dog_sprite,
                                                             self.solids_list)
            # set a physics engine for each enemy
            for enemy in self.rooms[self.current_room].class_enemies_list:
                enemy.set_physics_engine(self.solids_list)
                
            # set where the player begins
            self.player_sprite.center_x = 25
            
        elif (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].exit_list) != []) and self.current_room == 1  and len(self.rooms[self.current_room].enemies_list) == 0:
             # set the new room (level 3)
            self.current_room = 2
            
            # set the new solids list
            self.solids_list = [self.rooms[self.current_room].wall_list, self.rooms[self.current_room].gate1_list, self.rooms[self.current_room].gate2_list]
            
            # enable the platformer engine for the swimming effect
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, None, 0.1, None, self.solids_list)
            self.physics_engine.enable_multi_jump(1)
            self.physics_engine2 = arcade.PhysicsEngineSimple(self.dog_sprite,
                                                             self.solids_list)
            # set a physics engine for each enemy
            for enemy in self.rooms[self.current_room].class_enemies_list:
                enemy.set_physics_engine(self.solids_list)
                
        elif (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].exit_list) != []) and self.current_room == 2  and len(self.rooms[self.current_room].enemies_list) == 0:
            # set the new room (level 4)
            self.current_room = 3
            
            # set the new solids list
            self.solids_list = [self.rooms[self.current_room].wall_list]
            
            # set the new physics engines
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.solids_list)
            self.physics_engine2 = arcade.PhysicsEngineSimple(self.dog_sprite,
                                                             self.solids_list)
            for enemy in self.rooms[self.current_room].class_enemies_list:
                enemy.set_physics_engine(self.solids_list)
                
            # set where the player begins
            self.player_sprite.center_x = 25
                
        elif (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].exit_list) != []) and self.current_room == 3  and len(self.rooms[self.current_room].enemies_list) == 0 or self.red_orb_hit == True:
            # set the new room (level 5)
            self.current_room = 4
            
            # set up the spite lists and coord lists
            # red orb hit tells you if the player touched the red orb, level will reset if true
            self.red_orbs_list = arcade.SpriteList()
            self.green_orbs_list = arcade.SpriteList()
            self.red_orb_hit = False
            self.red_cord_list = [[110,500], [500,390], [105, 190], [330, 200]]
            self.green_cord_list = [[200,175], [450,520], [500, 200]]
            
            # resize camera so player can see less
            self.camera_for_sprites.resize(310, 310)
            
            # set the new solids list
            self.solids_list = [self.rooms[self.current_room].wall_list]
            
            # set the new physics engines
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.solids_list)
            self.physics_engine2 = arcade.PhysicsEngineSimple(self.dog_sprite,
                                                             self.solids_list)
            for enemy in self.rooms[self.current_room].class_enemies_list:
                enemy.set_physics_engine(self.solids_list)
                
            # set where the player begins
            self.player_sprite.center_x = 25
            
            # create red orbs
            for coord in self.red_cord_list:
                
                # create the star instance DRAWN BY ME
                red_orb = arcade.Sprite("sprites/red_orb.png", 0.7)
                
                # position orb
                red_orb.center_x = coord[0]
                red_orb.center_y = coord[1]                
                
                # add the star to the lists
                self.red_orbs_list.append(red_orb)
            
            # create green orbs
            for coord in self.green_cord_list:
                
                # create the star instance DRAWN BY ME
                green_orb = arcade.Sprite("sprites/green_orb.png", 0.7)
                
                # position orb
                green_orb.center_x = coord[0]
                green_orb.center_y = coord[1]                
                
                # add the star to the lists
                self.green_orbs_list.append(green_orb)            
                                  
        elif (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].exit_list) != []) and self.current_room == 4  and len(self.green_orbs_list) == 0 or self.restart == True:
            # set the new room (level 6)
            
            # variable to restart level for different stages
            self.restart = False
            self.current_room = 5
            
            # set the new solids list
            self.solids_list = [self.rooms[self.current_room].wall_list]
            
            # set the new physics engines
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.solids_list)
            self.physics_engine2 = arcade.PhysicsEngineSimple(self.dog_sprite,
                                                             self.solids_list)
            for enemy in self.rooms[self.current_room].class_enemies_list:
                enemy.set_physics_engine(self.solids_list)
                
            # set where the player begins
            self.player_sprite.center_x = 25
            
          # call update to all sprites
        self.rooms[self.current_room].enemies_list.update()
        self.rooms[self.current_room].enemies_list.update_animation()
        
        # if the enemy has been hit, remove them and add to score
        for enemy in self.enemies_hit_list:
            enemy.remove_from_sprite_lists()
            self.score += 1
            self.enemies_hit_list.remove(enemy)
        
        # make sure that every enemy looks for player and updates their physics engine
        for enemy in self.rooms[self.current_room].class_enemies_list:
            enemy.find_player(self.player_sprite)
            enemy.physics_engine.update()
        
        # update dog and gets them to follow you    
        self.pet_list.update()
        self.pet_list.update_animation()
        self.dog_sprite.follow_sprite(self.player_sprite)
        
        # if on level 5
        if self.current_room == 4:
            
            # update red orbs list
            self.red_orbs_list.update()
                    
            # generate a list of all sprites that collided with the player
            red_orb_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.red_orbs_list)
            
            # loop through each colliding sprite, remove it, and add it to the score
            for red_orb in red_orb_hit_list:
                red_orb.remove_from_sprite_lists()
                
                # shake the camera
                shake_direction = random.random() * 2 * math.pi
                # How 'far' to shake
                shake_amplitude = 10
                # Calculate a vector based on that
                shake_vector = Vec2(
                    math.cos(shake_direction) * shake_amplitude,
                    math.sin(shake_direction) * shake_amplitude
                )
                # Frequency of the shake
                shake_speed = 1.5
                # How fast to damp the shake
                shake_damping = 0.9
                # Do the shake
                self.camera_for_sprites.shake(shake_vector,
                                          speed=shake_speed,
                                          damping=shake_damping)
                
                # play sound and restart level
                arcade.play_sound(self.red_orb_sound)
                self.red_orb_hit = True
            
            # check if player has hit and green orbs and remove them + play sound 
            green_orb_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.green_orbs_list)
            for green_orb in green_orb_hit_list:
                green_orb.remove_from_sprite_lists()
                arcade.play_sound(self.green_orb_sound)
        
        # if on level 5 and the boss is still alive        
        elif self.current_room == 5 and self.boss_defeated == False:
            
            # add to frame count 
            self.frame_count += 1

            # Position the start at the enemy's current location
            start_x = self.boss.sprite.center_x
            start_y = self.boss.sprite.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # figure out how far the player is from the bullet
            # angle the bullet towards the player
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            self.boss.sprite.angle = math.degrees(angle) - 90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 50 == 0:
                self.boss.bullet = arcade.Sprite("sprites/enemies/fire_ball.png")
                
                self.boss.bullet.center_x = start_x
                self.boss.bullet.center_y = start_y

                # Angle the bullet sprite
                self.boss.bullet.angle = math.degrees(angle)

                # including the angle, move bullet at a set speed
                self.boss.bullet.change_x = math.cos(angle) * self.boss.bullet_speed
                self.boss.bullet.change_y = math.sin(angle) * self.boss.bullet_speed
                
                # add to bullet list and make sound with each bullet
                self.boss.bullet_list.append(self.boss.bullet)
                arcade.play_sound(self.bullet_sound)

            # Get rid of the bullet when it touches something solid
            for bullet in self.boss.bullet_list:
                if arcade.check_for_collision_with_list(bullet, self.rooms[self.current_room].wall_list) != []:
                    bullet.remove_from_sprite_lists()
                # damage the player if the bullet touches them
                elif arcade.check_for_collision(bullet, self.player_sprite) == True:
                    self.player_health -= 4
                    bullet.remove_from_sprite_lists()
            
            # update bullet list       
            self.boss.bullet_list.update()
            
            # if the player attacks the bpss
            if arcade.check_for_collision(self.player_sprite, self.boss.sprite) == True:
                # counter to keep track of how many times player has attacked
                self.counter += 1
                
                # if player has attacked three times
                # boss is defeated, don't restart level
                if self.counter == 3:
                    self.boss_defeated = True
                    self.restart = False
                    self.boss.sprite.remove_from_sprite_lists()
                    self.boss.bullet_list.clear()
                    arcade.play_sound(self.boss_death_sound)
                else:
                    # shake camera and restart level
                    self.restart = True
                    shake_direction = random.random() * 2 * math.pi
                    # How 'far' to shake
                    shake_amplitude = 10
                    # Calculate a vector based on that
                    shake_vector = Vec2(
                        math.cos(shake_direction) * shake_amplitude,
                        math.sin(shake_direction) * shake_amplitude
                    )
                    # Frequency of the shake
                    shake_speed = 1.5
                    # How fast to damp the shake
                    shake_damping = 0.9
                    # Do the shake
                    self.camera_for_sprites.shake(shake_vector,
                                              speed=shake_speed,
                                              damping=shake_damping)
    
        # if player attacked enemy first, kill them
        # otherwise hurt the player by that enemy's damage
        if arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].enemies_list) != []:
            global last_attack # set global variable for delay
            if self.attacking:
                self.player_attack()
                arcade.play_sound(self.enemy_grunt_sound, 2)
            elif time.time() >= (last_attack + attack_delay): # add a delay so it is not instant kill
                last_attack = time.time()
                self.player_health -= self.rooms[self.current_room].class_enemies_list[0].damage
                arcade.play_sound(self.enemy_attack_sound, 2)

    def scroll_to_player(self):
        ''' scroll the winow to the player '''
        
        # set camera speed
        CAMERA_SPEED = 1
        # scroll the window to the player
        lower_left_corner = (self.player_sprite.center_x - self.width / 2,
                             self.player_sprite.center_y - self.height / 2)
        self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)        
            
    def on_key_press(self, key, modifiers):
        ''' check to see which key is being pressed and move the player in the appropriate direction '''
        
        # controls the player attacking
        if key == arcade.key.SPACE:
            
            # let the game know that the player is attacking
            self.attacking = True
            # get rid of the instructions at the begining
            self.starting = False
            
            # play sound
            arcade.play_sound(self.knife_slice)
            
            # this code tells which way the player is facing and does
            # the appropriate attacking sprite
            if self.facing == 'left':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_left.png")
                    anim = arcade.AnimationKeyframe(i, 250, texture)
                    self.player_sprite.frames.append(anim)
                
            elif self.facing == 'right':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_right.png")
                    anim = arcade.AnimationKeyframe(i, 250, texture)
                    self.player_sprite.frames.append(anim)
                
            elif self.facing == 'down':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_front.png")
                    anim = arcade.AnimationKeyframe(i, 250, texture)
                    self.player_sprite.frames.append(anim)
                
            elif self.facing == 'up':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_back.png")
                    anim = arcade.AnimationKeyframe(i, 250, texture)
                    self.player_sprite.frames.append(anim)
            
            # when player attacks near gate , kill the enemy beside the gate in level one if he is not dead already 
            if (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].event1_list) != [] and not self.key_holding):
                self.enemies_hit_list.append(self.rooms[self.current_room].enemies_list[2])
                # let the player open other gates in level 1
                self.key_holding = True
                
          # controls the player movement and changes to the appropriate sprites
          # change the facing variable so game knows which direction player is facing
        elif key == arcade.key.UP:
            self.facing = 'up'
            self.player_sprite.change_y = self.rooms[self.current_room].up_speed
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = i * 32, y = 32, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)             
        elif key == arcade.key.DOWN:
            self.facing = 'down'
            self.player_sprite.change_y = -MOVEMENT_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = i * 32, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)            
        elif key == arcade.key.RIGHT:
            self.facing = 'right'
            self.player_sprite.change_x = MOVEMENT_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = i * 32, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.LEFT:
            self.facing = 'left'
            self.player_sprite.change_x = -MOVEMENT_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = i * 32, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        
        # open the gates in level 1 when condition are met        
        elif key == arcade.key.W and self.key_holding is True:
            if (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].event1_list) != []):
                self.rooms[self.current_room].gate1_list.clear()
            elif (arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].event2_list) != []):
                self.rooms[self.current_room].gate2_list.clear()
         
         # press E to boost your health or help you see in the dark maze level       
        elif key == arcade.key.E:
            self.player_health += 1
            self.camera_for_sprites.resize(550, 550)
            
    def on_key_release(self, key, modifiers):
        ''' check to see if the key is being released '''
        
        # clear sprite list when key is released
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = 0, y = 32, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 10, texture)
                self.player_sprite.frames.append(anim)            
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = 0, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 10, texture)
                self.player_sprite.frames.append(anim)            
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = 0, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 10, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("sprites\player.png", x = 0, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 10, texture)
                self.player_sprite.frames.append(anim)
        
        # clears sprite list when released        
        elif key == arcade.key.SPACE:
            self.attacking = False
            if self.facing == 'left':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_left.png")
                    anim = arcade.AnimationKeyframe(i, 10, texture)
                    self.player_sprite.frames.append(anim)
            elif self.facing == 'right':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_right.png")
                    anim = arcade.AnimationKeyframe(i, 10, texture)
                    self.player_sprite.frames.append(anim)
            elif self.facing == 'down':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_front.png")
                    anim = arcade.AnimationKeyframe(i, 10, texture)
                    self.player_sprite.frames.append(anim)
            elif self.facing == 'up':
                self.player_sprite.frames.clear()
                for i in range(4):
                    texture = arcade.load_texture("sprites/player_attacking/player_attacking_back.png")
                    anim = arcade.AnimationKeyframe(i, 10, texture)
                    self.player_sprite.frames.append(anim)
                    
    def player_attack(self):
        ''' checks whether the player has successfully attacked the enemy '''
        # generate a list of all sprites that collided with the player
        self.enemies_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].enemies_list)
    
    def check_health(self):
        ''' checks players health, sets game over if it is zero, and plays death sound'''
        if self.player_health <= 0:
            self.game_over = True
            arcade.play_sound(self.death_sound)
            
    def close(self):
        ''' close window and stop background music '''
        super().close()
        self.bgm.pause()
        self.bgm.delete()            
        
              
def main():
    ''' main method '''
    window = MyGame()
    window.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()
        