import getopt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from collections import defaultdict
from utilities.plotter import value_fn_plotter, mean_sq_error_plotter
from utilities import model_store as ms
from environment.easy21 import Easy21
import numpy as np



def sarsa_lambda(episodes, λ, valuefn=False):
    global Q_star
    global mse
    global mse_episode
    mse_episode[λ] = []
    nsX = 10
    nsY = 21
    nA = 2

    # Q = np.zeros(shape=(11, 22, nA))
    # defaultdict allows keys !in dict to auto create new entries
    Q = defaultdict(int)
    N = defaultdict(int)
    gamma = 1
    tol = 10e-3

    for i in range(episodes):
        E = defaultdict(int)
        game = Easy21(0)
        game.start()
        a = epsilon_greedy(game.state(), Q, N, nA)
        N[game.state(), a] += 1
        while not game.terminal:
            # sample the environment
            s = game.state()
            s_prime, reward = game.step(a)

            a_prime = epsilon_greedy(s_prime, Q, N, nA)

            td_error = reward + gamma * Q[s_prime, a_prime] - Q[s, a]
            E[s, a] += 1
            N[s_prime, a_prime] += 1
            # update Q for states visited this episode
            for s, a in E:
                Q[s, a] += (1 / N[s, a]) * td_error * E[s, a]
                E[s, a] *= gamma * λ
            a = a_prime

        # of course this adds some overhead
        mse_e = 0
        for i in range(nsX):
            for j in range(nsY):
                mse_e += (Q[(i,j),0] - Q_star[i-1][j-1][0])** 2
                mse_e += (Q[(i,j),1] - Q_star[i-1][j-1][1])** 2
        mse_episode[λ].append(mse_e/(nsX*nsY*nA))

    # generate optimal value fn by choosing the best action given the action value fn & state
    # calculate the mean squared error
    V = np.zeros(shape=(nsX, nsY))
    mse_error = 0
    for i in range(nsX):
        for j in range(nsY):
            V[i, j] = max(Q[(i, j), 0], Q[(i, j), 1])
            mse_error += (Q[(i,j),0] - Q_star[i-1][j-1][0])** 2
            mse_error += (Q[(i,j),1] - Q_star[i-1][j-1][1])** 2
    mse.append(mse_error/(nsX*nsY*nA))

    if valuefn:
        value_fn_plotter(V, [(1, nsX, 1), (1, nsY, 4)], "Sarsa(" + str(λ) + ") V(s,a) " + str(episodes) + \
            " Episodes", ("DEALER", "PLAYER", "V"), "./plots/λ-"+str(λ)+"_E-"+str(episodes)+".png")

# ε-greedy policy -> get next action
def epsilon_greedy(s, Q, N, nA):
    epsilon = 100 / (100 + N[s, 0] + N[s, 1])
    p_greedy = (epsilon / nA) + 1 - epsilon
    p_random = epsilon / nA
    a = 0
    if np.random.choice([1, 0], p=[p_greedy, p_random]):
        a = np.argmax([Q[s, 0], Q[s, 1]])
    else:
        a = np.random.choice([0, 1])
    return a


def command_line(argv):
    global episodes
    global λ
    global valuefn
    try:
        opts, args = getopt.getopt(argv, "e:l:v")
    except getopt.GetoptError:
        print("args: -e, -l, -v || -episodes, -lambda, -valuefn")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-e', "--episodes"):
            episodes = int(arg)
            print("---EPISODES: " + arg + "---")
        if opt in ('-l', "--lambda"):
            λ = float(arg)
            print("---λ: " + arg + "---")
        if opt in ('-v', "--valuefn"):
            valuefn = True

if __name__ == "__main__":
    valuefn = False
    episodes = 1000
    Q_star = ms.load("../model-data/q-functions/easy21_mcControl_E-100000")
    mse_episode = defaultdict(int)
    mse = []
    λ = [i/10 for i in range(11)]
    command_line(sys.argv[1:])

    for l in λ:
        sarsa_lambda(episodes, l, valuefn)

    mean_sq_error_plotter(mse, λ, "MSE: Sarsa(λ) vs Monte-Carlo Control - " + str(episodes) + " Episodes", "λ", "./plots/mse_vs_λ_sarsaλ_vs_mcControl_e" + str(episodes))

    mean_sq_error_plotter(mse_episode, λ, "MSE: Sarsa(λ) vs Monte-Carlo Control - " + str(episodes) + " Episodes", "EPISODES", "./plots/mse_vs_e_sarsaλ_vs_mcControl_e" + str(episodes), legend=True)
