"""
Mô-đun này chứa các lớp xác định các đối tượng trò chơi khác nhau được sử dụng trong trò chơi "Bóng nảy".

Lớp `Ball` định nghĩa đối tượng quả bóng được sử dụng trong trò chơi. Nó có các phương pháp để vẽ và cập nhật quả bóng trên màn hình.

Lớp `Platform` xác định đối tượng đệm nảy được sử dụng trong trò chơi. Nó có các phương thức để vẽ và cập nhật đệm nảy trên màn hình.

Lớp `Coin` xác định đối tượng xu được sử dụng trong trò chơi. Nó có một phương pháp để vẽ đồng xu trên màn hình.

Lớp `Obstacle` xác định đối tượng vật cản được sử dụng trong trò chơi. Nó có một phương pháp để vẽ vật cản trên màn hình.

Lớp `Laser` xác định đối tượng tia laser được sử dụng trong trò chơi. Nó có các phương pháp để vẽ và cập nhật tia laser trên màn hình.

Lớp `Buff` xác định đối tượng vật phẩm hỗ trợ được sử dụng trong trò chơi. Nó có các phương pháp để vẽ và áp dụng các hiệu ứng hỗ trợ cho các đối tượng quả bóng và đệm nảy.

Lớp `Effect` kế thừa từ lớp `Buff` và định nghĩa các hiệu ứng bổ sung có thể áp dụng cho các đối tượng bóng và đệm nảy. Nó có các phương pháp để áp dụng hiệu ứng và loại bỏ hiệu ứng.
"""
import pygame
import random
import math
from .settings import *


# Tạo class quả bóng
class Ball:
    """
    Lớp Ball đại diện cho đối tượng quả bóng trong trò chơi bóng nảy.
    
    Thuộc tính:
    -----------
    x: int
        Tọa độ x của tâm quả bóng.
    y: int
        Tọa độ y của tâm quả bóng.
    radius: int
        Bán kính của quả bóng
    color: tuple
        Màu sắc của quả bóng
    speed_x: float
        Tốc độ theo phương ngang của quả bóng
    speed_y: float
        Tốc độ theo phương dọc của quả bóng
    rect: pygame.Rect
        Vùng hình chữ nhật đại diện cho vị trí và kích thước của quả bóng.
    last_touch: int
        Thời gian (tính bằng mili giây) lần cuối cùng quả bóng chạm vào đệm nảy.
    break_buff: bool
        Một flag cho biết quả bóng cần phải chuyển hướng di chuyển hay không.

    Methods:
    -----------
    draw(): Vẽ quả bóng lên màn hình
    update(): Cập nhật vị trí và trạng thái của quả bóng dựa trên tốc độ và va chạm của nó với cạnh màn hình game hoặc đệm nảy.
    """
    def __init__(self):
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.radius = 15
        self.color = white
        speed = 5
        angle = random.uniform(math.pi/4, 7*math.pi/4)
        self.speed_x = speed * math.cos(angle)
        self.speed_y = speed * math.sin(angle)
        self.rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.last_touch = pygame.time.get_ticks()
        self.break_buff = False

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.radius)

    def update(self):
        # Kiểm tra nếu bóng đã không chạm vào đệm nảy trong 30s (tránh các chuyển động của bóng mà không thể rơi khỏi màn hình được)
        if not self.break_buff and pygame.time.get_ticks() - self.last_touch > 30000:
            # Kích hoạt chuyển hướng bóng
            self.break_buff = True
            angle = random.uniform(math.pi/4, 3*math.pi/4)
            speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
            self.speed_x = speed * math.cos(angle)
            self.speed_y = speed * math.sin(angle)

        self.x += self.speed_x
        self.y += self.speed_y

        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

        # Kiểm tra va chạm với các cạnh của cửa sổ game
        if self.x - self.radius < 0 or self.x + self.radius > screen_width:
            self.speed_x *= -1
            bounce_sound.play()

        if self.y - self.radius < 0:
            self.speed_y *= -1
            bounce_sound.play()


# Tạo class đệm nảy
class Platform:
    """
    Lớp Platform đại diện cho một đối tượng đệm nảy trong trò chơi bóng nảy.
    
    Attributes:
    -----------
    width: int
        Chiều rộng của đệm nảy
    height: int
        Chiều cao của đệm nảy.
    x: int
        Tọa độ x của góc trên cùng bên trái của đệm nảy.
    y: int
        Tọa độ y của góc trên cùng bên trái của đệm nảy.
    color: tuple
        Màu sắc của đệm nảy
    speed_x: int
        Tốc độ theo phương ngang của đệm nảy

    Methods:
    -----------
    draw(): Vẽ đệm nảy lên màn hình
    update(platform): Cập nhật vị trí và trạng thái của đệm nảy dựa trên input đầu vào từ bàn phím của người dùng và ngăn đệm nảy di chuyển ra khỏi màn hình.
    """
    def __init__(self):
        self.width = 150
        self.height = 30
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height - 50
        self.color = white
        self.speed_x = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, (int(self.x), int(
            self.y), int(self.width), int(self.height)))

    def update(self, platform):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            platform.speed_x = -5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            platform.speed_x = 5
        else:
            platform.speed_x = 0

        platform.x += platform.speed_x

        # Chặn không cho đệm nảy di chuyển xa khỏi màn hình game
        if platform.x < 0:
            platform.x = 0
        elif platform.x + platform.width > screen_width:
            platform.x = screen_width - platform.width


# Tạo class đồng xu
class Coin:
    """
    Lớp Coin đại diện cho một đối tượng đồng xu trong trò chơi bóng nảy.
    
    Attributes:
    -----------
    radius: int
        Bán kính của đồng xu
    x: int
        Tọa độ x của tâm đồng xu.
    y: int
        Tọa độ y của tâm đồng xu.
    color: tuple
        Màu sắc của đồng xu
    rect: pygame.Rect
        Vùng hình chữ nhật đại diện cho vị trí và kích thước của đồng xu.

    Methods:
    -----------
    draw(): Vẽ đồng xu trên màn hình và cập nhật diện tích vùng hình chữ nhật của nó.
    """
    def __init__(self, platform, ball):
        self.radius = 10
        self.x = random.randint(0 + self.radius, screen_width - self.radius)
        self.y = random.randint(
            50 + self.radius, screen_height - platform.height - ball.radius * 2 - self.radius)
        self.color = yellow
        self.rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(
            screen, yellow, (int(self.x), int(self.y)), int(self.radius))
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius


# Tạo class vật cản
class Obstacle:
    """
    Lớp Obstacle đại diện cho một đối tượng vật cản trong trò chơi Bóng nảy.
    
    Attributes:
    -----------
    width: int
        Chiều rộng của vật cản.
    height: int
        Chiều cao của vật cản.
    color: tuple
        Màu sắc của vật cản
    x: int
        Tọa độ x của góc trên cùng bên trái của vật cản.
    y: int
        Tọa độ y của góc trên cùng bên trái của vật cản.

    Methods:
    -----------
    draw(): Vẽ vật cản trên màn hình.
    """
    def __init__(self, grid_size, occupied_grids, coins, platform):
        self.width = grid_size
        self.height = grid_size
        self.color = red

        # Chọn ngẫu nhiên một vị trí lưới (grid) chưa được sử dụng
        max_x = screen_width // grid_size
        max_y = screen_height // grid_size
        while True:
            grid_x = random.randint(0, max_x - 1)
            grid_y = random.randint(0, max_y - 1)
            if (grid_x, grid_y) not in occupied_grids:
                # Chuyển đổi vị trí lưới (grid) thành vị trí pixel
                x = grid_x * grid_size
                y = grid_y * grid_size
                # Kiểm tra vị trí tạo vật cản có trùng với bất kỳ vị trí của đồng xu nào không, hoặc có quá gần cạnh trên đầu màn hình hoặc trong khu vực di chuyển của đệm nảy không
                overlaps_with_coin = any(
                    abs(coin.x - x) < coin.radius + self.width / 2 and abs(coin.y - y) < coin.radius + self.height / 2 for coin in coins)
                too_close_to_top = y < 100
                in_platform_area = y > platform.y - platform.height - self.height
                if not overlaps_with_coin and not too_close_to_top and not in_platform_area:
                    break

        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (int(self.x), int(self.y), int(self.width), int(self.height)))


# Tạo class Laser (chỉ kích hoạt khi bóng đã thu thập được mỗi 5 xu)
class Laser:
    """
    Lớp Laser đại diện cho một đối tượng laser trong trò chơi Bóng nảy.
    
    Attributes:
    -----------
    x: int
        Tọa độ x của góc trên bên trái của tia laser.
    y: int
        Tọa độ y của góc trên bên trái của tia laser.
    width: int
        Chiều rộng của tia laser.
    height: int
        Chiều cao của tia laser.
    color: tuple th
        Màu sắc của tia laser
    speed_y: int
        Tốc độ theo phương thẳng đứng của tia laser.

    Methods:
    -----------
    draw(): Vẽ tia laser trên màn hình.
    update(): Cập nhật vị trí của tia laser dựa trên tốc độ của nó.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 20
        self.color = cyan
        self.speed_y = -10

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (int(self.x), int(self.y), int(self.width), int(self.height)))

    def update(self):
        self.y += self.speed_y


# Tạo class Buff
class Buff:
    """
    Lớp Buff đại diện cho một đối tượng vật phẩm hỗ trợ trong trò chơi bóng nảy.
    
    Attributes:
    -----------
    radius: int
        Bán kính của vật phẩm hỗ trợ.
    x: int
        Tọa độ x của tâm vật phẩm hỗ trợ.
    y: int
        Tọa độ y của tâm vật phẩm hỗ trợ.
    color: tuple
        Màu của vật phẩm hỗ trợ.
    rect: pygame.Rect
        Vùng hình chữ nhật biểu thị vị trí và kích thước của vật phẩm hỗ trợ.

    Methods:
    -----------
    draw(): Vẽ vật phẩm hỗ trợ trên màn hình và cập nhật khu vực hình chữ nhật của nó.
    """
    def __init__(self, platform, ball):
        self.radius = 10
        self.x = random.randint(0 + self.radius, screen_width - self.radius)
        self.y = random.randint(
            50 + self.radius, screen_height - platform.height - ball.radius * 2 - self.radius)
        self.color = green
        self.rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(screen, green, (int(self.x),
                           int(self.y)), int(self.radius), 2)
        pygame.draw.line(screen, green, (int(self.x), int(
            self.y-self.radius/2)), (int(self.x), int(self.y+self.radius/2)), 2)
        pygame.draw.line(screen, green, (int(self.x-self.radius/2),
                         int(self.y)), (int(self.x+self.radius/2), int(self.y)), 2)
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius


# Tạo class Effect (hiệu ứng cho vật phẩm hỗ trợ) kế thừa lớp Buff
class Effect(Buff):
    """
    Lớp Effect đại diện cho một đối tượng hiệu ứng (status effect) trong trò chơi bóng bảy. Nó kế thừa từ lớp Buff.
    
    Attributes:
    -----------
    type: str
        Loại hiệu ứng (ví dụ: "Breaking ball" hoặc "Wide platform").
    start_time: int
        Thời gian (tính bằng mili giây) khi hiệu ứng được áp dụng.
    duration: int
        Khoảng thời gian hiệu lực (tính bằng mili giây) của hiệu ứng sau khi được áp dụng.

    Methods:
    -----------
    apply(ball, platform): Áp dụng hiệu ứng cho quả bóng hoặc đệm nảy dựa trên loại hiệu ứng của nó.
    remove(ball, platform): Xoá hiệu ứng cho quả bóng hoặc đệm nảy dựa trên loại hiệu ứng của nó.
    """
    def __init__(self, platform, ball):
        super().__init__(platform, ball)
        self.type = random.choice(["Breaking ball", "Wide platform"])
        self.start_time = pygame.time.get_ticks()
        self.duration = 5000  # effect lasts for 5 seconds

    def apply(self, ball, platform):
        if self.type == "Breaking ball":
            ball.radius *= 2
            ball.speed_x /= 2
            ball.speed_y /= 2
        elif self.type == "Wide platform":
            platform.width *= 2

    def remove(self, ball, platform):
        if self.type == "Breaking ball":
            ball.radius /= 2
            ball.speed_x *= 2
            ball.speed_y *= 2
        elif self.type == "Wide platform":
            platform.width /= 2
