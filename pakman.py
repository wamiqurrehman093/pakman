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

ENTITY_SCALE = 0.4
PACMAN_SIZE = 20
SPEED = 8

ENEMY_TOTAL = 5
ENEMY_SCALE = 0.3
ENEMY_SPEED = 4

LEFT = arcade.key.LEFT
RIGHT = arcade.key.RIGHT
UP = arcade.key.UP
DOWN = arcade.key.DOWN

TOTAL_COINS = 100
SCALE_COIN = 0.15

class Pakman(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x < PACMAN_SIZE:
            self.center_x = PACMAN_SIZE
        if self.center_x > WIDTH - PACMAN_SIZE:
            self.center_x = WIDTH - PACMAN_SIZE

        if self.center_y < PACMAN_SIZE:
            self.center_y = PACMAN_SIZE
        if self.center_y > HEIGHT - PACMAN_SIZE:
            self.center_y = HEIGHT - PACMAN_SIZE

class Enemy(arcade.Sprite):
    def follow(self, player):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x < PACMAN_SIZE:
            self.center_x = PACMAN_SIZE
        if self.center_x > WIDTH - PACMAN_SIZE:
            self.center_x = WIDTH - PACMAN_SIZE

        if self.center_y < PACMAN_SIZE:
            self.center_y = PACMAN_SIZE
        if self.center_y > HEIGHT - PACMAN_SIZE:
            self.center_y = HEIGHT - PACMAN_SIZE

        if random.randrange(50) == 0:
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
        self.enemy_list = None
        self.player = None
        self.score = None

    def draw_hud(self):
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, WIDTH//2 - 100, HEIGHT - 30, WHITE, 18)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
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
        if self.gameover:
            arcade.window_commands.close_window()
        self.player.update()

        for enemy in self.enemy_list:
            enemy.follow(self.player)

        player_enemy = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        if len(player_enemy) > 0:
            self.gameover = True

        player_coin = arcade.check_for_collision_with_list(self.player, self.coin_list)

        for coin in player_coin:
            coin.kill()
            self.score += 10

    def setup(self):
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.score = 0
        self.gameover = False

        self.player = Pakman('assets/images/pakman.png', ENTITY_SCALE)
        self.player.center_x = 100
        self.player.center_y = 100

        for i in range(ENEMY_TOTAL):
            enemy = Enemy('assets/images/'+ str(i) +'.png', ENTITY_SCALE)
            enemy.center_x = random.randrange(50, WIDTH - 50)
            enemy.center_y = random.randrange(50, HEIGHT- 50)
            self.enemy_list.append(enemy)

        for i in range(TOTAL_COINS):
            coin = arcade.Sprite('assets/images/coin.png', SCALE_COIN)
            coin_placed = False

            while not coin_placed:
                coin.center_x = random.randrange(5, WIDTH - 5)
                coin.center_y = random.randrange(5, HEIGHT- 5)
                coin_hitlist = arcade.check_for_collision_with_list(coin, self.coin_list)
                if len(coin_hitlist) == 0:
                    coin_placed = True
            self.coin_list.append(coin)
        arcade.set_background_color(BLACK)

def main():
    window = Window(WIDTH, HEIGHT, TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
