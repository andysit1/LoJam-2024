

from state import State
from components.sprite_base import Moving_Sprite, SquareMovingSprite
from components.projectiles import HProjectiles, TravelProjectiles, HTravelProjectiles
# class Player:


import pygame as pg
from pygame.math import Vector2
from random import randint


#represents the current block in hand
class Inventory:
    def __init__(self):
        self.blocks : list = []
        self.current_block : int = 0

    def get_current_block(self) -> Moving_Sprite:
       return self.blocks[self.current_block]

    #on place go to to the next right more block
    def get_next_possible(self):
        if self.current_block == -1:
           return

        for i, block in enumerate(self.blocks):
           if not block.is_placed:
              self.current_block = i
              return self.get_current_block()
        return -1

    def go_left(self):
        self.current_block -= 1
        #at start of inv
        if self.current_block < 0:
           self.current_block = len(self.blocks) - 1

    def go_right(self):
       self.current_block += 1
       #at end of inv
       if self.current_block == len(self.blocks):
          self.current_block = 0


class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('blue'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 1

        self.block_inventory = Inventory()
        

        self.block_inventory_group = pg.sprite.Group()
       
        block1 = SquareMovingSprite(self, self.block_inventory_group)
        block2 = SquareMovingSprite(self, self.block_inventory_group)
        block3 = SquareMovingSprite(self, self.block_inventory_group)

        block2.make_transpart()
        block3.make_transpart()
        self.block_inventory.blocks = [block1, block2, block3]
        self.block : SquareMovingSprite = self.block_inventory.get_current_block()
        self.block_group : pg.sprite.GroupSingle = pg.sprite.GroupSingle()

        self.placed_blocks : pg.sprite.Group = pg.sprite.Group()

    def input(self, event):
        ## movement
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = self.speed
            elif event.key == pg.K_a:
                self.vel.x = -self.speed
            elif event.key == pg.K_w:
                self.vel.y = -self.speed
            elif event.key == pg.K_s:
                self.vel.y = self.speed
            elif event.key == pg.K_SPACE:
               print("placed")
               #add block to placed group
               self.block.is_placed = True
               self.placed_blocks.add(self.block)
               #get new...
               self.block = self.block_inventory.get_next_possible()
               


        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pg.K_s and self.vel.y > 0:
                self.vel.y = 0


        if isinstance(self.block, Moving_Sprite):
          if self.vel.y > 0 and not self.vel.x:
            self.block.set_selected_points("down")
          elif self.vel.y < 0 and not self.vel.x:
            self.block.set_selected_points("up")
          elif self.vel.x > 0 and not self.vel.x < 0:
            self.block.set_selected_points("right")
          elif self.vel.x < 0 and not self.vel.x > 0:
            self.block.set_selected_points("left")

    def update(self, delta):
        # Move the player.
        self.pos += self.vel * delta * 150
        self.rect.center = self.pos


BLUE = (0, 0, 255)


class Door(pg.sprite.Sprite):
   def __init__(self, *groups):
      super().__init__(*groups)
      self.image = pg.Surface((50, 50))
      self.image.fill("green")
      self.rect = self.image.get_rect()


class Pit(pg.sprite.Sprite):
   def __init__(self, *groups):
      super().__init__(*groups)
      self.image = pg.Surface((120, 120))
      self.rect = self.image.get_rect()


class GameState(State):
  def __init__(self, engine, hardness_scale : int = 1):
    self.hard_level : int = hardness_scale

    self.engine = engine
    self.character_sprite = pg.sprite.Group()

    self.bo_width, self.bo_height = 1280 - 200, 720 - 200
    self.trigger_zone1 = pg.Rect((self.bo_width // 3) + 100, 0, self.bo_width // 3, 720)
    self.trigger_zone2 = pg.Rect((self.bo_width // 3) * 2 + 100, 0, self.bo_width // 3, 720)

    self.pits : pg.sprite.Group = pg.sprite.Group()
    self.potential_pit = (120, 120)

    self.player : Player = Player((200, self.bo_height // 2 + 100), self.character_sprite)
    self.start_pos : pg.Vector2 = pg.Vector2(200, self.bo_height // 2 + 100)
    self.end_pos : pg.Vector2 = pg.Vector2(self.bo_width,  self.bo_height // 2 + 100)

    self.game_ending_door : pg.sprite.GroupSingle = pg.sprite.GroupSingle()
    door = Door(self.game_ending_door)
    door.rect.x, door.rect.y = self.end_pos.x, self.end_pos.y

    self.bo = []
    blockSize = 40 #Set the size of the grid block
    for x in range(100, self.bo_width + 100, blockSize):
        for y in range(100, self.bo_height + 100, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)


            if not x <= self.start_pos.x <= x + 120 and not y <= self.start_pos.y <= y + 120:

                if randint(0, 10) == 0:
                    #add change of pit spawn
                    Pit(self.pits).rect.topleft = (x, y)
            self.bo.append(rect)

    self.projectiles_grp = pg.sprite.Group()
    self.projectiles = HProjectiles(self.character_sprite)
    self.t_list = []
    self.init_t_projectiles()
    self.flying : bool = False

  def init_t_projectiles(self):
        #top down
        for i in range(100, self.bo_width , 200):
            print(f"Created T_Project {i}")
            t = TravelProjectiles(self.projectiles_grp)
            t.dir = pg.Vector2(0, 1)
            t.rect.x , t.rect.y = i, 100

            t2 = TravelProjectiles(self.projectiles_grp)
            t2.dir = pg.Vector2(0, -1)
            t2.rect.x , t2.rect.y = i, self.bo_height + 100

            self.t_list.append(t)
            self.t_list.append(t2)

        for i in range(100, self.bo_height , 150):
            t = HTravelProjectiles(self.projectiles_grp)
            t.dir = pg.Vector2(1, 0)
            t.rect.x , t.rect.y = 100, i

            t2 = HTravelProjectiles(self.projectiles_grp)
            t2.dir = pg.Vector2(-1, 0)
            t2.rect.x , t2.rect.y = self.bo_width + 100, i

            self.t_list.append(t)
            self.t_list.append(t2)

  def draw_grid(self, surface):
      for rect in self.bo:
         pg.draw.rect(surface, "grey", rect, 1)

  def on_draw(self, surface):
      surface.fill("white")
      # pg.draw.rect(surface, "red", self.trigger_zone1)
      # pg.draw.rect(surface, "blue", self.trigger_zone2)
      self.draw_grid(surface)
      self.pits.draw(surface)
      pg.draw.rect(surface, BLUE, (100, 100, self.bo_width, self.bo_height), 2)
      self.character_sprite.draw(surface)

      if self.player.block:
        surface.blit(self.player.block.image, self.player.block.rect)

      for proj in self.t_list:
         proj.draw_shot(surface)

      #clearing overlap
      pg.draw.rect(surface, "white", (0, 0, 1280, 100))
      pg.draw.rect(surface, "white", (0, 620, 1280, 100))
      pg.draw.rect(surface, "white", (0, 0, 100, 720))
      pg.draw.rect(surface, "white", (1180, 0, 100, 720))

      self.game_ending_door.draw(surface)
      ## Rectangle dimensions and offset
      x, y = 100, 100
      width, height = 1080, 520
      offset = 30

      # Define trapezoid points
      top_trapezoid = [(x, y), (x + width, y), (x + width - offset, y + offset), (x + offset, y + offset)]
      right_trapezoid = [(x + width, y), (x + width, y + height), (x + width - offset, y + height - offset), (x + width - offset, y + offset)]
      bottom_trapezoid = [(x, y + height), (x + width, y + height), (x + width - offset, y + height - offset), (x + offset, y + height - offset)]
      left_trapezoid = [(x, y), (x, y + height), (x + offset, y + height - offset), (x + offset, y + offset)]

      pg.draw.polygon(surface, (200, 200, 200), top_trapezoid)
      pg.draw.polygon(surface, (150, 150, 150), bottom_trapezoid)
      pg.draw.polygon(surface, (100, 100, 100), right_trapezoid)
      pg.draw.polygon(surface, (50, 50, 50), left_trapezoid)

  def proj_update(self, delta):
      if self.player.block:
        self.player.block.update(delta)

      for proj in self.t_list:
        proj.update(delta)


        # logic for placed block interaction
        shot_to_remove, sprite = proj.is_colliding_group(self.player.placed_blocks)
        if proj.is_colliding_player(self.player):
           print("DIED")
           self.engine.machine.next_state = GameState(engine=self.engine)

        if shot_to_remove and sprite:
            proj.shots.remove(shot_to_remove)
            self.character_sprite.remove(sprite)
            self.player.placed_blocks.remove(sprite)

        #logic for when proj and block flying
        try:
            shot = proj.is_colliding_block(self.player.block)
            if shot:
                self.player.pos += shot['direction'] * shot['speed'] * delta
                self.player.rect.center = self.player.pos
                self.flying = True
                
        except:
            pass

  def on_update(self, delta):
      self.projectiles.update(delta)
      self.character_sprite.update(delta)
      self.game_ending_door.update(delta)
      self.proj_update(delta)

      if pg.sprite.groupcollide(self.pits, self.character_sprite, dokilla=False, dokillb=False):
        if not self.flying:
            self.engine.machine.next_state = GameState(engine=self.engine)
        
        self.flying = False
      if pg.sprite.groupcollide(self.character_sprite, self.game_ending_door, dokilla=False, dokillb=False):
         print("WIN")
         #trigger game winning

         if self.hard_level == 3:
            # send them to win state
            pass
         
         self.engine.machine.next_state = GameState(engine=self.engine, hardness_scale=self.hard_level + 1)



  def on_event(self, event):
    self.player.input(event)

  def handle_movement(self):
    return super().handle_movement()
