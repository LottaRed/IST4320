import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        self.width = 500
        self.height = 500
        self.cell_size = 20
        
        self.score = 0
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.snake = [(0, 0), (self.cell_size, 0), (self.cell_size * 2, 0)]
        self.snake_dir = "Right"
        self.food = None
        self.create_food()
        
        self.game_running = True
        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.pack()

    def create_food(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            self.food = (x, y)
            if self.food not in self.snake:
                break
        self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="red", tag="food")

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            new_dir = event.keysym
            # Prevent the snake from reversing
            opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
            if new_dir != opposites[self.snake_dir]:
                self.snake_dir = new_dir

    def update(self):
        if not self.game_running:
            return
        
        x, y = self.snake[-1]
        if self.snake_dir == "Left":
            x -= self.cell_size
        elif self.snake_dir == "Right":
            x += self.cell_size
        elif self.snake_dir == "Up":
            y -= self.cell_size
        elif self.snake_dir == "Down":
            y += self.cell_size
        
        new_head = (x, y)
        
        if (x < 0 or x >= self.width or y < 0 or y >= self.height or new_head in self.snake):
            self.game_over()
            return
        
        self.snake.append(new_head)
        
        if new_head == self.food:
            self.canvas.delete("food")
            self.create_food()
            self.update_score()
        else:
            self.snake.pop(0)
        
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.cell_size, segment[1] + self.cell_size, fill="green", tag="snake")
        
        self.root.after(100, self.update)
    
    def update_score(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(self.width / 2, self.height / 2, text="Game Over", fill="white", font=("Arial", 24))
    
    def restart_game(self):
        self.canvas.delete("all")
        self.snake = [(0, 0), (self.cell_size, 0), (self.cell_size * 2, 0)]
        self.snake_dir = "Right"
        self.create_food()
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.game_running = True
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()