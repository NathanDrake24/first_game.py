import pickle

import pygame

Window_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
FPS = 25
TILE_SIZE = 32
TIMER_EVENT_TYPE = 5000
DATA_DIR = "data"
DATA_GAME = "data_game"


class Labyrinth:# класс Лабиринт

    def __init__(self, filename, free_tile, finish_tile):
        self.map = []
        with open(f"{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tile = free_tile

        self.finish_tile = finish_tile

    def render(self, screen):#отображение карты
        bg = pygame.image.load('map.png')
        screen.blit(bg, (0, 0))

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tile


class Hero:#класс главного героя

    def __init__(self, position):
        self.x, self.y = position
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.x_hero, self.y_hero = 1, 1
        self.health = 5

    def get_flags(self):#возврщает направления
        return self.right, self.left, self.up, self.down

    def set_flags(self, flags):#задает направления
        self.right, self.left, self.up, self.down = flags

    def get_position(self):#возврщает координаты
        return self.x, self.y

    def set_position(self, position):#задает координаты
        self.x, self.y = position

    def render(self, screen):#отображение героя
        self.x_hero, self.y_hero = self.x * TILE_SIZE, self.y * TILE_SIZE
        walkRight = pygame.image.load('hero_right.png')

        walkLeft = pygame.image.load('hero_left.png')

        playerStand = pygame.image.load('stay.png')

        walkup = pygame.image.load('hero_up.png')

        if self.left:
            screen.blit(walkLeft, (self.x_hero, self.y_hero))
        elif self.right:
            screen.blit(walkRight, (self.x_hero, self.y_hero))
        elif self.up:
            screen.blit(walkup, (self.x_hero, self.y_hero))
        elif self.down:
            screen.blit(playerStand, (self.x_hero, self.y_hero))
        else:
            screen.blit(playerStand, (self.x_hero, self.y_hero))
        pygame.display.update()


class Enemy:#класс противника

    def __init__(self, position):
        self.x, self.y = position
        self.health = True

        self.right = True
        self.left = False

    def get_flags(self):#возврщает направления
        return self.right, self.left

    def set_flags(self, flags):#задает направления
        self.right, self.left = flags

    def get_position(self):#возврщает координаты
        return self.x, self.y

    def set_position(self, position):#задает координаты
        self.x, self.y = position

    def set_health(self, health):#задает здоровье
        self.health = health

    def render(self, screen):#отображает противника
        if self.health:
            if self.right:
                enemy_img = pygame.image.load('enemy_r.png')
            else:
                enemy_img = pygame.image.load('enemy_l.png')
            screen.blit(enemy_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        pygame.display.update()


class Demon:#класс демона
    def __init__(self, position, check_left):
        self.x, self.y = position
        self.health = True
        self.up = True
        self.down = False
        self.check_left = check_left

    def get_flags(self):#возврщает направления
        return self.up, self.down

    def set_flags(self, flags):#задает направления
        self.up, self.down = flags

    def get_position(self):#возврщает координаты
        return self.x, self.y

    def set_position(self, position):#задает координаты
        self.x, self.y = position

    def set_health(self, health):#задает здоровье
        self.health = health

    def render(self, screen):#отображает демона
        if self.health:
            if self.check_left:
                enemy_img = pygame.image.load('demon_left.png')
            else:
                enemy_img = pygame.image.load('demon_right.png')
            screen.blit(enemy_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        pygame.display.update()


class Game:#класс игра
    def __init__(self, labyrinth, hero, enemy, demon, enemy_2, enemy_3, enemy_4, enemy_5, enemy_6, enemy_7, enemy_8,
                 enemy_9, enemy_10, demon_1, demon_2, demon_3, demon_4):
        self.delay = 10000
        pygame.time.set_timer(TIMER_EVENT_TYPE, self.delay)
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemy = enemy
        self.enemy_2 = enemy_2
        self.enemy_3 = enemy_3
        self.enemy_4 = enemy_4
        self.enemy_5 = enemy_5
        self.enemy_6 = enemy_6
        self.enemy_7 = enemy_7
        self.enemy_8 = enemy_8
        self.enemy_9 = enemy_9
        self.enemy_10 = enemy_10
        self.demon = demon
        self.demon_1 = demon_1
        self.demon_2 = demon_2
        self.demon_3 = demon_3
        self.demon_4 = demon_4
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.health = 10

        self.health_enemy = True
        self.health_enemy_2 = True
        self.health_enemy_3 = True
        self.health_enemy_4 = True
        self.health_enemy_5 = True
        self.health_enemy_6 = True
        self.health_enemy_7 = True
        self.health_enemy_8 = True
        self.health_enemy_9 = True
        self.health_enemy_10 = True

        self.health_demon = True
        self.health_demon_1 = True
        self.health_demon_2 = True
        self.health_demon_3 = True
        self.health_demon_4 = True

        self.key_check = 0
        self.game_over = 0
        self.is_paused = 0
        self.number_of_opponents = 15

    def render(self, screen):
        if self.is_paused != 1:
            pygame.time.set_timer(TIMER_EVENT_TYPE, self.delay)
            self.labyrinth.render(screen)
            self.hero.render(screen)
            font = pygame.font.Font(None, 24)
            text = font.render(f"Жизней: {self.health}", True, (255, 0, 0))
            screen.blit(text, (20, 20))
            x, y = self.hero.get_position()
            if (x != 9 or y != 9) and (self.key_check == 0):
                key_img = pygame.image.load('key.png')
                screen.blit(key_img, (9 * TILE_SIZE, 9 * TILE_SIZE))
            if x == 9 and y == 9:
                self.key_check = 1
            if x != 13 or y != 1 or self.key_check == 0:
                door_img = pygame.image.load('дверь_закрытая.png')
            else:
                door_img = pygame.image.load('открытая_дверь.png')
                if self.number_of_opponents == 0:
                    self.game_over = 1
                else:
                    self.game_over = 2
            screen.blit(door_img, (13 * TILE_SIZE, TILE_SIZE))
        if self.is_paused == 0:
            self.enemy.render(screen)
            self.enemy_2.render(screen)
            self.enemy_3.render(screen)
            self.enemy_4.render(screen)
            self.enemy_5.render(screen)
            self.enemy_6.render(screen)
            self.enemy_7.render(screen)
            self.enemy_8.render(screen)
            self.enemy_9.render(screen)
            self.enemy_10.render(screen)
            self.demon.render(screen)
            self.demon_1.render(screen)
            self.demon_2.render(screen)
            self.demon_3.render(screen)
            self.demon_4.render(screen)

    def update_demon(self):
        if self.health_demon:
            next_x, next_y = self.demon.get_position()
            up_enemy, down_enemy = self.demon.get_flags()

            if up_enemy:
                if self.labyrinth.is_free((next_x, next_y + 1)):
                    next_y += 1
                    self.demon.set_position((next_x, next_y))
                else:
                    down_enemy = True
                    up_enemy = False
                    self.demon.set_flags((up_enemy, down_enemy))
            elif down_enemy:
                if self.labyrinth.is_free((next_x, next_y - 1)):
                    next_y -= 1
                    self.demon.set_position((next_x, next_y))
                else:
                    down_enemy = False
                    up_enemy = True
                    self.demon.set_flags((up_enemy, down_enemy))
        else:
            self.demon.set_health(self.health_demon)

    def update_demon_1(self):
        if self.health_demon_1:
            next_x, next_y = self.demon_1.get_position()
            up_enemy, down_enemy = self.demon_1.get_flags()

            if up_enemy:
                if self.labyrinth.is_free((next_x, next_y + 1)):
                    next_y += 1
                    self.demon_1.set_position((next_x, next_y))
                else:
                    down_enemy = True
                    up_enemy = False
                    self.demon_1.set_flags((up_enemy, down_enemy))
            elif down_enemy:
                if self.labyrinth.is_free((next_x, next_y - 1)):
                    next_y -= 1
                    self.demon_1.set_position((next_x, next_y))
                else:
                    down_enemy = False
                    up_enemy = True
                    self.demon_1.set_flags((up_enemy, down_enemy))
        else:
            self.demon_1.set_health(self.health_demon_1)

    def update_demon_2(self):
        if self.health_demon_2:
            next_x, next_y = self.demon_2.get_position()
            up_enemy, down_enemy = self.demon_2.get_flags()

            if up_enemy:
                if self.labyrinth.is_free((next_x, next_y + 1)):
                    next_y += 1
                    self.demon_2.set_position((next_x, next_y))
                else:
                    down_enemy = True
                    up_enemy = False
                    self.demon_2.set_flags((up_enemy, down_enemy))
            elif down_enemy:
                if self.labyrinth.is_free((next_x, next_y - 1)):
                    next_y -= 1
                    self.demon_2.set_position((next_x, next_y))
                else:
                    down_enemy = False
                    up_enemy = True
                    self.demon_2.set_flags((up_enemy, down_enemy))
        else:
            self.demon_2.set_health(self.health_demon_2)

    def update_demon_3(self):
        if self.health_demon_3:
            next_x, next_y = self.demon_3.get_position()
            up_enemy, down_enemy = self.demon_3.get_flags()

            if up_enemy:
                if self.labyrinth.is_free((next_x, next_y + 1)):
                    next_y += 1
                    self.demon_3.set_position((next_x, next_y))
                else:
                    down_enemy = True
                    up_enemy = False
                    self.demon_3.set_flags((up_enemy, down_enemy))
            elif down_enemy:
                if self.labyrinth.is_free((next_x, next_y - 1)):
                    next_y -= 1
                    self.demon_3.set_position((next_x, next_y))
                else:
                    down_enemy = False
                    up_enemy = True
                    self.demon_3.set_flags((up_enemy, down_enemy))
        else:
            self.demon_3.set_health(self.health_demon_3)

    def update_demon_4(self):
        if self.health_demon_4:
            next_x, next_y = self.demon_4.get_position()
            up_enemy, down_enemy = self.demon_4.get_flags()

            if up_enemy:
                if self.labyrinth.is_free((next_x, next_y + 1)):
                    next_y += 1
                    self.demon_4.set_position((next_x, next_y))
                else:
                    down_enemy = True
                    up_enemy = False
                    self.demon_4.set_flags((up_enemy, down_enemy))
            elif down_enemy:
                if self.labyrinth.is_free((next_x, next_y - 1)):
                    next_y -= 1
                    self.demon_4.set_position((next_x, next_y))
                else:
                    down_enemy = False
                    up_enemy = True
                    self.demon_4.set_flags((up_enemy, down_enemy))
        else:
            self.demon_4.set_health(self.health_demon_4)

    def update_enemy(self):
        if self.health_enemy:
            next_x, next_y = self.enemy.get_position()
            right_enemy, left_enemy = self.enemy.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy.set_flags((right_enemy, left_enemy))
        else:
            self.enemy.set_health(self.health_enemy)

    def update_enemy_2(self):
        if self.health_enemy_2:
            next_x, next_y = self.enemy_2.get_position()
            right_enemy, left_enemy = self.enemy_2.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_2.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_2.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_2.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_2.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_2.set_health(self.health_enemy_2)

    def update_enemy_3(self):
        if self.health_enemy_3:
            next_x, next_y = self.enemy_3.get_position()
            right_enemy, left_enemy = self.enemy_3.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_3.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_3.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_3.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_3.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_3.set_health(self.health_enemy_3)

    def update_enemy_4(self):
        if self.health_enemy_4:
            next_x, next_y = self.enemy_4.get_position()
            right_enemy, left_enemy = self.enemy_4.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_4.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_4.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_4.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_4.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_4.set_health(self.health_enemy_4)

    def update_enemy_5(self):
        if self.health_enemy_5:
            next_x, next_y = self.enemy_5.get_position()
            right_enemy, left_enemy = self.enemy_5.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_5.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_5.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_5.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_5.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_5.set_health(self.health_enemy_5)

    def update_enemy_6(self):
        if self.health_enemy_6:
            next_x, next_y = self.enemy_6.get_position()
            right_enemy, left_enemy = self.enemy_6.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_6.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_6.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_6.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_6.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_6.set_health(self.health_enemy_6)

    def update_enemy_7(self):
        if self.health_enemy_7:
            next_x, next_y = self.enemy_7.get_position()
            right_enemy, left_enemy = self.enemy_7.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_7.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_7.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_7.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_7.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_7.set_health(self.health_enemy_7)

    def update_enemy_8(self):
        if self.health_enemy_8:
            next_x, next_y = self.enemy_8.get_position()
            right_enemy, left_enemy = self.enemy_8.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_8.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_8.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_8.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_8.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_8.set_health(self.health_enemy_8)

    def update_enemy_9(self):
        if self.health_enemy_9:
            next_x, next_y = self.enemy_9.get_position()
            right_enemy, left_enemy = self.enemy_9.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_9.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_9.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_9.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_9.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_9.set_health(self.health_enemy_9)

    def update_enemy_10(self):
        if self.health_enemy_10:
            next_x, next_y = self.enemy_10.get_position()
            right_enemy, left_enemy = self.enemy_10.get_flags()
            if right_enemy:
                if self.labyrinth.is_free((next_x + 1, next_y)):
                    next_x += 1
                    self.enemy_10.set_position((next_x, next_y))
                else:
                    left_enemy = True
                    right_enemy = False
                    self.enemy_10.set_flags((right_enemy, left_enemy))
            elif left_enemy:
                if self.labyrinth.is_free((next_x - 1, next_y)):
                    next_x -= 1
                    self.enemy_10.set_position((next_x, next_y))
                else:
                    left_enemy = False
                    right_enemy = True
                    self.enemy_10.set_flags((right_enemy, left_enemy))
        else:
            self.enemy_10.set_health(self.health_enemy_10)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        right, left, up, down = self.hero.get_flags()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            left = True
            right = False
            down = False
            up = False
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            left = False
            right = True
            down = False
            up = False
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            left = False
            right = False
            down = False
            up = True
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            left = False
            right = False
            down = True
            up = False
            next_y += 1
        if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_flags((right, left, up, down))
            self.hero.set_position((next_x, next_y))

    def check_health(self):

        right, left, up, down = self.hero.get_flags()
        right_enemy, left_enemy = self.enemy.get_flags()
        right_enemy_2, left_enemy_2 = self.enemy_2.get_flags()
        right_enemy_3, left_enemy_3 = self.enemy_3.get_flags()
        right_enemy_4, left_enemy_4 = self.enemy_4.get_flags()
        right_enemy_5, left_enemy_5 = self.enemy_5.get_flags()
        right_enemy_6, left_enemy_6 = self.enemy_6.get_flags()
        right_enemy_7, left_enemy_7 = self.enemy_7.get_flags()
        right_enemy_8, left_enemy_8 = self.enemy_8.get_flags()
        right_enemy_9, left_enemy_9 = self.enemy_9.get_flags()
        right_enemy_10, left_enemy_10 = self.enemy_10.get_flags()
        up_enemy, down_enemy = self.demon.get_flags()
        up_enemy_1, down_enemy_1 = self.demon_1.get_flags()
        up_enemy_2, down_enemy_2 = self.demon_2.get_flags()
        up_enemy_3, down_enemy_3 = self.demon_3.get_flags()
        up_enemy_4, down_enemy_4 = self.demon_4.get_flags()
        if self.health == 0:
            self.game_over = 3
        if self.enemy.get_position() == self.hero.get_position() and \
                (right == left_enemy or left == right_enemy) and self.health_enemy:
            self.health -= 1

        elif self.enemy.get_position() == self.hero.get_position() and (right == right_enemy or left == right_enemy):
            if self.health_enemy:
                self.number_of_opponents -= 1
            self.health_enemy = False

        if self.enemy_2.get_position() == self.hero.get_position() and \
                (right == left_enemy_2 or left == right_enemy_2) and self.health_enemy_2:
            self.health -= 1

        elif self.enemy_2.get_position() == self.hero.get_position() and \
                (right == right_enemy_2 or left == right_enemy_2):
            if self.health_enemy_2:
                self.number_of_opponents -= 1
            self.health_enemy_2 = False

        if self.enemy_3.get_position() == self.hero.get_position() and \
                (right == left_enemy_3 or left == right_enemy_3) and self.health_enemy_3:
            self.health -= 1

        elif self.enemy_3.get_position() == self.hero.get_position() and \
                (right == right_enemy_3 or left == right_enemy_3):
            if self.health_enemy_3:
                self.number_of_opponents -= 1
            self.health_enemy_3 = False

        if self.enemy_4.get_position() == self.hero.get_position() and \
                (right == left_enemy_4 or left == right_enemy_4) and self.health_enemy_4:
            self.health -= 1

        elif self.enemy_4.get_position() == self.hero.get_position() and \
                (right == right_enemy_4 or left == right_enemy_4):
            if self.health_enemy_4:
                self.number_of_opponents -= 1
            self.health_enemy_4 = False

        if self.enemy_5.get_position() == self.hero.get_position() and \
                (right == left_enemy_5 or left == right_enemy_5) and self.health_enemy_5:
            self.health -= 1

        elif self.enemy_5.get_position() == self.hero.get_position() and \
                (right == right_enemy_5 or left == right_enemy_5):
            if self.health_enemy_5:
                self.number_of_opponents -= 1
            self.health_enemy_5 = False

        if self.enemy_6.get_position() == self.hero.get_position() and \
                (right == left_enemy_6 or left == right_enemy_6) and self.health_enemy_6:
            self.health -= 1

        elif self.enemy_6.get_position() == self.hero.get_position() and \
                (right == right_enemy_6 or left == right_enemy_6):
            if self.health_enemy_6:
                self.number_of_opponents -= 1
            self.health_enemy_6 = False

        if self.enemy_7.get_position() == self.hero.get_position() and \
                (right == left_enemy_7 or left == right_enemy_7) and self.health_enemy_7:
            self.health -= 1

        elif self.enemy_7.get_position() == self.hero.get_position() and \
                (right == right_enemy_7 or left == right_enemy_7):
            if self.health_enemy_7:
                self.number_of_opponents -= 1
            self.health_enemy_7 = False

        if self.enemy_8.get_position() == self.hero.get_position() and \
                (right == left_enemy_8 or left == right_enemy_8) and self.health_enemy_8:
            self.health -= 1

        elif self.enemy_8.get_position() == self.hero.get_position() and \
                (right == right_enemy_8 or left == right_enemy_8):
            if self.health_enemy_8:
                self.number_of_opponents -= 1
            self.health_enemy_8 = False

        if self.enemy_9.get_position() == self.hero.get_position() and \
                (right == left_enemy_9 or left == right_enemy_9) and self.health_enemy_9:
            self.health -= 1

        elif self.enemy_9.get_position() == self.hero.get_position() and \
                (right == right_enemy_9 or left == right_enemy_9):
            if self.health_enemy_9:
                self.number_of_opponents -= 1
            self.health_enemy_9 = False

        if self.enemy_10.get_position() == self.hero.get_position() and \
                (right == left_enemy_10 or left == right_enemy_10) and self.health_enemy_10:
            self.health -= 1

        elif self.enemy_10.get_position() == self.hero.get_position() and \
                (right == right_enemy_10 or left == right_enemy_10):
            if self.health_enemy_10:
                self.number_of_opponents -= 1
            self.health_enemy_10 = False

        if self.demon.get_position() == self.hero.get_position() and \
                (down != up_enemy or up != down_enemy) and self.health_demon:
            self.health -= 1

        elif self.demon.get_position() == self.hero.get_position() and (down == up_enemy or up == down_enemy):
            if self.health_demon:
                self.number_of_opponents -= 1
            self.health_demon = False

        if self.demon_1.get_position() == self.hero.get_position() and \
                (down != up_enemy_1 or up != down_enemy_1) and self.health_demon_1:
            self.health -= 1

        elif self.demon_1.get_position() == self.hero.get_position() and (down == up_enemy_1 or up == down_enemy_1):
            if self.health_demon_1:
                self.number_of_opponents -= 1
            self.health_demon_1 = False

        if self.demon_2.get_position() == self.hero.get_position() and \
                (down != up_enemy_2 or up != down_enemy_2) and self.health_demon_2:
            self.health -= 1

        elif self.demon_2.get_position() == self.hero.get_position() and (down == up_enemy_2 or up == down_enemy_2):
            if self.health_demon_2:
                self.number_of_opponents -= 1
            self.health_demon_2 = False

        if self.demon_3.get_position() == self.hero.get_position() and \
                (down != up_enemy_3 or up != down_enemy_3) and self.health_demon_3:
            self.health -= 1

        elif self.demon_3.get_position() == self.hero.get_position() and (down == up_enemy_3 or up == down_enemy_3):
            if self.health_demon_3:
                self.number_of_opponents -= 1
            self.health_demon_3 = False

        if self.demon_4.get_position() == self.hero.get_position() and \
                (down != up_enemy_4 or up != down_enemy_4) and self.health_demon_4:
            self.health -= 1

        elif self.demon_4.get_position() == self.hero.get_position() and (down == up_enemy_4 or up == down_enemy_4):
            if self.health_demon_4:
                self.number_of_opponents -= 1
            self.health_demon_4 = False

    def check_game_over(self, screen):
        if self.game_over == 3:
            self.is_paused = 1
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 150)
            text = font.render(f"YOU DIED", True, (255, 0, 0))
            screen.blit(text, (180, 300))
        elif self.game_over == 1:
            self.is_paused = 1
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 50)
            text = font.render(f"Поздравляем! Вы спасли принцессу!", True, (53, 201, 43))
            screen.blit(text, (50, 50))
            prinzesa = pygame.image.load('принцесса.jpg')
            screen.blit(prinzesa, (0, 120))
        elif self.game_over == 2:
            self.is_paused = 1
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 35)
            text = font.render(f"Вы спасли принцессу, но на выходе из лабиринта ее убили", True, (255, 0, 0))
            screen.blit(text, (50, 50))
            prinzesa_ = pygame.image.load('принцессаумерла.jpg')
            screen.blit(prinzesa_, (0, 120))


def main():
    pygame.init()
    pygame.display.set_caption('Knights')
    screen = pygame.display.set_mode(Window_SIZE)

    labyrinth = Labyrinth("map.txt", [0, 2], 2)
    hero = Hero((12, 23))
    enemy = Enemy((1, 1))
    enemy_2 = Enemy((3, 3))
    enemy_3 = Enemy((3, 17))
    enemy_4 = Enemy((3, 15))
    enemy_5 = Enemy((5, 13))
    enemy_6 = Enemy((14, 21))
    enemy_7 = Enemy((14, 11))
    enemy_8 = Enemy((14, 7))
    enemy_9 = Enemy((14, 5))
    enemy_10 = Enemy((23, 1))
    demon = Demon((1, 1), False)
    demon_1 = Demon((23, 1), True)
    demon_2 = Demon((21, 3), True)
    demon_3 = Demon((14, 14), False)
    demon_4 = Demon((8, 21), True)
    game = Game(labyrinth, hero, enemy, demon, enemy_2, enemy_3, enemy_4, enemy_5, enemy_6, enemy_7, enemy_8, enemy_9,
                enemy_10, demon_1, demon_2, demon_3, demon_4)

    with open(f"{DATA_GAME}/save.dat", "wb") as file:
        pickle.dump(game, file)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == TIMER_EVENT_TYPE:
                game.update_demon()
                game.update_demon_1()
                game.update_demon_2()
                game.update_demon_3()
                game.update_demon_4()
                game.update_enemy()
                game.update_enemy_2()
                game.update_enemy_3()
                game.update_enemy_4()
                game.update_enemy_5()
                game.update_enemy_6()
                game.update_enemy_7()
                game.update_enemy_8()
                game.update_enemy_9()
                game.update_enemy_10()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open(f"{DATA_DIR}/save.dat", "wb") as file:
                        pickle.dump(game, file)
                if event.key == pygame.K_l:
                    with open(f"{DATA_DIR}/save.dat", "rb") as file:
                        game = pickle.load(file)
                if event.key == pygame.K_w:
                    with open(f"{DATA_GAME}/save.dat", "rb") as file:
                        game = pickle.load(file)
        game.check_health()
        game.render(screen)
        game.update_hero()
        game.check_game_over(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()