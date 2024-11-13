import pygame
import sys
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

LINE_WIDTH = 5 
BOARD_SIZE = 300 

board_x = (WINDOW_WIDTH - BOARD_SIZE) // 2
board_y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

BG_COLOR = (33, 33, 33)  # dark gray
LINE_COLOR = (179, 179, 179) # light gray

class Game():
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("Tic Tac Toe")
    self.click_sound = pygame.mixer.Sound("sounds/click.mp3")
    self.win_sound = pygame.mixer.Sound("sounds/win.mp3")
    self.newgame_sound = pygame.mixer.Sound("sounds/newgame.mp3")
    self.draw_sound = pygame.mixer.Sound("sounds/draw.wav")
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.clock = pygame.time.Clock()
    self.font = pygame.font.Font("font.ttf", 100)
    self.font2 = pygame.font.Font("font.ttf", 30)
    self.bord = TicTacToe(self)
    self.icon = pygame.image.load("icon/icon.png")
    pygame.display.set_icon(self.icon)
    self.win_sound.set_volume(0.4)

  def check_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        clicked_square = self.bord.get_clicked_square(event.pos)
        if clicked_square:
          self.bord.change_value(clicked_square[0], clicked_square[1])

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE: 
          self.newgame_sound.play()
          self.bord.set_default()
        if event.key == pygame.K_DELETE:
          self.newgame_sound.play()
          self.bord = TicTacToe(self)

  def run(self):
    while True:
      self.screen.fill(BG_COLOR)
      self.bord.run()
      self.check_events()
      pygame.display.flip()
      self.clock.tick(60)

class TicTacToe():
  def __init__(self, game: Game):
    self.game = game
    self.x_o = [["", "", ""], ["", "", ""], ["", "", ""]]
    self.rects_list = []
    self.player = ("X", "O")
    self.turn = 0
    self.winner = None
    self.x_score = 0
    self.o_score = 0
    self.end_game = False
    self.win_positions = [
    [(0, 0), (0, 1), (0, 2)],  # top row
    [(1, 0), (1, 1), (1, 2)],  # middle row
    [(2, 0), (2, 1), (2, 2)],  # bottom row
    [(0, 0), (1, 0), (2, 0)],  # left column
    [(0, 1), (1, 1), (2, 1)],  # middle column
    [(0, 2), (1, 2), (2, 2)],  # right column
    [(0, 0), (1, 1), (2, 2)],  # diagonal
    [(0, 2), (1, 1), (2, 0)]   # anti-diagonal
    ]

  def click_sound(self):
    self.game.click_sound.play()

  def win_sound(self):
    self.game.win_sound.play()

  def draw_sound(self):
    self.game.draw_sound.play()

  def draw_win_line(self, pos):
    pygame.draw.line(self.game.screen, (46, 150, 64), self.rects_list[pos[0][0]][pos[0][1]].center, self.rects_list[pos[2][0]][pos[2][1]].center, LINE_WIDTH + 5)

  def check_win(self):
    for position in self.win_positions:
      if self.x_o[position[0][0]][position[0][1]] == self.x_o[position[1][0]][position[1][1]] == self.x_o[position[2][0]][position[2][1]] != "":
        return position
    return False

  def check_draw(self):
    if not self.check_win() and all(all(row) for row in self.x_o):
      return True

  def draw_board(self):
    pygame.draw.rect(self.game.screen, LINE_COLOR, (board_x - 10, board_y - 10, BOARD_SIZE + 20, BOARD_SIZE + 20), border_radius=5, width=LINE_WIDTH)
    for row in range(3):
      row_list = []
      for col in range(3):
        width = BOARD_SIZE // 3
        height = BOARD_SIZE // 3
        x = board_x + col * width
        y = board_y + row * height
        row_list.append(pygame.draw.rect(self.game.screen, BG_COLOR, (x, y, width, height), width=0))
      
      self.rects_list.append(row_list)

    # Vertical lines
    pygame.draw.line(self.game.screen, LINE_COLOR, (board_x + BOARD_SIZE // 3, board_y), (board_x + BOARD_SIZE // 3, board_y + BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(self.game.screen, LINE_COLOR, (board_x + 2 * BOARD_SIZE // 3, board_y), (board_x + 2 * BOARD_SIZE // 3, board_y + BOARD_SIZE), LINE_WIDTH)
    
    # Horizontal lines
    pygame.draw.line(self.game.screen, LINE_COLOR, (board_x, board_y + BOARD_SIZE // 3), (board_x + BOARD_SIZE, board_y + BOARD_SIZE // 3), LINE_WIDTH)
    pygame.draw.line(self.game.screen, LINE_COLOR, (board_x, board_y + 2 * BOARD_SIZE // 3), (board_x + BOARD_SIZE, board_y + 2 * BOARD_SIZE // 3), LINE_WIDTH)
    self.draw_x_o()

  def draw_x_o(self): 
    for i in range(0, 3):
      for j in range(0, 3):
        if self.x_o[i][j] != "":
          color = (255, 0, 0) if self.x_o[i][j] == "X" else (0, 0, 255)
          
          text_surface = self.game.font.render(self.x_o[i][j], True, color)  # Black text
          # Get the center of the rectangle
          text_rect = text_surface.get_rect(center=self.rects_list[i][j].center)
          # Blit the text on the screen
          self.game.screen.blit(text_surface, text_rect)

  def change_value(self, row, col):
    if self.x_o[row][col] == "" and self.winner == None:
      self.x_o[row][col] = self.player[self.turn]
      self.click_sound()
      if not self.check_win(): 
        self.change_turn()

  def change_turn(self):
    self.turn = 1 - self.turn

  def count_score(self):
    if self.winner == "X":
      self.x_score += 1
    elif self.winner == "O":
      self.o_score += 1

  def get_clicked_square(self, mouse_pos):
    rel_x = mouse_pos[0] - board_x
    rel_y = mouse_pos[1] - board_y
    if 0 <= rel_x < BOARD_SIZE and 0 <= rel_y < BOARD_SIZE:
      col = rel_x // (BOARD_SIZE // 3)  
      row = rel_y // (BOARD_SIZE // 3)
      return row, col
    return None

  def set_default(self):
    self.x_o = [["", "", ""], ["", "", ""], ["", "", ""]] 
    self.turn = 0
    self.winner = None
    self.end_game = False

  def show_score(self):
    x_score_text = self.game.font2.render(f"  X Score: {self.x_score}  ", True, (255, 255, 255), (46, 150, 64))
    o_score_text = self.game.font2.render(f"  {self.o_score} :O Score  ", True, (255, 255, 255), (46, 150, 64))
    message = self.game.font2.render(f"Click Space To Start New Game", True, (255, 255, 255))
    self.game.screen.blit(message, (WINDOW_WIDTH // 2 - message.get_width() // 2, WINDOW_HEIGHT - message.get_height() - 10))
    self.game.screen.blit(x_score_text, (10, 10))
    self.game.screen.blit(o_score_text, (WINDOW_WIDTH - o_score_text.get_width() - 10, 10))

  def show_winner_draw(self):
    if self.winner:
      win_message = self.game.font2.render(f"Player {self.winner} Won!", True, (255, 255, 255))
      self.game.screen.blit(win_message, (WINDOW_WIDTH // 2 - win_message.get_width() // 2, 20))
    elif self.check_draw():
      draw_message = self.game.font2.render(f"!!!Draw!!!", True, (255, 255, 255))
      self.game.screen.blit(draw_message, (WINDOW_WIDTH // 2 - draw_message.get_width() // 2, 20))

  def show_turn(self):
    if not self.winner and not self.check_draw():
      turn_message = self.game.font2.render(f"Turn: {self.player[self.turn]}", True, (255, 255, 255))
      self.game.screen.blit(turn_message, (WINDOW_WIDTH // 2 - turn_message.get_width() // 2, 20))

  def run(self):
    self.draw_board()
    self.show_turn()
    self.show_score()
    self.show_winner_draw()
    win_pos = self.check_win()

    if not self.end_game:
      if win_pos :
        self.end_game = True
        self.win_sound()
        self.winner = self.player[self.turn]
        self.count_score()
      elif self.check_draw():
        self.end_game = True
        self.draw_sound()

    if win_pos:
      self.draw_win_line(win_pos)

