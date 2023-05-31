"""
Mô-đun này chứa các Hàm xác định các màn hình khác nhau của trò chơi Bóng nảy.

Hàm `main_menu` hiển thị màn hình menu chính của trò chơi. Nó cho phép người dùng bắt đầu một trò chơi mới, truy cập màn hình cài đặt hoặc thoát khỏi trò chơi.

Hàm `settings_screen` hiển thị màn hình cài đặt của trò chơi. Nó cho phép người dùng điều chỉnh âm lượng của hiệu ứng âm thanh và âm nhạc.

Hàm `game_loop` chạy vòng lặp trò chơi chính. Nó khởi tạo các đối tượng trò chơi, xử lý các sự kiện, cập nhật trạng thái trò chơi và vẽ các đối tượng trò chơi trên màn hình.

Hàm `pause_screen` hiển thị màn hình tạm dừng của trò chơi. Nó cho phép người dùng tiếp tục trò chơi, bắt đầu lại trò chơi mới hoặc quay lại màn hình menu chính.

Hàm `game_over` hiển thị màn hình trò chơi kết thúc của trò chơi. Nó cho phép người dùng bắt đầu lại trò chơi mới hoặc quay lại màn hình menu chính.
"""
import pygame
import math
from .objects import *
from .settings import *


# Màn hình Main Menu
def main_menu():
    """
    Hàm này hiển thị màn hình Main Menu của trò chơi. Nó chứa một vòng lặp while liên tục kiểm tra các sự kiện và cập nhật màn hình.
    
    Hàm kiểm tra ba loại sự kiện: QUIT, MOUSEBUTTONDOWN trên nút "Play", nút "Settings" hoặc nút "Quit".
    
    Nếu sự kiện QUIT được kích hoạt, trò chơi sẽ thoát.
    
    Nếu sự kiện MOUSEBUTTONDOWN được kích hoạt trên các nút:
    - "Play": hàm game_loop sẽ được gọi.
    - "Settings": hàm settings_screen sẽ được gọi. 
    - "Quit": trò chơi sẽ thoát.
    
    Hàm này cũng cập nhật màn hình bằng cách tô màu nền đen và vẽ tiêu đề trò chơi và ba nút: "Play", "Settings" và "Quit".
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if play_button.collidepoint(mouse_pos):
                    game_loop()

                if settings_button.collidepoint(mouse_pos):
                    settings_screen()

                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

        # Vẽ màn hình chính
        screen.fill(black)

        # Vẽ tiêu đề game
        title_text = title_font.render("Bouncing Ball", True, white)
        title_text_rect = title_text.get_rect(
            center=(screen_width/2, screen_height/4))
        screen.blit(title_text, title_text_rect)

        # Vẽ nút "Play"
        play_button_text = font.render("Play", True, black)
        play_button_text_rect = play_button_text.get_rect(
            center=(screen_width/2, screen_height/2))
        play_button = pygame.draw.rect(screen, white, (play_button_text_rect.centerx - button_width/2,
                                       play_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(play_button_text, play_button_text_rect)

        # Vẽ nút "Settings"
        settings_button_text = font.render("Settings", True, black)
        settings_button_text_rect = settings_button_text.get_rect(
            center=(screen_width/2, screen_height/2 + 100))
        settings_button = pygame.draw.rect(screen, white, (settings_button_text_rect.centerx - button_width/2,
                                                           settings_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(settings_button_text, settings_button_text_rect)

        # Vẽ nút "Quit"
        quit_button_text = font.render("Quit", True, black)
        quit_button_text_rect = quit_button_text.get_rect(
            center=(screen_width/2, screen_height/2 + 200))
        quit_button = pygame.draw.rect(screen, white, (quit_button_text_rect.centerx - button_width/2,
                                       quit_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(quit_button_text, quit_button_text_rect)

        pygame.display.update()
        clock.tick(60)


# Màn hình cài đặt trò chơi
def settings_screen():
    """
    Hàm này hiển thị màn hình cài đặt của trò chơi. Nó chứa một vòng lặp while liên tục kiểm tra các sự kiện và cập nhật màn hình.
    
    Hàm kiểm tra ba loại sự kiện: QUIT, MOUSEBUTTONDOWN trên nút "Back", thanh trượt điều chỉnh âm lượng cho hiệu ứng âm thanh hoặc nhạc.
    
    Nếu sự kiện QUIT được kích hoạt, trò chơi sẽ thoát. 
    
    Nếu sự kiện MOUSEBUTTONDOWN được kích hoạt trên nút "Back", hàm sẽ quay trở lại màn hình Main Menu.
    
    Nếu sự kiện MOUSEBUTTONDOWN được kích hoạt trên các thanh trượt:
    - sfx: biến toàn cầu sfx_volume sẽ được cập nhật và tất cả các hiệu ứng âm thanh sẽ có âm lượng được đặt thành giá trị mới.
    - music, biến toàn cục music_volume sẽ được cập nhật và âm lượng nhạc sẽ được đặt thành giá trị mới.
    
    Hàm này cũng cập nhật màn hình bằng cách tô màu nền đen và vẽ tiêu đề của màn hình, nút "Back" và hai thanh trượt: "SFX" và "Music". Nó cũng hiển thị giá trị phần trăm cho cả hai thanh trượt.
    """
    global sfx_volume
    global music_volume

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_button.collidepoint(mouse_pos):
                    return

                if sfx_slider.collidepoint(mouse_pos):
                    sfx_volume = int(
                        (mouse_pos[0] - sfx_slider.x) / sfx_slider.width * 100)
                    bounce_sound.set_volume(sfx_volume / 100)
                    laser_blast_sound.set_volume(sfx_volume / 100)
                    coin_collect_sound.set_volume(sfx_volume / 100)
                    obstacle_break_sound.set_volume(sfx_volume / 100)
                    game_over_sound.set_volume(sfx_volume / 100)
                    voice_game_over_sound.set_volume(sfx_volume / 100)
                    voice_go.set_volume(sfx_volume / 100)

                if music_slider.collidepoint(mouse_pos):
                    music_volume = int(
                        (mouse_pos[0] - music_slider.x) / music_slider.width * 100)
                    pygame.mixer.music.set_volume(music_volume / 100)

        screen.fill(black)

        # Vẽ tiêu đề màn hình
        title_text = title_font.render("Settings", True, white)
        title_text_rect = title_text.get_rect(
            center=(screen_width/2, screen_height/4))
        screen.blit(title_text, title_text_rect)

        # Vẽ nút "Back"
        back_button_text = font.render("Back", True, black)
        back_button_text_rect = back_button_text.get_rect(
            center=(screen_width/2, screen_height/2 + 300))
        back_button = pygame.draw.rect(screen, white, (back_button_text_rect.centerx - button_width/2,
                                       back_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(back_button_text, back_button_text_rect)

        # Vẽ thanh trượt âm lượng SFX
        sfx_label = font.render("SFX", True, white)
        sfx_label_rect = sfx_label.get_rect(
            center=(screen_width/4, screen_height/2))
        screen.blit(sfx_label, sfx_label_rect)

        sfx_slider = pygame.draw.rect(screen, white,
                                      (screen_width/4 + 50,
                                       screen_height/2 - 10,
                                       screen_width/2 - 100,
                                       20))

        sfx_handle = pygame.draw.circle(screen,
                                        black,
                                        (int(screen_width/4 + 50 + (sfx_volume / 100) * (screen_width/2 - 100)),
                                         int(screen_height/2)),
                                        15)

        # Vẽ thanh trượt âm lượng nhạc
        music_label = font.render("Music", True, white)
        music_label_rect = music_label.get_rect(
            center=(screen_width/4, screen_height/2 + 100))
        screen.blit(music_label, music_label_rect)

        music_slider = pygame.draw.rect(screen,
                                        white,
                                        (screen_width/4 + 50,
                                         screen_height/2 + 90,
                                         screen_width/2 - 100,
                                         20))

        music_handle = pygame.draw.circle(screen,
                                          black,
                                          (int(screen_width/4 + 50 + (music_volume / 100) * (screen_width/2 - 100)),
                                           int(screen_height/2 + 100)),
                                          15)

        # Hiển thị giá trị phần trăm của thanh trượt âm lượng SFX và nhạc
        sfx_value_label = font.render(str(sfx_volume) + "%", True, white)
        sfx_value_label_rect = sfx_value_label.get_rect(
            center=(screen_width/4 + 50 + (screen_width/2 - 100) + 50, screen_height/2))
        screen.blit(sfx_value_label, sfx_value_label_rect)

        music_value_label = font.render(str(music_volume) + "%", True, white)
        music_value_label_rect = music_value_label.get_rect(
            center=(screen_width/4 + 50 + (screen_width/2 - 100) + 50, screen_height/2 + 100))
        screen.blit(music_value_label, music_value_label_rect)

        pygame.display.update()
        clock.tick(60)


collision_cooldown = 0


# Vòng lặp trò chơi khi bấm "Play"
def game_loop():
    """
    Hàm này chạy vòng lặp trò chơi chính. Nó khởi tạo các biến toàn cục như ball, platform, coins, score và collision_cooldown. Nó cũng phát hiệu ứng âm thanh và phát nhạc nền.

    Hàm chứa một vòng lặp while liên tục kiểm tra các sự kiện và cập nhật trạng thái trò chơi. Vòng lặp kiểm tra ba loại sự kiện: QUIT, MOUSEBUTTONDOWN trên nút "Pause" và va chạm giữa quả bóng và các đối tượng trò chơi khác nhau.

    Nếu sự kiện QUIT được kích hoạt, trò chơi sẽ thoát. 
    
    Nếu sự kiện MOUSEBUTTONDOWN được kích hoạt trên nút "Pause", trò chơi sẽ vào màn hình "Pause".

    Vòng lặp cũng cập nhật và vẽ tất cả các đối tượng trò chơi trên màn hình, bao gồm quả bóng (ball), đệm nảy (platform), đồng xu (coin), chướng ngại vật (obstacle), tia laze (laser), vật phẩm hỗ trợ (buff) và hiệu ứng (effect). Nó kiểm tra các xung đột giữa các đối tượng này và cập nhật trạng thái của chúng cho phù hợp.

    Vòng lặp cũng cập nhật điểm số và hiển thị nó trên màn hình. Trạng thái trò chơi được cập nhật với tốc độ 60 khung hình mỗi giây (60FPS).
    """
    global ball
    global platform
    global coins
    global score
    global collision_cooldown

    voice_go.play()
    pygame.time.delay(1000)
    pygame.mixer.music.load('Music/(AB) Bejeweled 3 Remix Medley.mp3')
    pygame.mixer.music.play(-1)

    ball = Ball()
    platform = Platform()
    coins = [Coin(platform, ball) for _ in range(10)]
    score = 0
    hit_count = 0

    obstacles = []
    grid_size = 50
    occupied_grids = set()

    coins_collected = 0
    lasers = []
    last_laser_time = 0

    buffs = []
    last_buff_time = 0

    effects = []

    # Tạo số lượng vật cản
    for _ in range(10):
        obstacle = Obstacle(grid_size, occupied_grids, coins, platform)
        obstacles.append(obstacle)

        grid_x = int(obstacle.x / grid_size)
        grid_y = int(obstacle.y / grid_size)
        occupied_grids.add((grid_x, grid_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if pause_button.collidepoint(mouse_pos):
                    pause_screen()

        screen.fill(black)

        if collision_cooldown > 0:
            collision_cooldown -= 1

        # Vẽ nút "Pause"
        pause_button_text = font.render("Pause", True, black)
        pause_button_text_rect = pause_button_text.get_rect(
            topright=(screen_width - 10, 10))
        pause_button = pygame.draw.rect(
            screen, white, pause_button_text_rect.inflate(20, 10))
        screen.blit(pause_button_text, pause_button_text_rect)

        # Vẽ quả bóng và cập nhật chuyển động
        ball.draw()
        ball.update()

        # Kiểm tra quả bóng va chạm với đệm nảy
        if ball.y + ball.radius > platform.y and ball.y + ball.radius < platform.y + platform.height and platform.x < ball.x < platform.x + platform.width:
            if collision_cooldown == 0:
                bounce_sound.play()
                ball.y = platform.y - ball.radius
                ball.speed_y *= -1
                hit_count += 1
                collision_cooldown = 10

            # Thay đổi góc độ quả bóng tuỳ vào va chạm với đệm nảy đang di chuyển
            angle = math.atan2(ball.speed_y, ball.speed_x)
            angle += platform.speed_x * 0.1
            speed = math.sqrt(ball.speed_x ** 2 + ball.speed_y ** 2)
            ball.speed_x = speed * math.cos(angle)
            ball.speed_y = speed * math.sin(angle)

            # Với mỗi 5 lần bóng chạm đệm nảy:
            if hit_count % 5 == 0:
                # Giảm diện tích và tăng tốc độ đệm nảy
                platform.width -= 5
                platform.speed_x += 1.2
                # Tăng tốc độ quả bóng
                ball.speed_x *= 1.1
                ball.speed_y *= 1.1

            # Đặt lại flag chuyển hướng quả bóng thành False
            ball.last_touch = pygame.time.get_ticks()
            ball.break_buff = False

        # Kiểm tra trò chơi kết thúc (khi bóng rơi khỏi màn hình)
        if ball.y - ball.radius > screen_height:
            game_over()

        # Vẽ đệm nảy
        platform.draw()
        platform.update(platform)

        # Vẽ đồng xu
        for coin in coins:
            coin.draw()

            # Kiểm tra quả bóng va chạm với đồng xu
            if ball.rect.colliderect(coin.rect):
                coins.remove(coin)
                coin_collect_sound.play()
                coins.append(Coin(platform, ball))
                score += 1
                coins_collected += 1

                # Kiểm tra xem bóng đã thu hoạch đủ 5 đồng xu chưa (để kích hoạt tia laser từ đệm nảy)
                if coins_collected == 5:
                    coins_collected = 0
                    last_laser_time = pygame.time.get_ticks()

        # Tia laser bắn ra theo từng lượt, mỗi tia cách nhau một khoảng thời gian nhất định
        current_time = pygame.time.get_ticks()
        if current_time - last_laser_time < 2500 and (current_time - last_laser_time) // 500 > len(lasers):
            lasers.append(Laser(platform.x + platform.width / 2,
                                platform.y - platform.height))
            laser_blast_sound.play()

        # Vẽ laser
        for laser in lasers[:]:
            laser.update()
            laser.draw()

            # Kiểm tra va tia laser chạm với cạnh trên màn hình
            if laser.y + laser.height < 0:
                lasers.remove(laser)

            # Kiểm tra tia laser va chạm với vật cản
            else:
                for obstacle in obstacles[:]:
                    if laser.x > obstacle.x and laser.x < obstacle.x + obstacle.width and laser.y < obstacle.y + obstacle.height:
                        obstacle_break_sound.play()
                        obstacles.remove(obstacle)
                        score += 1

                        grid_x = int(obstacle.x / grid_size)
                        grid_y = int(obstacle.y / grid_size)
                        occupied_grids.remove((grid_x, grid_y))

                        # Tạo vật cản mới
                        new_obstacle = Obstacle(
                            grid_size, occupied_grids, coins, platform)
                        obstacles.append(new_obstacle)

                        grid_x = int(new_obstacle.x / grid_size)
                        grid_y = int(new_obstacle.y / grid_size)
                        occupied_grids.add((grid_x, grid_y))

                        # Xoá tia laser
                        lasers.remove(laser)
                        break

        # Kiểm tra số buff tồn tại trên màn hình
        current_time = pygame.time.get_ticks()
        if len(buffs) == 0 and current_time - last_buff_time > 15000:
            buffs.append(Buff(platform, ball))

        # Vẽ buff
        for buff in buffs:
            buff.draw()
            
            # Kiểm tra quả bóng va chạm buff
            if ball.rect.colliderect(buff.rect):
                buffs.remove(buff)
                last_buff_time = current_time

                # Áp dụng hiệu ứng
                effect = Effect(platform, ball)
                effect.apply(ball, platform)
                effects.append(effect)

        # Kiểm tra nếu hiệu ứng là "Breaking ball"
        if any(effect.type == "Breaking ball" for effect in effects):
            for obstacle in obstacles[:]:
                if ball.rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)):
                    # Phá vật cản khi tiếp xúc với quả bóng trong hiệu ứng "Breaking ball", đồng thời tăng 2 điểm
                    obstacle_break_sound.play()
                    obstacles.remove(obstacle)
                    score += 2

                    # Tạo vật cản mới
                    new_obstacle = Obstacle(
                        grid_size, occupied_grids, coins, platform)
                    obstacles.append(new_obstacle)

                    grid_x = int(new_obstacle.x / grid_size)
                    grid_y = int(new_obstacle.y / grid_size)
                    occupied_grids.add((grid_x, grid_y))

        # Kiểm tra xem các hiệu ứng đã hết hạn thời gian hiệu lực chưa
        for effect in effects[:]:
            if pygame.time.get_ticks() - effect.start_time > effect.duration:
                effect.remove(ball, platform)
                effects.remove(effect)

        # Vẽ vật cản
        for obstacle in obstacles:
            obstacle.draw()

            # Kiểm tra quả bóng va chạm với vật cản
            if ball.rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)):
                if collision_cooldown == 0:
                    bounce_sound.play()
                    dx = (obstacle.x + obstacle.width / 2) - ball.x
                    dy = (obstacle.y + obstacle.height / 2) - ball.y
                    if abs(dx) > abs(dy):
                        ball.speed_x *= -1
                        if dx > 0:
                            ball.x = obstacle.x - ball.radius
                        else:
                            ball.x = obstacle.x + obstacle.width + ball.radius
                    else:
                        ball.speed_y *= -1
                        if dy > 0:
                            ball.y = obstacle.y - ball.radius
                        else:
                            ball.y = obstacle.y + obstacle.height + ball.radius

                    collision_cooldown = 10

        # Tính điểm
        score_text = font.render("Score: " + str(score), True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)


# Màn hình "Pause" trò chơi
def pause_screen():
    """
    Hàm này hiển thị màn hình tạm dừng của trò chơi. Nó tạm dừng nhạc nền và chứa một vòng lặp while liên tục kiểm tra các sự kiện và cập nhật màn hình.

    Hàm kiểm tra ba loại sự kiện: QUIT, MOUSEBUTTONDOWN trên các nút "Resume", "Retry" hoặc "Main Menu".

    Nếu sự kiện QUIT được kích hoạt, trò chơi sẽ thoát. 
    
    Nếu sự kiện MOUSEBUTTONDOWN được kích hoạt trên các nút:
    - "Resume": Hàm sẽ bỏ tạm dừng nhạc nền và quay lại vòng lặp trò chơi game_loop.
    - "Retry": Hàm sẽ khởi động mới lại vòng lặp trò chơi game_loop.
    - "Main Menu": Hàm sẽ dừng nhạc nền và trở về màn hình Main Menu.

    Hàm này cũng cập nhật màn hình bằng cách tô màu nền đen và vẽ tiêu đề màn hình, các nút "Resume", "Retry" và "Main Menu".
    """
    pygame.mixer.music.pause()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if resume_button.collidepoint(mouse_pos):
                    pygame.mixer.music.unpause()
                    return

                if main_menu_button.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    main_menu()

                if retry_button.collidepoint(mouse_pos):
                    game_loop()

        # Vẽ màn hình
        screen.fill(black)

        # Vẽ tiêu đề màn hình
        title_text = title_font.render("PAUSE", True, white)
        title_text_rect = title_text.get_rect(
            center=(screen_width/2, screen_height/4))
        screen.blit(title_text, title_text_rect)

        # Vẽ nút "Resume"
        resume_button_text = font.render("Resume", True, black)
        resume_button_text_rect = resume_button_text.get_rect(
            center=(screen_width/2, screen_height/2))
        resume_button = pygame.draw.rect(screen, white, (resume_button_text_rect.centerx - button_width/2,
                                         resume_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(resume_button_text, resume_button_text_rect)

        # Vẽ nút "Retry"
        retry_button_text = font.render("Retry", True, black)
        retry_button_text_rect = retry_button_text.get_rect(
            center=(screen_width/2, screen_height/2 + 100))
        retry_button = pygame.draw.rect(screen, white, (retry_button_text_rect.centerx - button_width/2,
                                        retry_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(retry_button_text, retry_button_text_rect)

        # Vẽ nút "Main Menu"
        main_menu_button_text = font.render("Main Menu", True, black)
        main_menu_button_text_rect = main_menu_button_text.get_rect(
            center=(screen_width/2, screen_height/2 + 200))
        main_menu_button = pygame.draw.rect(screen, white, (main_menu_button_text_rect.centerx - button_width/2,
                                            main_menu_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(main_menu_button_text, main_menu_button_text_rect)

        pygame.display.update()
        clock.tick(60)


# Màn hình trò chơi kết thúc
def game_over():
    """
    Hàm này hiển thị màn hình trò chơi kết thúc của trò chơi. Nó dừng nhạc nền từ vòng lặp trò chơi game_loop, chạy các hiệu ứng âm thanh và nhạc nền cho màn hình trò chơi kết thúc game_over.

    Hàm chứa một vòng lặp while liên tục kiểm tra các sự kiện và cập nhật màn hình. Vòng lặp kiểm tra hai loại sự kiện: QUIT và MOUSEBUTTONDOWN trên các nút "Retry" hoặc "Main Menu".

    Nếu sự kiện QUIT được kích hoạt, trò chơi sẽ thoát. 
    
    Nếu sự kiện MOUSEBUTTONDOWN được kích hoạt trên các nút:
    - "Retry": Hàm sẽ khởi động mới lại vòng lặp trò chơi game_loop.
    - "Main Menu": Hàm sẽ dừng nhạc nền và trở về màn hình menu chính.

    Hàm này cũng cập nhật màn hình bằng cách tô màu nền đen và vẽ dòng chữ "GAME OVER", điểm số cuối cùng, các nút "Retry", "Main Menu".
    """
    pygame.mixer.music.stop()
    game_over_sound.play()
    pygame.mixer.music.load('Music/Bejeweled 3 Game Over.mp3')
    pygame.time.delay(3000)
    pygame.mixer.music.play()
    voice_game_over_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if retry_button.collidepoint(mouse_pos):
                    game_loop()

                if main_menu_button.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    main_menu()

        screen.fill(black)

        # Vẽ chữ "GAME OVER"
        game_over_text = title_font.render("GAME OVER", True, white)
        game_over_text_rect = game_over_text.get_rect(
            center=(screen_width/2, screen_height/4))
        screen.blit(game_over_text, game_over_text_rect)

        # Tính điểm cuối cùng
        final_score_text = font.render(
            "Final Score: " + str(score), True, white)
        final_score_text_rect = final_score_text.get_rect(
            center=(screen_width/2, screen_height/4 + 50))
        screen.blit(final_score_text, final_score_text_rect)

        # Vẽ nút "Retry"
        retry_button_text = font.render("Retry", True, black)
        retry_button_text_rect = retry_button_text.get_rect(
            center=(screen_width/2, screen_height/2))
        retry_button = pygame.draw.rect(screen, white, (retry_button_text_rect.centerx - button_width/2,
                                        retry_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(retry_button_text, retry_button_text_rect)

        # Vẽ nút "Main Menu"
        main_menu_button_text = font.render("Main Menu", True, black)
        main_menu_button_text_rect = main_menu_button_text.get_rect(
            center=(screen_width/2, screen_height/2 + 100))
        main_menu_button = pygame.draw.rect(screen, white, (main_menu_button_text_rect.centerx - button_width/2,
                                            main_menu_button_text_rect.centery - button_height/2, button_width, button_height))
        screen.blit(main_menu_button_text, main_menu_button_text_rect)

        pygame.display.update()
        clock.tick(60)


main_menu()
