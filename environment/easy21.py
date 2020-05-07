import numpy as np


class Easy21:
    def __init__(self, cl=1):
        self.s = [0, 0]
        self.s[0] = self.draw_card(0)[0]
        self.s[1] = self.draw_card(0)[0]
        self.terminal = 0
        self.command_line = cl

    def state(self):
        return self.s[0], self.s[1]

    def start(self):
        if self.command_line:
            print("---Start state [dealer, player]: ", self.s, "---")
            while not self.terminal:
                self.a = int(input("Enter 1 to twist or 0 to stick: "))
                self.s, self.reward = self.step(self.a)

    def draw_card(self, c=1):
        n = 0
        color = "black"
        if c:
            n = np.random.randint(1, 11)
            colors = ["red", "black", "black"]
            color = colors[np.random.randint(0, 3)]
        else:
            n = np.random.randint(1, 11)
        return n, color

    def state_update(self, p, s, n, color):
        if (color == "red"):
            s[p] -= n
        else:
            s[p] += n
        return s

    def dealers_turn(self, s):
        while s[0] < 17 and s[0] > 0:
            n, color = self.draw_card()
            s = self.state_update(0, s, n, color)
        return s

    def check_bust(self, p, s):
        if s[p] > 21 or s[p] < 1:
            if p:
                title = "player"
            else:
                title = "dealer"
            if self.command_line:
                print("---" + title + " busted---")
            return 1
        else:
            return 0

    def declare_victor(self, s):
        if self.check_bust(0, s):
            return 1
        else:
            if s[0] > s[1]:
                return (-1)
            elif s[0] < s[1]:
                return 1
            else:
                return 0

    def step(self, a):
        if self.command_line:
            print(self.s, a)
        reward = 0
        if(a == 1):
            n, color = self.draw_card()
            if self.command_line:
                print(n, color)
            self.s = self.state_update(1, self.s, n, color)
            if self.command_line:
                print(self.s)
            if self.check_bust(1, self.s):
                reward = (-1)
            if reward != 0:
                self.terminal = 1
        else:
            self.s = self.dealers_turn(self.s)
            if self.command_line:
                print("---dealer's turn complete: ", self.s, "---")
            reward = self.declare_victor(self.s)
            self.terminal = 1
        return (self.s[0], self.s[1]), reward
