from image_load import load_image
from actor import Actor


class Character(Actor):
    def __init__(self, sprite_group, pos_x, pos_y, ind, width, height, obstacles, bullet_group, targets):
        super().__init__('character.png', pos_x, pos_y, 2, 3, ind, obstacles,
                         width, height, bullet_group, sprite_group, targets)
        self.image = load_image('character.png')

    def can_shoot(self):
        return False

    def change_speed(self, direct):
        self.vx = 10 * direct


