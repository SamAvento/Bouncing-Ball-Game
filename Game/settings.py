"""
Mô-đun này chứa các cài đặt chung cho trò chơi Bóng nảy.

Nó khởi tạo pygame và đặt kích thước màn hình và phông chữ tiêu đề mặc định. Nó cũng xác định kích thước của các nút được sử dụng trong trò chơi.

Mô-đun xác định một số màu được sử dụng trong suốt trò chơi.

Nó khởi tạo pygame.mixer và tải các hiệu ứng âm thanh được sử dụng trong trò chơi. Nó cũng đặt âm lượng mặc định cho hiệu ứng âm thanh và âm nhạc.

Mô-đun xác định phông chữ được sử dụng cho các nút trong trò chơi và đặt chú thích cho cửa sổ trò chơi. Nó cũng tạo ra một đối tượng đồng hồ được sử dụng để kiểm soát tốc độ khung hình của trò chơi.
"""
import pygame
pygame.init()

# Cài đặt kích thước cửa sổ game mặc định
screen_size = (600, 700)
screen_width, screen_height = screen_size
screen = pygame.display.set_mode(screen_size)

# Cài đặt kích thước tiêu đề game
title_font = pygame.font.Font(None, 72)

# Cài đặt kích thước các nút bấm
button_width = 200
button_height = 50

# Tạo các màu sắc
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
purple = (127, 0, 255)
magenta = (255, 0, 255)
pink = (255, 0, 127)

# Cài đặt âm thanh
pygame.mixer.init()
bounce_sound = pygame.mixer.Sound('SFX/ball-bouncing.wav')
laser_blast_sound = pygame.mixer.Sound('SFX/laser-blast.wav')
coin_collect_sound = pygame.mixer.Sound('SFX/coin-collect.wav')
obstacle_break_sound = pygame.mixer.Sound('SFX/obstacle-break.wav')
game_over_sound = pygame.mixer.Sound('SFX/game-over.wav')
voice_game_over_sound = pygame.mixer.Sound('SFX/voice-game-over.ogg')
voice_go = pygame.mixer.Sound('SFX/voice-go.ogg')

# Cài đặt âm lượng mặc định cho âm thanh và nhạc
sfx_volume = 100
music_volume = 100

# Cài đặt font chữ cho các nút
font = pygame.font.Font(None, 36)

# Tiêu đề của game
pygame.display.set_caption("Bouncing Ball")

clock = pygame.time.Clock()
