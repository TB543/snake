from tkinter import *
from random import choice
from time import sleep


class Snake(Tk):
    """
    A class for the game of snake.

    Rules:
        1) move with wasd
        2) avoid hitting walls and snake body
        3) eat more food to grow
        4) grow as large as possible
        5) press esc to pause
    """

    def __init__(self):
        """
        Creates the snake game

        The following components are created:
            1) the gui
            2) bindings for the keys
        """

        # creates the window
        super().__init__()
        self.title('Snake')
        self.geometry('850x650')
        self.resizable(0, 0)

        # creates the canvas
        self.canvas = Canvas(self, bg='gray')
        self.canvas.pack(fill=BOTH, expand=True)

        # creates labels
        self.pause_label = Label(self, text='Game Paused\nPress Escape To Start', bg='gray', font=100)
        self.start = Label(self, text='Press Space To Start', bg='gray', font=100)
        self.start.place(relx=.5, rely=.5, anchor=CENTER)

        # sets up key-binds
        self.bind('<space>', lambda event: self.setup())
        self.bind('w', self.handle_key)
        self.bind('a', self.handle_key)
        self.bind('s', self.handle_key)
        self.bind('d', self.handle_key)

        # starts the game
        self.mainloop()

    def setup(self):
        """
        sets up variables for the game:
            1) default snake starting position and direction
            2) generates food
        """

        # binds keys to actions
        self.unbind('<space>')
        self.bind('<Escape>', lambda event: self.pause())

        # creates the snake and food
        self.body = [(8, 7), (8, 8), (8, 9)]
        self.generate_food()
        self.draw()

        # other setup actions
        self.start.place_forget()
        self.facing = N
        self.running = True
        self.paused = False

        # starts game
        self.game()

    def pause(self):
        """
        pauses the game until the player presses escape again
        """

        if self.paused:
            self.game()
            self.pause_label.place_forget()
            self.paused = False
        else:
            self.after_cancel(self.game_loop)
            self.pause_label.place(relx=.5, rely=.5, anchor=CENTER)
            self.paused = True

    def handle_key(self, key):
        """
        Handles key presses

        Key-binds:
            1) W moves the snake north
            2) A moves the snake west
            3) S moves the snake south
            4) D moves the snake east
        ** note: the snake can only change to a direction that is not opposite to the one it is currently facing
        ie. cannot go north if already facing south **

        :param key: the key event that occurred
        """

        # updates keys when they are pressed
        self.facing = N if key.char == 'w' and self.facing != S else self.facing
        self.facing = W if key.char == 'a' and self.facing != E else self.facing
        self.facing = S if key.char == 's' and self.facing != N else self.facing
        self.facing = E if key.char == 'd' and self.facing != W else self.facing

    def generate_food(self):
        """
        generates a new bit of food for the snake to eat
        """

        # generates a new food bit
        game = [(x, y) for x in range(17) for y in range(13)]
        for body in self.body:
            game.remove(body)
        self.food = choice(game)

    def draw(self):
        """
        draws all the game components to the screen
            1) the snake and its body parts
            2) the food bit
        """

        # draws the snake
        self.canvas.delete('all')
        for body in self.body:
            self.canvas.create_rectangle(body[0] * 50, body[1] * 50,
                                         body[0] * 50 + 50, body[1] * 50 + 50, fill='green')

        # draws the food
        self.canvas.create_rectangle(self.food[0] * 50, self.food[1] * 50,
                                     self.food[0] * 50 + 50, self.food[1] * 50 + 50, fill='red')

    def move(self):
        """
        moves the snake:
            1) move the head
            2) removes ending body part
        """

        # moves the head north
        if self.facing == N:
            self.body.insert(0, (self.body[0][0], self.body[0][1] - 1))

        # moves the head east
        elif self.facing == E:
            self.body.insert(0, (self.body[0][0] + 1, self.body[0][1]))

        # moves the head south
        elif self.facing == S:
            self.body.insert(0, (self.body[0][0], self.body[0][1] + 1))

        # moves the head west
        else:
            self.body.insert(0, (self.body[0][0] - 1, self.body[0][1]))

    def collisions(self):
        """
        checks and handles collisions:
            1) collisions with snake
            2) collisions with food
            3) collisions with walls
        """

        # checks for wall collisions
        if self.body[0][0] == -1 or self.body[0][1] == -1 or self.body[0][0] == 17 or self.body[0][1] == 13:
            self.running = False

        # checks for body collisions
        for body in self.body[1:]:
            if self.body[0] == body:
                self.running = False

        # checks for food collisions
        if self.body[0] == self.food:
            self.generate_food()
        else:
            self.body.pop()

    def game(self):
        """
        The main loop where the game will run

        Performs the following tasks:
            1) moves the snake
            2) checks for collisions with food, snake and walls
            3) updates gui
        """

        # game mainloop
        if self.running:
            self.draw()
            self.move()
            self.collisions()
            self.game_loop = self.after(300, self.game)

        # game loss
        else:
            self.start = Label(self, text=f'You Got A Score Of {len(self.body)}\nPress Space To Play Again', bg='gray',
                               font=100)
            self.start.place(relx=.5, rely=.5, anchor=CENTER)
            self.bind('<space>', lambda event: self.setup())
            self.unbind('<Escape>')


if __name__ == '__main__':
    Snake()
