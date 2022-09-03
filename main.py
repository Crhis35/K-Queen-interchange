import random
from PIL import Image, ImageDraw

images = []
num = int(input('Size of matrix to draw: '))

zoom = 20
borders = 6


queens = []


def gen_board(deck, num: int):

    matrix = [[0 for i in range(num)] for j in range(num)]

    for pos in deck.values():
        matrix[pos[0]][pos[1]] = 1

    for line in matrix:
        print('  '.join(map(str, line)))

    return matrix


def draw_matrix(a, the_path=[]):
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255)
            r = 0
            if a[i][j] == 1:
                color = (0, 0, 0)
            if i == start_j and j == start_j:
                color = (0, 255, 0)
                r = borders
            if i == end_i and j == end_j:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom -
                           r-1, i*zoom+zoom-r-1), fill=color)
            if a[i][j] == 2:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                             fill=(128, 128, 128))
    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
    draw.rectangle(
        (0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0, 255, 0), width=2)
    images.append(im)


def go_to(i, j,):
    global path_so_far, end_i, end_j, a, m
    if i < 0 or j < 0 or i > len(a)-1 or j > len(a[0])-1:
        return
    # If we've already been there or there is a queen, quit
    if (i, j) in path_so_far or a[i][j] > 0:
        return
    path_so_far.append((i, j))
    a[i][j] = 2
    draw_matrix(a, path_so_far)
    if (i, j) == (end_i, end_j):
        print("Found!", path_so_far)
        queens.append(path_so_far)
        for animate in range(10):
            if animate % 2 == 0:
                draw_matrix(a, path_so_far)
            else:
                draw_matrix(a)
        path_so_far.pop()
        return
    else:
        go_to(i - 1, j)  # check top
        go_to(i + 1, j)  # check bottom
        go_to(i, j + 1)  # check right
        go_to(i, j - 1)  # check left
    path_so_far.pop()
    draw_matrix(a, path_so_far)
    return


def circular():
    while True:
        for connection in [i for i in range(4)]:
            yield connection


def get_initial_state(num: int):
    return {
        0: (0, 0),
        1: (num - 1, num - 1),
        2: (0, num - 1),
        3: (num - 1, 0),
    }


def get_final_state(num: int):
    return {
        0: (num - 1, 0),
        1: (0, 0),
        2: (num - 1, num - 1),
        3: (0, num - 1),
    }


def validate_pos(positions: dict, current_pos: tuple):
    for pos in positions.values():
        if pos[0] == current_pos[0] and pos[1] == current_pos[1]:
            return False
    return True


moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Queen moves from a position


deck = get_initial_state(num)
final_deck = get_final_state(num)
active_queen = circular()
i = 0

if num > 2:
    while len(queens) < 4 and i < 1e6:
        print('----------------------------------------------------------------')

        a = gen_board(deck, num)  # Generate board base on queen position
        idx = next(active_queen)  # Get current queen
        path_so_far = []  # Save path

        # Check if the destination is already blocked and random move a queen
        if not validate_pos(final_deck, deck[idx]):
            while True:
                random_move = random.choice(moves)
                current_move = (deck[idx][0] + random_move[0],
                                deck[idx][1] + random_move[1])
                if current_move[0] >= 0 and current_move[1] >= 0 and current_move[0] < num and current_move[1] < num:
                    deck[idx] = current_move
                    print('Turn queen {} from {} to {}'.format(
                        idx, deck[idx], current_move))
                    break
        else:
            print('Turn queen {} from {} to {}'.format(
                idx, deck[idx], final_deck[idx]))
            start_i, start_j = deck[idx]
            end_i, end_j = final_deck[idx]

            # Before start move set current queen position to 0
            a[start_i][start_j] = 0
            go_to(start_i, start_j)
        i += 1
    print('Iterations [{}]'.format(i))
    images[0].save('chessboard.gif',
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=50, loop=0)
else:
    print('Min size of 3')
