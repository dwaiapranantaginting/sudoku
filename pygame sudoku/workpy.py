import pygame as pg
import random
import copy

pg.init()
pg.mixer.init()

# Ukuran window
WIDTH = 1200
HEIGHT = 700

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku Alin")

# Icom dan suara
icon = pg.image.load("sudoku.jpg")
pg.display.set_icon(icon)
soundKalah = pg.mixer.Sound("losing.mp3")
angkabenar = pg.mixer.Sound("sound benar.wav")
angkasalah = pg.mixer.Sound("sound salah.wav")
soundmenang = pg.mixer.Sound("menang.wav")
soundkartuswap = pg.mixer.Sound("kartuswap.mp3")
kartuterklik = pg.mixer.Sound("clicked card.mp3")
healsfx = pg.mixer.Sound("healsfx.mp3")
revealsfx = pg.mixer.Sound("revealsfx.mp3")
scsfx = pg.mixer.Sound("2xsfx.mp3")


# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
DARK_GRAY = (160,160,160)
BLUE = (0, 128, 255)
RED = (220, 50, 50)
GREEN = (60, 180, 90)

baris = 9
kolom = 9
grid_size = 540
cell_size = grid_size // kolom
grid_x = 100
grid_y = 50
def membuat_grid():
    for i in range(baris + 1):
        if i % 3 == 0:
            tebal = 4
        else :
            tebal = 1

        # grid vertical (--)
        pg.draw.line(
            screen,
            BLACK,
            (grid_x + i * cell_size, grid_y),
            (grid_x + i * cell_size, grid_y + grid_size),
            tebal
        )

        # grid horizontal (||)
        pg.draw.line(
            screen,
            BLACK,
            (grid_x, grid_y + i * cell_size),
            (grid_x + grid_size, grid_y + i * cell_size),
            tebal
        )

barisTom = 3
kolomTom = 3
sizeTom = 330
cellTom = sizeTom // kolomTom
tomX = 700
tomY = 220
padding = 5      
radius = 15

def grid_tombol():
    angka = 1
    for r in range(barisTom):
        for c in range(kolomTom):
            
            x = tomX + c * cellTom
            y = tomY + r * cellTom
            w = cellTom - padding * 2
            h = cellTom - padding * 2
            pg.draw.rect(
                screen,
                GRAY,
                (x, y, w, h),
                border_radius = radius
            )
            text = font_tombol.render(str(angka), True, BLUE)
            rect = text.get_rect(
                center=(x + w//2, y + h//2)
            )
            screen.blit(text, rect)
            angka += 1

def deteksi_posisi_tombol(posisi):
    mx, my = posisi

    if tomX <= mx <= tomX + sizeTom and tomY <= my <= tomY + sizeTom:
        kolomDetTom = (mx - tomX) // cellTom
        barisDetTom = (my - tomY) // cellTom
        angkaDetTom = barisDetTom * 3 + kolomDetTom + 1
        return angkaDetTom
    return None

def cek_grid_sudoku(xypos):
    sx, sy = xypos

    if grid_x <= sx <= grid_x + grid_size and grid_y <= sy <= grid_y + grid_size :
        barisCek = (sy - grid_y) // cell_size
        kolomCek = (sx - grid_x) // cell_size
        return (barisCek, kolomCek)
    return None

def highlight_kotak():
    if kotak_aktif:
        r, c = kotak_aktif

        # highlight baris
        for col in range(9):
            x = grid_x + col * cell_size
            y = grid_y + r * cell_size
            pg.draw.rect(screen, (220,230,245), (x, y, cell_size, cell_size))

        # highlight kolom
        for row in range(9):
            x = grid_x + c * cell_size
            y = grid_y + row * cell_size
            pg.draw.rect(screen, (220,230,245), (x, y, cell_size, cell_size))

        # highlight kotak aktif (lebih biru)
        x = grid_x + c * cell_size
        y = grid_y + r * cell_size
        pg.draw.rect(screen, (170,200,230), (x, y, cell_size, cell_size))

def gambar_angka():
    for r in range(9):
        for c in range(9):

            angka = board[r][c]

            x = grid_x + c * cell_size
            y = grid_y + r * cell_size

            # STEP 2 — highlight angka yang sama
            if kotak_aktif:
                r_sel, c_sel = kotak_aktif
                angka_sel = board[r_sel][c_sel]

                if angka_sel != 0 and angka == angka_sel:
                    pg.draw.rect(
                        screen,
                        (210,220,235),
                        (x, y, cell_size, cell_size)
                    )

            # STEP 3 — highlight error
            if angka != 0 and original_board[r][c] == 0:
                if angka != solusi[r][c]:
                    pg.draw.rect(
                        screen,
                        (255,100,100),
                        (x, y, cell_size, cell_size)
                    )

            # warna angka
            warna = BLACK

            if angka != 0 and original_board[r][c] == 0 and angka != solusi[r][c]:
                warna = RED

            if angka != 0:
                text = font_grid.render(str(angka), True, warna)
                rect = text.get_rect(
                    center=(x + cell_size//2, y + cell_size//2)
                )
                screen.blit(text, rect)

def aman(grid, r, c, n):
    if n in grid[r]:
        return False
    for i in range(9):
        if grid[i][c] == n:
            return False
    br = (r // 3) * 3
    bc = (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[br+i][bc+j] == n:
                return False
    return True

def solve(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:

                angka = list(range(1,10))
                random.shuffle(angka)

                for n in angka:

                    if aman(grid, r, c, n):
                        grid[r][c] = n
                        if solve(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True

def count_solutions(grid, limit=2):
    count = 0

    def solve_count(g):
        nonlocal count

        for r in range(9):
            for c in range(9):
                if g[r][c] == 0:

                    for n in range(1,10):
                        if aman(g, r, c, n):
                            g[r][c] = n
                            solve_count(g)
                            g[r][c] = 0

                            if count >= limit:
                                return
                    return

        count += 1

    solve_count(copy.deepcopy(grid))
    return count

def isi_grid_random(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                angka = list(range(1,10))
                random.shuffle(angka)

                for n in angka:

                    if aman(grid, r, c, n):

                        grid[r][c] = n

                        if isi_grid_random(grid):
                            return True

                        grid[r][c] = 0

                return False

    return True

wave = 1
score = 0
def generate_soal():
    global board, solusi, original_board, jumlah_salah, game_over
    global error_cell, error_reason
    error_cell = None
    error_reason = []
    game_over = False

    grid = [[0 for _ in range(9)] for _ in range(9)]
    isi_grid_random(grid)
    solusi = copy.deepcopy(grid)
    if wave <= 3:
        kosong = random.randint(32, 36)

    elif wave <= 6:
        kosong = random.randint(36, 42)

    elif wave <= 10:
        kosong = random.randint(42, 48)

    else:
        kosong = random.randint(48, 52)

    attempt = 0

    while kosong > 0 and attempt < 500:
        attempt += 1

        r = random.randint(0,8)
        c = random.randint(0,8)
        if grid[r][c] != 0:
            backup = grid[r][c]
            grid[r][c] = 0
            if count_solutions(grid) != 1:
                grid[r][c] = backup
            else :
                kosong -= 1
    board = grid
    original_board = copy.deepcopy(board)

def gambar_tombol_newgame():
    if pg.time.get_ticks() - last_newgame_click < newgame_cooldown:
        gambarTOmbol = DARK_GRAY
    else :
        gambarTOmbol = GREEN
    pg.draw.rect(screen, gambarTOmbol, newgame_rect, border_radius=15)

    text = font_grid.render("NEW GAME", True, WHITE)
    rect = text.get_rect(center=newgame_rect.center)
    screen.blit(text, rect)

def gambar_kesalahan():

    # Title
    title = font_grid.render("Salah :", True, BLACK)
    screen.blit(title, (720, 30))

    start_x = 720
    y = 70
    size = 28
    gap = 12

    for i in range(3):

        x = start_x + i * (size + gap)

        if i < jumlah_salah:
            color = (180,40,40)
        else:
            color = (210,210,210)

        rect = pg.Rect(x, y, size, size)

        pg.draw.rect(screen, color, rect, border_radius=6)

        if i < jumlah_salah:
            pg.draw.line(screen, WHITE, (x+6,y+6),(x+size-6,y+size-6),2)
            pg.draw.line(screen, WHITE, (x+size-6,y+6),(x+6,y+size-6),2)

def gambar_gameover():
    if game_over:

        # overlay transparan
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        # shadow panel
        shadow = pg.Rect(
            gameover_rect.x + 6,
            gameover_rect.y + 6,
            gameover_rect.width,
            gameover_rect.height
        )
        pg.draw.rect(screen, (60,60,60), shadow, border_radius=20)

        # panel utama
        pg.draw.rect(screen, WHITE, gameover_rect, border_radius=20)
        pg.draw.rect(screen, BLACK, gameover_rect, 3, border_radius=20)

        # text GAME OVER
        text = font_grid.render("GAME OVER", True, RED)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(text, rect)

        # score
        score_text = font_grid.render(f"Score: {score}", True, BLACK)
        rect2 = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
        screen.blit(score_text, rect2)

        # tombol new game
        if pg.time.get_ticks() - gameover_time > 1500:
            warna_tombol = GREEN
        else :
            warna_tombol = (170, 170, 170)

        pg.draw.rect(screen, warna_tombol, gameover_button, border_radius=15)

        text2 = font_grid.render("NEW GAME", True, WHITE)
        rect3 = text2.get_rect(center=gameover_button.center)
        screen.blit(text2, rect3)

def highlight_error():
    global error_cell, error_reason

    if error_cell:
        r, c = error_cell
        x = grid_x + c * cell_size
        y = grid_y + r * cell_size
        pg.draw.rect(
            screen,
            (255,100,100),
            (x, y, cell_size, cell_size)
        )
        for tipe, rr, cc in error_reason:
            x = grid_x + cc * cell_size
            y = grid_y + rr * cell_size

            pg.draw.rect(
                screen,
                (255,200,200),
                (x, y, cell_size, cell_size)
            )
        if pg.time.get_ticks() - error_time > 800:
            error_cell = None
            error_reason = []

def cek_menang():
    for r in range(9):
        for c in range(9):
            if board[r][c] != solusi[r][c]:
                return False
    return True

def gambar_info():
    info_x = 720
    wave_y = 150
    score_y = 190
    wave_text = font_grid.render(f"Wave : {wave}", True, BLACK)
    screen.blit(wave_text, (info_x, wave_y))
    score_text = font_grid.render(f"Score : {score}", True, BLACK)
    screen.blit(score_text, (info_x, score_y))

def cek_konflik(r, c, angka):
    konflik = []

    # cek baris
    for col in range(9):
        if board[r][col] == angka:
            konflik.append(("row", r, col))

    # cek kolom
    for row in range(9):
        if board[row][c] == angka:
            konflik.append(("col", row, c))

    # cek box 3x3
    br = (r // 3) * 3
    bc = (c // 3) * 3

    for i in range(3):
        for j in range(3):
            rr = br + i
            cc = bc + j
            if board[rr][cc] == angka:
                konflik.append(("box", rr, cc))
    return konflik

def gambar_wave_clear():

    if wave_clear:

        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        text = font_grid.render("WAVE CLEAR!", True, GREEN)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
        screen.blit(text, rect)

        score_text = font_grid.render(f"+{100 * wave} SCORE", True, WHITE)
        rect2 = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
        screen.blit(score_text, rect2)

def generate_cards():
    global cards

    semua = ["reveal", "heal", "double"]
    cards = random.sample(semua, 2)

def gambar_cards():

    if not show_cards:
        return

    # dark background
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(170)
    overlay.fill((0,0,0))
    screen.blit(overlay,(0,0))

    # title
    title = font_grid.render("CHOOSE A CARD", True, WHITE)
    rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 200))
    screen.blit(title, rect)

    start_x = WIDTH//2 - 180
    y = HEIGHT//2 - 80

    mx, my = pg.mouse.get_pos()

    for i, card in enumerate(cards):

        x = start_x + i * 220
        rect = pg.Rect(x, y, 180, 220)

        hover = rect.collidepoint(mx, my)

        if hover:
            if not hovered_cards[i] :
                soundkartuswap.play()
                hovered_cards[i] = True

            rect.y -= 10
        else :
            hovered_cards[i] = False
        # shadow
        shadow = rect.move(6,6)
        pg.draw.rect(screen,(40,40,40),shadow,border_radius=15)

        # warna card
        if card == "reveal":
            color = (255,230,120)
            icon = "?"

        elif card == "heal":
            color = (140,255,160)
            icon = "+"

        else:
            color = (140,200,255)
            icon = "x2"

        # card body
        pg.draw.rect(screen,color,rect,border_radius=15)
        pg.draw.rect(screen,WHITE,rect,2,border_radius=15)

        # icon
        icon_font = pg.font.SysFont("sans-serif",50,True)
        icon_text = icon_font.render(icon,True,BLACK)
        icon_rect = icon_text.get_rect(center=(rect.centerx,rect.y+70))
        screen.blit(icon_text,icon_rect)

        # title
        name = font_grid.render(card.upper(),True,BLACK)
        name_rect = name.get_rect(center=(rect.centerx,rect.y+150))
        screen.blit(name,name_rect)

def apply_card(card):

    global jumlah_salah, score
    global card_effect, card_effect_time, effect_cell

    card_effect = card
    card_effect_time = pg.time.get_ticks()

    if card == "heal":
        jumlah_salah = max(0, jumlah_salah - 1)

    if card == "reveal":

        kosong = []

        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    kosong.append((r,c))

        if kosong:
            effect_cell = random.choice(kosong)

    if card == "double":
        score += 100

def next_wave():
    global kotak_aktif, show_cards
    kotak_aktif = None
    show_cards = False
    generate_soal()

def gambar_card_effect():

    global card_effect, effect_cell

    if card_effect is None:
        return

    elapsed = pg.time.get_ticks() - card_effect_time

    # efek heal
    if card_effect == "heal":

        alpha = max(0, 150 - elapsed//2)

        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill((100,255,100))

        screen.blit(overlay,(0,0))

    # efek reveal
    if card_effect == "reveal" and effect_cell:

        r,c = effect_cell

        x = grid_x + c * cell_size
        y = grid_y + r * cell_size

        pg.draw.rect(screen,(255,255,100),(x,y,cell_size,cell_size))

        if elapsed > 700:
            board[r][c] = solusi[r][c]
            effect_cell = None

    # selesai efek
    if elapsed > 800:
        card_effect = None

def gambar_inventory():

    title = font_grid.render("CARDS", True, BLACK)
    screen.blit(title, (900, 5))

    start_x = 900
    y = 40

    mx, my = pg.mouse.get_pos()

    for i, card in enumerate(inventory_cards):

        x = start_x + i * 120
        rect = pg.Rect(x, y, 110, 120)

        hover = rect.collidepoint(mx, my)

        # efek hover membesar
        if hover:
            rect.inflate_ip(6, 6)

        # shadow
        shadow = rect.move(4,4)
        pg.draw.rect(screen, (180,180,180), shadow, border_radius=15)

        # warna tiap card
        if card == "reveal":
            color = (255,230,120)
            icon = "?"

        elif card == "heal":
            color = (140,255,160)
            icon = "+"

        elif card == "double":
            color = (140,200,255)
            icon = "x2"

        # background card
        pg.draw.rect(screen, color, rect, border_radius=15)
        pg.draw.rect(screen, BLACK, rect, 2, border_radius=15)

        # ICON BESAR
        icon_font = pg.font.SysFont("sans-serif", 40, bold=True)
        icon_text = icon_font.render(icon, True, BLACK)
        icon_rect = icon_text.get_rect(center=(rect.centerx, rect.y + 35))

        screen.blit(icon_text, icon_rect)

        # NAMA CARD
        name_font = pg.font.SysFont("sans-serif", 22, bold=True)
        name = name_font.render(card.upper(), True, BLACK)
        name_rect = name.get_rect(center=(rect.centerx, rect.y + 70))

        screen.blit(name, name_rect)

        # DESKRIPSI
        desc_font = pg.font.SysFont("sans-serif", 16)

        if card == "reveal":
            desc = "Reveal cell"
        elif card == "heal":
            desc = "Remove kesalahan"
        else:
            desc = "Bonus score"

        desc_text = desc_font.render(desc, True, (60,60,60))
        desc_rect = desc_text.get_rect(center=(rect.centerx, rect.y + 95))

        screen.blit(desc_text, desc_rect)

running = True
clock = pg.time.Clock()
font_tombol = pg.font.SysFont("sans-serif", 70, bold = False)
kotak_aktif = None
board = [[0 for _ in range(9)] for _ in range(9)]
font_grid = pg.font.SysFont("sans-serif", 40, bold = False)
solusi = None
original_board = copy.deepcopy(board)
newgame_rect = pg.Rect(720, 580, 300, 70)
gameover_rect = pg.Rect(WIDTH//2 - 200, HEIGHT//2 - 120, 400, 240)
gameover_button = pg.Rect(WIDTH//2 - 120, HEIGHT//2 + 20, 240, 60)
jumlah_salah = 0
game_over = False
error_cell = None
error_time = 0
error_reason = []
gameover_time = 0
newgame_cooldown = 1500
last_newgame_click = -newgame_cooldown
dev_mode = True
wave_clear = False
wave_clear_time = 0
show_cards = False
card_effect = None
card_effect_time = 0
effect_cell = None
cards = []
hovered_cards = [False, False]
selected_card = None
inventory_cards = []
shake_time = 0
shake_power = 0


# buat soal dulu
generate_soal()

# loop kita
while running:
    clock.tick(60)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if show_cards and not game_over :

                    card_clicked = False 

                    for i in range(len(cards)):
                        x = WIDTH//2 - 180 + i * 220
                        rect = pg.Rect(x, HEIGHT//2 - 120, 200, 240)

                        if rect.collidepoint(event.pos):
                            kartuterklik.play()
                            inventory_cards.append(cards[i])
                            show_cards = False
                            wave_clear = False
                            next_wave()
                            card_clicked = True
                            break
                    if not card_clicked :
                        continue

                for i, card in enumerate(inventory_cards):
                        x = 900 + i * 120
                        y = 40
                        rect = pg.Rect(x, y, 110, 120)

                        if rect.collidepoint(event.pos):
                            kartuterklik.play()
                            apply_card(card)
                            if card == "heal" :
                                healsfx.play()
                            elif card == "reveal" :
                                revealsfx.play()
                            else :
                                scsfx.play()
                            inventory_cards.pop(i)
                            break

                if game_over:
                    if pg.time.get_ticks() - gameover_time > 1500:
                        if gameover_button.collidepoint(event.pos):
                            wave = 1
                            score = 0
                            kotak_aktif = None
                            generate_soal()
                            game_over = False
                        continue
                if newgame_rect.collidepoint(event.pos):
                    if pg.time.get_ticks() - last_newgame_click >= newgame_cooldown:
                        generate_soal()
                        last_newgame_click = pg.time.get_ticks()

                else:
                    angka = deteksi_posisi_tombol(event.pos)

                    if angka and kotak_aktif and not game_over:
                        r, c = kotak_aktif

                        if original_board[r][c] == 0 and board[r][c] == 0:

                            if angka == solusi[r][c]:
                                angkabenar.play()
                                board[r][c] = angka
                            else:
                                angkasalah.play()
                                shake_time = pg.time.get_ticks()
                                shake_power = 10
                                error_cell = (r, c)
                                error_time = pg.time.get_ticks()
                                error_reason = cek_konflik(r, c, angka)

                                jumlah_salah += 1

                                if jumlah_salah >= 3:
                                    soundKalah.play()
                                    game_over = True
                                    gameover_time = pg.time.get_ticks()

                    else:
                        pos = cek_grid_sudoku(event.pos)
                        if pos:
                            kotak_aktif = pos


        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE and kotak_aktif and not game_over:
                r, c = kotak_aktif
                if original_board[r][c] == 0 and board[r][c] != solusi[r][c]:
                    board[r][c] = 0
        
        if event.type == pg.KEYDOWN:
            if dev_mode and event.key == pg.K_F1 and not show_cards:
                for r in range(9):
                    for c in range(9):
                        if board[r][c] == 0:
                            board[r][c] = solusi[r][c]


    if not game_over and not wave_clear and not show_cards and cek_menang():
        soundmenang.play()
        wave_clear = True
        wave_clear_time = pg.time.get_ticks()
        score += 100 * wave

    if wave_clear:
        if pg.time.get_ticks() - wave_clear_time > 1500:
            wave += 1
            if (wave - 1) % 2 == 0:
                show_cards = True
                generate_cards()
            else :
                generate_soal()

            wave_clear = False


    screen.fill(WHITE)

    draw_x = grid_x
    draw_y = grid_y

    if pg.time.get_ticks() - shake_time < 200:
        offset_x = random.randint(-shake_power, shake_power)
        offset_y = random.randint(-shake_power, shake_power)

    old_x = grid_x
    old_y = grid_y

    grid_x = draw_x
    grid_y = draw_y

    highlight_kotak()
    highlight_error()
    membuat_grid()
    gambar_angka()

    grid_x = old_x
    grid_y = old_y

    grid_tombol()
    gambar_tombol_newgame()
    gambar_kesalahan()
    gambar_gameover()
    gambar_info()
    gambar_cards()
    gambar_card_effect()
    gambar_inventory()
    gambar_wave_clear()

    pg.display.update()

pg.quit() 