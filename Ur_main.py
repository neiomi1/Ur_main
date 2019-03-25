import os
import pygame
import math
import random
import time

os.environ['SDL_VIDEO_CENTERED'] = "1"

pygame.init()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def get_size(self):
        return [self.rect[2], self.rect[3]]


class GamePiece(pygame.sprite.Sprite):
    def __init__(self, player, width):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = pygame.Surface([width, width])
        self.image.fill(blue)
        self.image.set_colorkey(blue)
        self.radius = int(width/2)
        self.distance = None
        self.speed = 0.2
        self.vector = None
        self.target_location = None

        if player == 1:
            pygame.draw.circle(self.image, white, (self.radius, self.radius), self.radius-5, 0)
        else:
            pygame.draw.circle(self.image, black, (self.radius, self.radius), self.radius-5, 0)
        self.rect = self.image.get_rect()

    def update(self, delta):
        if self.target_location:
            travelled = math.hypot(self.vector[0]*deltaTime, self.vector[1] * deltaTime)
            # print("-------------------------")
            # print(travelled)
            self.distance -= travelled
            # print(self.distance)
            if self.distance < 0:
                self.rect.x = self.target_location[0]
                self.rect.y = self.target_location[1]
                self.target_location = None
            else:
                # print(self.vector[0])
                # print(deltaTime)
                self.rect[0] += self.vector[0] * deltaTime
                self.rect[1] += self.vector[1] * deltaTime
                # print(self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, location):
        x = location[0] - self.rect[0]
        y = location[1] - self.rect[1]
        self.distance = math.hypot(x, y)
        # print(self.distance)
        try:
            self.vector = self.speed * x / self.distance, self.speed * y / self.distance
            self.target_location = list(location)
        except ZeroDivisionError:
            pass


background = Background("test_2_flipped.png", (0, 0))

label_font = pygame.font.Font("./assets/Kaldevaderibbon.ttf", 100)
label_font_2 = pygame.font.Font("./assets/Quiska Personal Use Only.ttf", 50)
# label_font.set_italic(False)

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
beige_1 = (190, 173, 153)
beige_2 = (159, 143, 118)
label = label_font.render("Throw(the(dice!", True, black)


box_size = int(background.get_size()[0]/12)
print(box_size)

all_sprites_list = pygame.sprite.Group()

tiles = [None]*50
occupied = [None]*50
for i in range(1, 51):
    if i < 3:
        tiles[i-1] = ((i+1)*86, 2*86)
    elif 7 > i > 2:
        tiles[i-1] = ((i+3)*86, 2*86)
    elif 15 > i > 6:
        tiles[i-1] = ((i-5)*86, 3*86)
    elif 17 > i > 14:
        tiles[i-1] = ((i-13)*86, 4*86)
    elif i == 21:
        tiles[20] = (4*86, 2*86)
    elif i == 22:
        tiles[21] = (4*86, 4*86)
    elif 30 > i > 22:
        tiles[i-1] = (0, (i-23)*86)
    elif 37 > i > 29:
        tiles[i-1] = ((i-26)*86, 6*86)
    elif 44 > i > 35:
        tiles[i-1] = (11*86, (i-37)*86)
    elif 51 > i > 43:
        tiles[i-1] = ((i-43)*86, 0)
    else:
        tiles[i-1] = ((i-11)*86, 4*86)

print(tiles)
pieces = {}
for x in range(1, 15):
    if x < 8:
        placeholder = GamePiece(0, box_size)
        placeholder.rect.x = 86*x
        placeholder.rect.y = 0
        all_sprites_list.add(placeholder)
        pieces["black_piece{0}".format(x)] = placeholder
        print(placeholder.rect[0:2])
        occupied[x+42] = 0
    else:
        placeholder = GamePiece(1, box_size)
        placeholder.rect.x = (x-4)*86
        placeholder.rect.y = 516
        all_sprites_list.add(placeholder)
        pieces["white_piece{0}".format(x-7)] = placeholder
        occupied[x+21] = 1
print(occupied)


def check_tile(coordinates):
    if coordinates[1] < 86 and 9*86 > coordinates[0] >= 1*86:
        return -1
    elif 3*86 > coordinates[1] >= 2*86:
        if 5*86 > coordinates[0] >= 4*86:
            return 20
        elif 4*86 > coordinates[0]:
            for n in range(3, 5):
                if n * 86 > coordinates[0] >= (n-1)*86:
                    return n - 2
        elif 10*86 > coordinates[0] >= 6*86:
            for n in range(7, 11):
                if n*86 > coordinates[0] >= (n-1)*86:
                    return n - 4
        else:
            pass
    elif 4*86 > coordinates[1] >= 3*86:
        if 11*86 > coordinates[0] >= 2*86:
            for n in range(3, 11):
                if n*86 > coordinates[0] >= (n-1)*86:
                    return n + 4
        else:
            pass
    elif 5*86 > coordinates[1] >= 4*86:
        if 5 * 86 > coordinates[0] >= 4 * 86:
            return 21
        elif 4 * 86 > coordinates[0]:
            for n in range(3, 5):
                if n * 86 > coordinates[0] >= (n - 1) * 86:
                    return n + 12
        elif 10 * 86 > coordinates[0] >= 6 * 86:
            for n in range(7, 11):
                if n * 86 > coordinates[0] >= (n - 1) * 86:
                    return n + 10
        else:
            pass
    elif 7*86 > coordinates[1] >= 6*86 and 11*86 > coordinates[0] >= 2*86:
        return -2
    else:
        pass


def button(message, x_coord, y_coord, width, height, colour, hovered_colour, action=None):
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if x_coord + width > mouse_pos[0] >= x_coord and y_coord + height > mouse_pos[1] >= y_coord:
        pygame.draw.rect(gameDisplay, hovered_colour, (x_coord, y_coord, width, height))
        if clicked[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, colour, (x_coord, y_coord, width, height))
    text = label_font.render(message, True, black)
    rect = text.get_rect()
    rect.center = ((x_coord + (width/2)), (y_coord+(height/2)))
    gameDisplay.blit(text, rect)


def dice_roll():
    print("Rolling")
    global dice
    if dice is None:
        dice = 0
        for m in range(1, 5):
            dice += random.randint(0, 1)


def display_message(message, x_coord, y_coord, width, height, colour):
    pygame.draw.rect(gameDisplay, colour, (x_coord, y_coord, width, height))
    text = label_font_2.render(message, True, black)
    rect = text.get_rect()
    rect.center = ((x_coord + (width/2)), (y_coord+(height/2)))
    gameDisplay.blit(text, rect)


def swap_players():
    global player_turn
    if player_turn == 1:
        player_turn = 0
    elif player_turn == 0:
        player_turn = 1


def check_collision(player_turn, location):
    if occupied[location] == player_turn:
        return 0
    elif occupied[location] is None:
        return 1
    else:
        return 2


def check_rosetta(tile):
    if tile in [1, 5, 10, 15, 19]:
        return True
    else:
        False


def new_game():
    global game_done, game_end, winner, to_move, dice, tile_location, to_kill, to_kill_location, move_done, safe, killed, player2_safe, player_turn, player1_safe, occupied
    w = 0
    occupied = 50*[None]
    for key in pieces.keys():
        if w < 7:
            pieces[key].rect.x = (w+1)*86
            pieces[key].rect.y = 0
            occupied[w+43] = 0
            w += 1
        elif w < 13:
            pieces[key].rect.x = (w-3)*86
            pieces[key].rect.y = 6*86
            occupied[w+29] = 1
            w += 1
    game_done = game_end = safe = killed = False
    player1_safe = player2_safe = player_turn = 0
    winner = to_move = dice = tile_location = to_kill = to_kill_location = None
    move_done = True


def check_possible_move(player_turn, dice):
    print(player_turn, dice)
    for piece in all_sprites_list:
        if player_turn == 0:
            if piece.player == player_turn:
                player_tile = tiles.index(tuple(piece.rect[0:2]))
                print("black")
                print(piece.rect)
                print(player_tile, player_tile+dice)
                if player_tile > 42 and occupied[player1_board[dice - 1] - 1] != 0:
                    return True
                elif player_tile < 22 and occupied[player_tile + dice] != 0  and player1_board.index(player_tile+1) + dice < 15:
                        return True

        elif player_turn == 1:
            if piece.player == player_turn and dice is not None:
                player_tile = tiles.index(tuple(piece.rect[0:2]))
                print("white")
                print(piece.rect)
                print(player_tile, player_tile+1)
                if 36 > player_tile > 28 and occupied[player2_board[dice-1]-1] != 0:
                    return True
                elif player_tile < 29 and occupied[player_tile + dice] != 1  and player2_board.index(player_tile+1) + dice < 15:
                    return True
    return False


print(pieces)
print(all_sprites_list)
# piece2 = GamePiece(0, box_size)
# piece2.rect.x = box_size * 3
# piece2.rect.y = box_size*3
# all_sprites_list.add(piece2)


# print(gameboard)
player1_board = [3, 4, 5, 6, 14, 13, 12, 11, 10, 9, 8, 7, 1, 2, 21]
player2_board = [17, 18, 19, 20, 14, 13, 12, 11, 10, 9, 8, 7, 15, 16, 22]

gameDisplay = pygame.display.set_mode(background.get_size(), 0, 0)
# print(gameDisplay.get_size())
# gameDisplay.blit(background_board)
pygame.display.set_caption("Ur")
# gameDisplay.fill(white)

clock = pygame.time.Clock()
game_done = False
# print(piece)
# gameDisplay.fill(white)
# gameDisplay.blit(background_board_scaled, (0, 0))
# pygame.draw.circle(gameDisplay, white, (x, y), 25, 0)
# pygame.display.flip()
# time.sleep(20)
player_turn = 0
move_done = True
dice = None
print(box_size)
print(tiles[49])
# y = int(box_size/2)
to_move = None
#click = (86, 86)
getTicksLastFrame = 0
tile_location = None
player1_safe = player2_safe = 0
safe = False
killed = False
to_kill = None
to_kill_location = None
game_end = False
rosetta = False
winner = "Black"
while not game_done:
    # event loop
    gameDisplay.fill(white)
    gameDisplay.blit(background.image, background.rect)
    if game_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        message = winner + "(wins!"
        pygame.draw.rect(gameDisplay, beige_2, (86, 86, 10*86, 7*86))
        message = label_font.render(message, True, black)
        rect = message.get_rect()
        rect.center = ((86 + (10*86 / 2)), (86 + (7*86 / 2)))
        gameDisplay.blit(message, rect)
        button("New(game?", 3.5*86, 6*86, 5*86, 86, beige_2, beige_1, new_game)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP and move_done and dice is not None:
                print("---------------------")
                click = event.pos
                # for s in all_sprites_list: print(type(s.rect))
                clicked_sprites = [s for s in all_sprites_list if s.rect.collidepoint(event.pos)]
                # try: click = tiles.index(click)
                # except ValueError: pass
                try: to_move = clicked_sprites[0]
                except IndexError: pass
                # if move_done and dice != 5:
                #         pass

        if dice is not None and dice == 0:
            swap_players()
            print("------------------------------------------------")
            print("Swapping", player_turn)
            print("-------------------------------------------------")
            move_done = True
            dice_display = "0, unlucky!"
            display_message(dice_display, 258, 688, 6 * 86, 86, beige_2)
            all_sprites_list.draw(gameDisplay)
            pygame.display.update()
            time.sleep(2)
            dice = None
            dice_display = "Player {0}".format(player_turn)
            display_message(dice_display, 258, 688, 6 * 86, 86, beige_2)
            time.sleep(1)

        if dice is not None and move_done and not killed:
            check = check_possible_move(player_turn, dice)
            if not check:
                dice = None
                swap_players()

        if to_move is not None and move_done and dice is not None and not killed and check:
            print("click", player_turn, to_move.player)
            if player_turn == to_move.player:
                placeholder = tile_location = check_tile(click)
                if tile_location is not None:
                    print(tile_location, player_turn)
                    if player_turn == 0:
                        print("move_done", move_done)
                        if tile_location < 0:
                            print("Starter")
                            tile = player1_board[dice-1]-1
                            print(occupied[tile], tile, placeholder)
                            if check_collision(player_turn, tile) == 1:
                                tile_location = tiles[tile]
                                occupied[tile] = 0
                                occupied[tiles.index(tuple(to_move.rect[0:2]))] = None
                                rosetta = check_rosetta(tile)
                                print(occupied)
                                move_done = False
                        elif player1_board.index(tile_location) + dice < 15:
                            print("Not starter")
                            tile_location = player1_board.index(tile_location) + dice
                            tile = player1_board[tile_location] - 1
                            check = check_collision(player_turn, tile)
                            print(check)
                            if check == 1:
                                if tile_location == 14:
                                    safe = True
                                    player1_safe += 1
                                move_done = False
                            elif check == 2:
                                print("kill detected")
                                killed = True
                                for n in all_sprites_list:
                                    print(n.rect[0:2], tiles[tile], n.player)
                                    if n.player != player_turn and tuple(n.rect[0:2]) == tiles[tile]:
                                        print("found")
                                        to_kill = n
                                move_done = False
                            if not move_done:
                                rosetta = check_rosetta(tile)
                                print(occupied)
                                tile_location = tiles[tile]
                                occupied[tile] = 0
                                occupied[placeholder-1] = None
                                print(placeholder)
                                print(occupied)
                                print(tile)
                                print(tile_location)
                    elif player_turn == 1:
                        if tile_location < 0:
                            tile = player2_board[dice - 1] - 1
                            if check_collision(player_turn, tile) == 1:
                                tile_location = tiles[tile]
                                occupied[tile] = 1
                                occupied[tiles.index(tuple(to_move.rect[0:2]))] = None
                                rosetta = check_rosetta(tile)
                                move_done = False
                        elif player2_board.index(tile_location) + dice < 15:
                            tile_location = player2_board.index(tile_location) + dice
                            tile = player2_board[tile_location] - 1
                            check = check_collision(player_turn, tile)
                            if check == 1:
                                if tile_location == 14:
                                    safe = True
                                    player2_safe += 1
                                move_done = False
                            elif check == 2:
                                print("kill detected")
                                killed = True
                                for n in all_sprites_list:
                                    print(n.rect[0:2], tiles[tile], n.player)
                                    if n.player != player_turn and tuple(n.rect[0:2]) == tiles[tile]:
                                        print("found")
                                        to_kill = n
                                move_done = False
                            if not move_done:
                                rosetta = check_rosetta(tile)
                                print(occupied)
                                tile_location = tiles[tile]
                                occupied[tile] = 1
                                occupied[placeholder-1] = None
                                print(placeholder)
                                print(occupied)
                                print(tile)

        if not move_done and to_move is not None and tile_location is not None:
            to_move.move(tile_location)
            # print("moving")
            # print(tuple(to_move.rect[0:2]), " ", tile_location)
            if tuple(to_move.rect[0:2]) == tile_location:
                if safe:
                    occupied[tiles.index(tile_location)] = None
                    if player_turn == 0:
                        tile_location = tiles.index(tile_location)
                        tile_location = tiles[tile_location+player1_safe+1]
                        occupied[tiles.index(tile_location)] = 0
                    elif player_turn == 1:
                        tile_location = tiles.index(tile_location)
                        tile_location = tiles[tile_location+player2_safe+14]
                        occupied[tiles.index(tile_location)] = 1
                    safe = False
                elif rosetta:
                    dice = None
                    tile_location = None
                    move_done = True
                    rosetta = False
                    to_move = None
                else:
                    move_done = True
                    print("------------------------------------------------")
                    print("Swapping", player_turn)
                    print("-------------------------------------------------")
                    swap_players()
                    tile_location = None
                    dice = None
                    to_move = None

        if to_kill is not None and killed is True and move_done is True:
            print(to_kill)
            print("killing", occupied)
            print(to_kill.player, tuple(to_kill.rect[0:2]), to_kill_location)
            if to_kill.player == 0:
                for n in range(1, 8):
                    if check_collision(to_kill.player, n+42) == 1 and to_kill_location is None:
                        print("free spot")
                        to_kill_location = tiles[n+42]
                to_kill.move(to_kill_location)
            else:
                for n in range(1, 8):
                    if check_collision(to_kill.player, n+28) == 1 and to_kill_location is None:
                        to_kill_location = tiles[n+28]
                to_kill.move(to_kill_location)
            if tuple(to_kill.rect[0:2]) == to_kill_location:
                killed = False
                occupied[tiles.index(to_kill_location)] = player_turn
                to_kill_location = None

        if player1_safe == 7:
            game_end = True
            winner = "Black"
        elif player2_safe == 7:
            game_end = True
            winner = "White"
        # to_move = [s for s in all_sprites_list]
        # for i in range(0,len(to_move)):
        #     to_move[i].move(tiles[x])
        # if x <= 35:
        #     # print(tiles[x])
        #     pieces['black_piece1'].move(tiles[x])
        #     # print(tiles[x], pieces['black_piece1'].rect[0:2])
        #     # print(type(pieces['black_piece1'].rect))
        #     if tuple(pieces['black_piece1'].rect[0:2]) == tiles[x] and x < 35:
        #         print(x)
        #         x += 1

        # delta time for movement
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame)
        getTicksLastFrame = t
        all_sprites_list.update(deltaTime)
        # screen refresh

        button("Throw(the(dice!", 258, 602, 6*86, 86, beige_2, beige_1, dice_roll)
        if player_turn == 0:
            player = "black"
        else:
            player = "white"
        if dice is None:
            dice_display = player + "'s turn"
        else:
            dice_display = player + ":  {0}".format(dice)
        display_message(dice_display, 258, 688, 6*86, 86, beige_2)
        all_sprites_list.draw(gameDisplay)




    # for w in range(0, 2000, box_size):
    #     pygame.draw.line(gameDisplay, black, (w, 0), (w, 2000))
    # for w in range(0, 2000, box_size):
    #     pygame.draw.line(gameDisplay, black, (0, w), (2000, w))
    # pygame.draw.line(gameDisplay, black, (x2, 0), (x2, 2000))
    # for w in range(0, 1034, 86):
    #     pygame.draw.circle(gameDisplay, white, (w+z, z), z-5, 0)
    pygame.display.flip()
    clock.tick(60)
# def adjust_gameboard(x, y):
#     box_size = display_height/7
#     temp_x = 0
#     t
#     for i in range(1,20):
#         if
#
#
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         pygame.quit()
#         quit()
