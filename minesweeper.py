import tkinter as tk
from tkinter import messagebox
import random

class Cell:
    def __init__(self, master, x, y, click_callback, flag_callback):
        self.master = master
        self.button = tk.Button(master, width=2, height=1, font=("Arial", 14), relief="raised")
        self.button.grid(row=y, column=x)
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.click_callback = click_callback
        self.flag_callback = flag_callback
        self.button.bind("<Button-1>", self.left_click)   # 左鍵
        self.button.bind("<Button-3>", self.right_click)  # 右鍵

    def left_click(self, event):
        if not self.is_flagged:
            self.click_callback(self.x, self.y)

    def right_click(self, event):
        self.flag_callback(self.x, self.y)

    def reveal(self, text='', color='black'):
        self.button.config(text=text, relief="sunken", state="disabled", disabledforeground=color)
        self.is_revealed = True

    def flag(self):
        if not self.is_flagged:
            self.button.config(text="🚩", fg="red")
            self.is_flagged = True
        else:
            self.button.config(text="")
            self.is_flagged = False


class Minesweeper:
    def __init__(self, root, width=10, height=10, mines=10):
        self.root = root
        self.width = width
        self.height = height
        self.total_mines = mines
        self.cells = []
        self.mines = set()
        self.setup_game()

    def setup_game(self):
        self.cells = []
        self.mines = set()
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(self.root, x, y, self.reveal_cell, self.flag_cell)
                row.append(cell)
            self.cells.append(row)

        while len(self.mines) < self.total_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.cells[y][x].is_mine:
                self.cells[y][x].is_mine = True
                self.mines.add((x, y))

    def reveal_cell(self, x, y):
        cell = self.cells[y][x]
        if cell.is_revealed or cell.is_flagged:
            return
        if cell.is_mine:
            cell.reveal("💣", color="red")
            self.game_over(False)
            return

        count = self.count_adjacent_mines(x, y)
        cell.reveal(text=str(count) if count > 0 else "", color=self.color_for_count(count))
        if count == 0:
            for nx, ny in self.get_neighbors(x, y):
                self.reveal_cell(nx, ny)

        if self.check_win():
            self.game_over(True)

    def flag_cell(self, x, y):
        cell = self.cells[y][x]
        if not cell.is_revealed:
            cell.flag()

    def count_adjacent_mines(self, x, y):
        return sum(1 for nx, ny in self.get_neighbors(x, y) if self.cells[ny][nx].is_mine)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (dx != 0 or dy != 0):
                    neighbors.append((nx, ny))
        return neighbors

    def game_over(self, won):
        for x, y in self.mines:
            if not self.cells[y][x].is_flagged:
                self.cells[y][x].reveal("💣", color="red")
        msg = "你贏了！🎉" if won else "踩到地雷啦 💥"
        messagebox.showinfo("遊戲結束", msg)
        self.root.quit()

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def color_for_count(self, count):
        colors = ["black", "blue", "green", "red", "purple", "maroon", "turquoise", "gray"]
        return colors[count] if 0 < count < len(colors) else "black"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("踩地雷 Minesweeper")
    game = Minesweeper(root, width=10, height=10, mines=10)
    root.mainloop()
