#!/usr/bin/python3.7
### MDP Value Iteration and Policy Iteration
### Acknowledgement: start-up codes were adapted with permission from Prof. Emma Brunskill of Stanford University


import numpy as np
import gym
import time
# from lake_envs import *
import rmit_rl_env
import sys

np.set_printoptions(precision=3)

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

    P: nested dictionary
        From gym.core.Environment
        For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
        tuple of the form (probability, nextstate, reward, terminal) where
            - probability: float
                the probability of transitioning from "state" to "nextstate" with "action"
            - nextstate: int
                denotes the state we transition to (in range [0, nS - 1])
            - reward: int
                either 0 or 1, the reward for transitioning from "state" to
                "nextstate" with "action"
            - terminal: bool
              True when "nextstate" is a terminal state (hole or goal), False otherwise
    nS: int
        number of states in the environment
    nA: int
        number of actions in the environment
    gamma: float
        Discount factor. Number in range [0, 1]
"""


def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3):
    """Evaluate the value function from a given policy.

    Parameters
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    policy: np.array[nS]
        The policy to evaluate. Maps states to actions.
    tol: float
        Terminate policy evaluation when
            max |value_function(s) - prev_value_function(s)| < tol
    Returns
    -------
    value_function: np.ndarray[nS]
        The value function of the given policy, where value_function[s] is
        the value of state s
    """

    value_function = np.zeros(nS)

    ############################
    # YOUR IMPLEMENTATION HERE #

    new_value_func = value_function.copy()
    while True:
        for state in range(nS):
            state_detail = P[state]

            pr, next_state, reward = get_state_action_results(state_detail[policy[state]])

            for i in range(len(pr)):
                new_value_func[state] += pr[i] * (reward[i] + gamma * value_function[next_state[i]])

        if converge(value_function, new_value_func):
            break
        else:
            value_function = new_value_func.copy() # improve value function
            new_value_func = np.zeros(nS, dtype=float) # reset new value function to all 0

    ############################
    return new_value_func


def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
    """Given the value function from policy improve the policy.

    Parameters
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    value_from_policy: np.ndarray
        The value calculated from the policy
    policy: np.array
        The previous policy.

    Returns
    -------
    new_policy: np.ndarray[nS]
        An array of integers. Each integer is the optimal action to take
        in that state according to the environment dynamics and the
        given value function.
    """

    new_policy = np.zeros(nS, dtype='int')

    ############################
    # YOUR IMPLEMENTATION HERE #
    pi = np.zeros([nS, nA])
    for state in range(nS):
        for action in range(nA):
            result_filter = P[state][action]
            pr, next_state, reward = get_state_action_results(result_filter)

            for i in range(len(pr)):
                pi[state][action] += pr[i] * (reward[i] + gamma * value_from_policy[next_state][i])
    
    new_policy = np.argmax(pi, axis=1) # extract the optimal policy

    ############################
    return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, tol=10e-3):
    """Runs policy iteration.

    You should call the policy_evaluation() and policy_improvement() methods to
    implement this method.

    Parameters
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    tol: float
        tol parameter used in policy_evaluation()
    Returns:
    ----------
    value_function: np.ndarray[nS]
    policy: np.ndarray[nS]
    """

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)

    iteration_count = 0

    ############################
    # YOUR IMPLEMENTATION HERE #

    optimal_policy = False
    while not optimal_policy:
        iteration_count += 1
        value_function = policy_evaluation(P, nS, nA, policy)
        new_policy = policy_improvement(P, nS, nA, value_function, policy) # improve policy according to the given value function
        if np.array_equal(policy, new_policy): # when two policy are exactly the same - find the optimal policy
            optimal_policy = True
        else:
            policy = new_policy.copy()


    print("Number of iteration: " + str(iteration_count))

    ############################
    return value_function, policy


def value_iteration(P, nS, nA, gamma=0.9, tol=1e-3):
    """
    Learn value function and policy by using value iteration method for a given
    gamma and environment.

    Parameters:
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    tol: float
        Terminate value iteration when
            max |value_function(s) - prev_value_function(s)| < tol
    Returns:
    ----------
    value_function: np.ndarray[nS]
    policy: np.ndarray[nS]
    """

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)
    ############################
    # YOUR IMPLEMENTATION HERE #

    new_value_func = value_function.copy()

    iteration_count = 0

    while True:
        iteration_count += 1
        for state in range(nS):
            for action in range(nA):
                """
                loop through all states taking all actions to calculate Q value
                """

                temp_q_value = 0.0 # initiliaze q value
                possible_result = P[state][action] # list of result for one state taking action
                pr, next_state, reward = get_state_action_results(possible_result)

                q_value_list = list()

                for i in range(len(pr)):
                    temp_q_value += pr[i] * (reward[i] + gamma * value_function[next_state[i]]) # calculate q value
                    q_value_list.append(temp_q_value)

                q_value = max(q_value_list) # get highest q value
                if q_value > new_value_func[state]:
                    new_value_func[state] = q_value

        if converge(value_function, new_value_func):
            break
        else:
            value_function = new_value_func.copy()

    policy = policy_improvement(P, nS, nA, value_function, policy) # improve policy according to value function

    print("Number of iteration: " + str(iteration_count))

    ############################
    return value_function, policy

def get_state_action_results(state_action):
    """
    get all probability, next state and reward for one state taking actoins

    Param:
        state_action: list of result for one state taking action
    """

    pr_list = list()
    next_state_list = list()
    reward_list = list()
    for result in state_action:
        pr_list.append(result[0])
        next_state_list.append(result[1])
        reward_list.append(result[2])

    return pr_list, next_state_list, reward_list

def converge(value, new_value, tol=1e-3):
    return np.all(np.abs(value - new_value) < tol)

def render_single(env, policy, max_steps=100):
    """
    This function does not need to be modified
    Renders policy once on environment. Watch your agent play!

    Parameters
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as
      attributes.
    Policy: np.array of shape [env.nS]
      The action to take at a given state
  """

    episode_reward = 0
    ob = env.reset()
    for t in range(max_steps):
        env.render()
        time.sleep(0.25)
        a = policy[ob]
        ob, rew, done, _ = env.step(a)
        episode_reward += rew
        if done:
            break
    env.render()
    if not done:
        print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
    else:
        print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":
    # comment/uncomment these lines to switch between deterministic/stochastic environments

    # Deterministic Frozen Lake Environment
    env = gym.make("Deterministic-4x4-FrozenLake-v0")
    print("="*10 + "Deterministic FrozenLake" + "="*10)
    print("\n" + "-" * 25 + "\nBeginning Policy Iteration\n" + "-" * 25)

    V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
    print("Option Value Funtion: " + str(V_pi))
    print("Opitmal Policy: " + str(p_pi))
    # render_single(env, p_pi, 100)

    print("\n" + "-" * 25 + "\nBeginning Value Iteration\n" + "-" * 25)

    V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
    print("Optimal Value Function: " + str(V_vi))
    print("Optimal Policy: " + str(p_vi))
    # render_single(env, p_vi, 100)

    print()

    # Stochastic Frozen Lake Environment!
    env = gym.make("Stochastic-4x4-FrozenLake-v0")
    print("="*10 + "Stochastic FrozenLake" + "="*10)
    print("\n" + "-" * 25 + "\nBeginning Policy Iteration\n" + "-" * 25)

    V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
    print("Option Value Funtion: " + str(V_pi))
    print("Opitmal Policy: " + str(p_pi))
    # render_single(env, p_pi, 100)

    print("\n" + "-" * 25 + "\nBeginning Value Iteration\n" + "-" * 25)

    V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
    print("Optimal Value Function: " + str(V_vi))
    print("Optimal Policy: " + str(p_vi))
    # render_single(env, p_vi, 100)
