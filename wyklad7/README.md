Agent — the learner and the decision maker.
Environment — where the agent learns and decides what actions to perform.
Action — a set of actions which the agent can perform.
State — the state of the agent in the environment.
Reward — for each action selected by the agent the environment provides a reward. Usually a scalar value.
Policy — the decision-making function (control strategy) of the agent, which represents a mapping from situations to actions.
Value function — mapping from states to real numbers, where the value of a state represents the long-term reward achieved starting from that state, and executing a particular policy.
Function approximator — refers to the problem of inducing a function from training examples. Standard approximators include decision trees, neural networks, and nearest-neighbor methods
Markov decision process (MDP) — A probabilistic model of a sequential decision problem, where states can be perceived exactly, and the current state and action selected determine a probability distribution on future states. Essentially, the outcome of applying an action to a state depends only on the current action and state (and not on preceding actions or states).
Dynamic programming (DP) — is a class of solution methods for solving sequential decision problems with a compositional cost structure. Richard Bellman was one of the principal founders of this approach.
Monte Carlo methods — A class of methods for learning of value functions, which estimates the value of a state by running many trials starting at that state, then averages the total rewards received on those trials.
Temporal Difference (TD) algorithms — A class of learning methods, based on the idea of comparing temporally successive predictions. Possibly the single most fundamental idea in all of reinforcement learning.
Model — The agent’s view of the environment, which maps state-action pairs to probability distributions over states. Note that not every reinforcement learning agent uses a model of its environment


Pacman (Atari):

Stan = obraz (210×160×3)

Akcje = dyskretne (NOOP, LEFT, RIGHT, UP, DOWN…)

Nagroda = punkty z gry

❌ Q-table NIE DZIAŁA

✅ Deep Reinforcement Learning (DQN)