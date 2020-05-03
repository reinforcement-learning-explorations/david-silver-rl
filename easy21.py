import numpy as np
import sys
import getopt


def command_line(argv):
    try:
        opts, args = getopt.getopt(argv, "t")
    except getopt.GetoptError:
        print("-t or no args")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-t', "--terminal"):
            print("---TERMINAL OUTPUT MODE---")


def draw_card(c=1):
    n = 0
    color = "black"
    if c:
        n = np.random.randint(1, 11)
        colors = ["red", "black", "black"]
        color = colors[np.random.randint(0, 3)]
    else:
        n = np.random.randint(1, 11)
    return n, color


def state_update(p, s, n, color):
    if (color == "red"):
        s[p] -= n
    else:
        s[p] += n
    return s


def dealers_turn(s):
    while s[0] < 17 and s[0] > 0:
        n, color = draw_card()
        s = state_update(0, s, n, color)
    return s


def check_bust(p, s):
    if s[p] > 21 or s[p] < 1:
        if p:
            title = "player"
        else:
            title = "dealer"
        print("---" + title + " busted---")
        return 1
    else:
        return 0


def declare_victor(s):
    if check_bust(0, s):
        return 1
    else:
        if s[0] > s[1]:
            return (-1)
        elif s[0] < s[1]:
            return 1
        else:
            return 0


def step(s, a):
    print(s, a)
    reward = 0
    finished = 0
    if(a == 1):
        n, color = draw_card()
        print(n, color)
        s = state_update(1, s, n, color)
        print(s)
        if check_bust(1, s):
            reward = (-1)
        if reward != 0:
            finished = 1
    else:
        s = dealers_turn(s)
        print("---dealer's turn complete: ", s, "---")
        reward = declare_victor(s)
        finished = 1
    return s, reward, finished


def main():
    s = [0, 0]
    s[0] = draw_card(0)[0]
    s[1] = draw_card(0)[0]
    finished = 0
    print("---Start state [dealer, player]: ", s, "---")

    while not finished:
        a = int(input("Enter 1 to twist or 0 to stick: "))
        s, reward, finished = step(s, a)

if __name__ == "__main__":
    command_line(sys.argv[1:])
    main()
