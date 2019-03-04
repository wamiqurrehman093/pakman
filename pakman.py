import arcade
import os
import math
import random

WIDTH = 1280
HEIGHT = 720
TITLE = "PAKMAN - GAME"

WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
BLUE = arcade.color.ALICE_BLUE

ENTITY_SCALE = 0.3
SPEED = 5
WALL_SCALE = 0.5

ENEMY_TOTAL = 5
ENEMY_SCALE = 0.1
ENEMY_SPEED = 2

LEFT = arcade.key.LEFT
RIGHT = arcade.key.RIGHT
UP = arcade.key.UP
DOWN = arcade.key.DOWN

TOTAL_COINS = 200
SCALE_COIN = 0.15

class Enemy(arcade.Sprite):
    def set_physics_engine(self, wall_list):
        self.physics_engine = arcade.PhysicsEngineSimple(self, wall_list)

    def follow(self, player):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            dest_x = player.center_x
            dest_y = player.center_y

            diff_x = dest_x - start_x
            diff_y = dest_y - start_y

            angle = math.atan2(diff_y, diff_x)

            self.change_x = math.cos(angle) * ENEMY_SPEED
            self.change_y = math.sin(angle) * ENEMY_SPEED

class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)

        self.gameover = False
        self.coin_list = None
        self.wall_list = None
        self.enemy_list = None
        self.player = None
        self.physics_engine = None
        self.enemy_physics_engine = None
        self.score = None

    def draw_hud(self):
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, WIDTH//2 - 100, HEIGHT - 30, WHITE, 18)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.draw_hud()
        self.enemy_list.draw()

    def on_key_release(self, key, mods):
        if key == LEFT or key == RIGHT:
            self.player.change_x = 0
        if key == UP or key == DOWN:
            self.player.change_y = 0

    def on_key_press(self, key, mods):
        if key == LEFT:
            self.player.change_x = -SPEED
        if key == RIGHT:
            self.player.change_x = SPEED
        if key == UP:
            self.player.change_y = SPEED
        if key == DOWN:
            self.player.change_y = -SPEED

    def update(self, delta_time):
        self.physics_engine.update()

        for enemy in self.enemy_list:
            enemy.follow(self.player)
        for enemy in self.enemy_list:
            enemy.physics_engine.update()

        player_enemy = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        if len(player_enemy) > 0:
            self.gameover = True

        player_coin = arcade.check_for_collision_with_list(self.player, self.coin_list)

        for coin in player_coin:
            coin.kill()
            self.score += 10

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.score = 0
        self.gameover = False

        self.player = arcade.Sprite('assets/images/pakman.png', ENTITY_SCALE)
        self.player.center_x = 93
        self.player.center_y = 93

        for i in range(5):
            enemy = Enemy('assets/images/enemy.png', ENTITY_SCALE)
            enemy_placed = False
            enemy.set_physics_engine(self.wall_list)

            while not enemy_placed:
                enemy.center_x = random.randrange(100, WIDTH - 100)
                enemy.center_y = random.randrange(100, HEIGHT - 100)

                enemy_wall = arcade.check_for_collision_with_list(enemy, self.wall_list)

                if len(enemy_wall) == 0:
                    enemy_placed = True
            self.enemy_list.append(enemy)

        for y in range(31, HEIGHT - 31, HEIGHT - 63):
            for x in range(30, WIDTH, 62):
                wall = arcade.Sprite('assets/images/box.png', WALL_SCALE)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        for x in range(30, WIDTH, WIDTH - 62):
            for y in range(93, HEIGHT, 63):
                wall = arcade.Sprite('assets/images/box.png', WALL_SCALE)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        for i in range(TOTAL_COINS):
            coin = arcade.Sprite('assets/images/coin.png', SCALE_COIN)
            coin_placed = False

            while not coin_placed:
                coin.center_x = random.randrange(WIDTH)
                coin.center_y = random.randrange(HEIGHT)

                coin_hitlist = arcade.check_for_collision_with_list(coin, self.coin_list)
                wall_hitlist = arcade.check_for_collision_with_list(coin, self.wall_list)

                if len(coin_hitlist) == 0 and len(wall_hitlist) == 0:
                    coin_placed = True

            self.coin_list.append(coin)


        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

        arcade.set_background_color(BLUE)


def main():
    window = Window(WIDTH, HEIGHT, TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
