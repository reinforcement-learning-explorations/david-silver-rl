import getopt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import numpy as np
from environment.easy21 import Easy21
from utilities.plotter import value_fn_plotter


def monte_carlo_control():
    nS = 210
    nA = 2

    Q = np.zeros(shape=(10, 21, nA))
    N = np.zeros(shape=(10, 21, nA))
    policy = np.zeros(shape=(10, 21), dtype=int)

    gamma = 0.9
    tol = 10e-3

    converged = 0
    episodes = []
    for i in range(iterations):
        episode = []
        game = Easy21(0)
        game.start()
        G = 0
        while not game.terminal:
            i, j = game.s
            action = policy[i-1, j-1]
            s, r = game.step(action)
            episode.append([[i, j], action, r])
            G += r

        Q = monte_carlo_policy_evaluation(Q, N, G, episode, policy, gamma)
        policy_update = e_greedy_policy_improvement(Q, N, policy, episode, nS, nA)

        episodes.append(episode)
        if np.array_equal(policy, policy_update):
            converged = 1
        else:
            policy = policy_update.copy()

    # generate optimal value fn by choosing the best action given the action value fn & state
    V = np.zeros(shape=(10,21))
    for i in range(np.shape(Q)[0]):
        for j in range(np.shape(Q)[1]):
            V[i, j] = max(Q[i, j,:])
    value_fn_plotter(V)


def monte_carlo_policy_evaluation(Q, N, G, episode, policy, gamma):
    for s, a, r in episode:
        # G += gamma * G + r
        # compute the action-value update
        i, j = s
        i -= 1
        j -= 1
        N[i,j,a] += 1
        Q[i,j,a] += (1 / N[i,j,a]) * (G - Q[i,j,a])
    return Q


def e_greedy_policy_improvement(Q, N, policy, episode, nS, nA):
    policy_update = policy.copy()
    epsilon = 0
    for s, a, r in episode:
        i, j = s
        i -= 1
        j -= 1
        epsilon = 100 / (100 + max(N[i,j,:]))
        p_greedy = (epsilon / nA) + 1 - epsilon
        p_random = epsilon / nA
        if np.random.choice([1, 0], p=[p_greedy, p_random]):
            policy_update[i,j] = np.argmax(Q[i,j,:])
        else:
            policy_update[i,j] = np.random.choice([0,1])
    return policy_update


def command_line(argv):
    global iterations
    try:
        opts, args = getopt.getopt(argv, "i:")
    except getopt.GetoptError:
        print("-i or no args")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', "--iterations"):
            iterations = int(arg)
            print("---Iterations: " + arg + "---")


if __name__ == "__main__":
    iterations = 1000
    command_line(sys.argv[1:])
    monte_carlo_control()
