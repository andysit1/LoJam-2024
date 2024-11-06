import pygame as pg
from random import randint
vec2 = pg.math.Vector2

#just for the sake for the example here.

def generate_location_screen() -> vec2:
  return vec2(randint(0, 1280 - 200), randint(0, 720 - 200))

def generate_position_out_of_screen() -> pg.math.Vector2:
    WIDTH, HEIGHT = 280 - 200, 720 - 200
    from random import choice
    x_offset = [-1, -4, -10, WIDTH + 1, WIDTH + 4, WIDTH + 10]
    y_offset = [-1, -4, -10, HEIGHT + 1, HEIGHT + 4, HEIGHT + 10]

    x = choice(x_offset)
    y = choice(y_offset)

    return pg.math.Vector2(x, y)

class HProjectiles(pg.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

    self.image = pg.Surface((3, 3))
    self.image.fill("red")
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = generate_location_screen()

    #respawn timer to delay
    self.respawn_timer = .2
    self.shots = []


  def create_shot(self):
    speed = randint(20, 45)
    return {
            'surface' :  self.image,
            'position' : pg.Vector2(self.rect.x,  self.rect.y),
            'speed' : speed,
            'direction' : pg.Vector2(0, -1),
            'radius' : 7,
            'life' : 4
          }

  def get_rect(self, obj):
    return pg.Rect(obj['position'][0],
                    obj['position'][1],
                    obj['surface'].get_width(),
                    obj['surface'].get_height())

  def is_colliding_group(self, group : pg.sprite.Group):
    for sprite in group:
      for shot in list(self.shots):
        if self.get_rect(shot).colliderect(sprite.rect):
          print('removing...')
          return shot, sprite
    return None, None

  def is_colliding_player(self, player : pg.sprite.Sprite):
    for shot in self.shots:
      if pg.Rect.colliderect(player.rect, self.get_rect(shot)):
        return True
    return False

  def is_colliding_block(self, block : pg.sprite.Sprite):
    for shot in self.shots:
      if pg.Rect.colliderect(block.rect, self.get_rect(shot)):
        return shot
    return None
    #handles remove and update
  def update_shot(self, dt):
    for shot in self.shots:
      shot['position'] += shot['direction'] * shot['speed'] * dt
      shot['life'] -= 1 * dt

      if shot['life'] < 0:
        try:
          self.shots.remove(shot)
        except:
          pass

  def draw_shot(self, surface: pg.Surface):
    for shot in self.shots:
      if shot:
        surface.blit(shot['surface'].convert_alpha(), shot['position'])

  def update(self, dt):
    self.update_shot(dt)

    self.respawn_timer -= 1 * dt
    if self.respawn_timer < 0:
      for _ in range(3):
        self.shots.append(self.create_shot())
      self.respawn_timer = .2


class TravelProjectiles(HProjectiles):
  def __init__(self, *groups):
    super().__init__(*groups)
    self.image = pg.Surface((3, 200))
    self.image.fill("red")

    self.rect = self.image.get_rect()
    self.respawn_timer = randint(7, 10)
    self.dir : pg.Vector2 =  pg.Vector2(1, 0)

  def create_shot(self):
    speed = randint(180, 200)
    shot = {
            'surface' :  self.image,
            'position' : pg.Vector2(self.rect.x,  self.rect.y),
            'speed' : speed,
            'direction' : self.dir,
            'radius' : 7,
            'life' : 4
          }

    return shot

  def update(self, dt):
    self.update_shot(dt)

    self.respawn_timer -= 1 * dt
    if self.respawn_timer < 0:
      self.shots.append(self.create_shot())
      self.respawn_timer = randint(2, 5)



class HTravelProjectiles(TravelProjectiles):
  def __init__(self, *groups):
    super().__init__(*groups)
    self.image = pg.Surface((200, 3))
    self.image.fill("red")

    self.respawn_timer = randint(2, 5)

