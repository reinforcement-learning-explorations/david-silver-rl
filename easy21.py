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

def main():
    s = (np.random.randint(1, 11), np.random.randint(1, 22))
    a = np.random.randint(0,2)
    step(s, a)

def step(s, a):
    print(s, a)


if __name__ == "__main__":
    command_line(sys.argv[1:])

    main()
