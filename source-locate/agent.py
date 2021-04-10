import random
import sys
from environment import Environment
from utils import debug_print
import numpy as np
REWARD = 100
# Template for the agent containing agents x and y coordinate within the world.
# Contains fnx initializing the location of the agent within the world
# fnx is_at provides agent location at specific step in the world
# fnx move updates agent location based off of change in x and y
# fnx move_: e,w,n,s provide changes to the appropriate coordinate to move N, S, E, W.  origin at bottom left


class Agent:

    POSX = (1, 0, 0)
    NEGX = (-1, 0, 0)
    NONE = 'none'
    NEGY = (0, -1, 0)
    POSY = (0, 1, 0)
    POSZ = (0, 0, 1)
    NEGZ = (0, 0 -1)

    MOVES = [NEGY, POSY, POSX, NEGX, POSZ, NEGZ]

    def __init__(self, x, y, z, space_width, space_height, space_depth, epsilon_decay=0.9999):
        self.x = x
        self.y = y
        self.z = z
        self.width = space_width
        self.height = space_height
        self.depth = space_depth

        self.epsilon_decay = epsilon_decay

        # Exploration Factor: 1-epsilon, where epsilon range between 0 to 1,
        # make a random choice epsilon = 1,
        # strictly follow policy epsilon = 0
        # some float combination of the random and policy
        self.epsilon = 1

        # Discount Factor: Gamma is
        # multiplied by the estimation of the optimal future value.
        # The next reward’s importance is defined by the gamma parameter.
        self.gamma = 0.9

        # Initializes the previous_action to NONE. keeps track of the action taken prior to get to current tile
        self.previous_action = Agent.NONE
        # Initializes the previous_state to 0. keeps track of the status in the tile visited prior
        # location, pollution, DO2, reward
        # Make Dict
        self.experiences = []
        # Make 3D numpy array
        self.utility_table = np.zeros((self.width, self.height, self.depth))

    def location_string(self):
        return '(%s, %s, %s)' % (self.x, self.y, self.z)

    def last_pollution(self):
        if len(self.experiences) == 0:
            return 0
        return self.experiences[len(self.experiences) - 1][1]

    def last_do2(self):
        if len(self.experiences) == 0:
            return 0
        return self.experiences[len(self.experiences) - 1][2]

    def potential_moves(self):
        moves = []
        if self.x > 0:
            moves.append(Agent.NEGX)

        if self.x < self.width - 1:
            moves.append(Agent.POSX)

        if self.y > 0:
            moves.append(Agent.POSY)

        if self.y < self.height - 1:
            moves.append(Agent.NEGY)

        if self.z > 0:
            moves.append(Agent.POSZ)

        if self.z < self.depth - 1:
            moves.append(Agent.NEGZ)

        return moves

    # Need exploitation
        # need best utility and best action. both initialized to none.
        # needs next location

    def choose_action(self, environment: Environment):


        # perceive environment status based on location
        pollution = environment.get_pollution(self.x, self.y, self.z)
        do2 = environment.get_do2(self.x, self.y, self.z)

        # if agent is at source it will do nothing
        if pollution == Environment.SOURCE:
            debug_print('source found at, %s. Pollution: %s do2: %s' % (self.location_string(), pollution, do2))
            print('Found Source')
            return Agent.NONE

        # if agent is at the NEGX boundary and corner will move in bounds
        # These are the 8 corner cases
        # ----------------------------------------------
        if self.x == 0 and self.y == 0 and self.z == 0:
            action = random.choice((Agent.POSX, Agent.POSY, Agent.POSZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y == 0 and self.z == environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.POSY, Agent.NEGZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y == environment.height - 1 and self.z == 0:
            action = random.choice((Agent.POSX, Agent.NEGY, Agent.POSZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y == environment.height - 1 and self.z == environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGY, Agent.NEGZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y == 0 and self.z == environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.POSY, Agent.NEGZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y == environment.height - 1 and self.z == environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.NEGY, Agent.NEGZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y == 0 and self.z == 0:
            action = random.choice((Agent.NEGX, Agent.POSY, Agent.POSZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y == environment.height - 1 and self.z == 0:
            action = random.choice((Agent.NEGX, Agent.NEGY, Agent.POSZ))
            debug_print('Agent in corner. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action
        # ----------------------------------------------
        # 12 edges
        # ----------------------------------------------
        elif self.x == 0 and self.y < environment.height - 1 and self.z == 0:
            action = random.choice((Agent.POSX, Agent.NEGY, Agent.POSY, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y == environment.height - 1 and self.z == 0 :
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.NEGY, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y == 0 and self.z == 0:
            action = random.choice((Agent.NEGX, Agent.POSX, Agent.POSY, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y == 0 and self.z < environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.POSY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y < environment.height - 1 and self.z == 0:
            action = random.choice((Agent.NEGX, Agent.NEGY, Agent.POSY, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y == environment.height - 1 and self.z < environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y < environment.height - 1 and self.z == environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGY, Agent.POSY, Agent.NEGZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y == 0 and self.z == environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.POSY, Agent.NEGZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y == environment.height - 1 and self.z == environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.POSX, Agent.NEGY, Agent.NEGZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y == 0 and self.z < environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.POSY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y < environment.height - 1 and self.z == environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.NEGY, Agent.POSY, Agent.NEGZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y == environment.height - 1 and self.z < environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.NEGY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on edge. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action
        # ----------------------------------------------
        # 6 faces
        # ----------------------------------------------
        elif self.x < environment.width - 1 and self.y < environment.height - 1 and self.z == 0:
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.POSY, Agent.NEGY, Agent.POSZ))
            debug_print('Agent on face 1. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == 0 and self.y < environment.height - 1 and self.z < environment.depth - 1 :
            action = random.choice((Agent.POSX, Agent.POSY, Agent.NEGY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on face 2. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y == 0 and self.z < environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.POSY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on face 3. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y < environment.height - 1 and self.z == environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.POSY, Agent.NEGY, Agent.NEGZ))
            debug_print('Agent on face 4. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x < environment.width - 1 and self.y == environment.height - 1 and self.z < environment.depth - 1:
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.NEGY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on face 5. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        elif self.x == environment.width - 1 and self.y < environment.height - 1 and self.z < environment.depth - 1:
            action = random.choice((Agent.NEGX, Agent.POSY, Agent.NEGY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent on face 6. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        else:
            action = random.choice((Agent.POSX, Agent.NEGX, Agent.POSY, Agent.NEGY, Agent.NEGZ, Agent.POSZ))
            debug_print('Agent is within bounds. Moving %s from %s. Pollution: %s do2: %s'
                        % (action, self.location_string(), pollution, do2))
            return action

        # Error checking
        if self.x or self.y or self.z < 0:
            print('ERROR: Agent is outside of bounds, exiting')
            sys.exit()
        # prevents agent from getting stuck in initial "previous_action"
        if self.previous_action == Agent.NONE:
            return random.choice((Agent.NEGX, Agent.POSX, Agent.NEGY, Agent.POSY, Agent.NEGZ, Agent.POSZ))

        # # exploration using epsilon decay
        # # encourages agent to explore early in the process
        # moves = self.potential_moves()
        # if random.random() < self.epsilon:
        #     return random.choice(moves)
        #
        # # Exploitation of Action Policy
        # # exploit
        # best_utility = None
        # best_move = None
        # for move in moves:
        #     next_location = self.next_local(move)
        #     utility = self.utility_table[next_location[1] * self.width + next_location[0]]
        #     if best_utility is None or utility > best_utility:
        #         best_utility = utility
        #         best_move = move
        #
        # return best_move

        # if pollution is increasing and DO2 is decreasing the agent will return the previous action otherwise random.
        if do2 < self.last_do2():
            debug_print('Moving %s, from %s pollution: %s do2: %s.'
                        % (self.previous_action, self.location_string(), pollution, do2))
            return self.previous_action

        if do2 == self.last_do2():
            if pollution >= self.last_pollution():
                debug_print('Moving %s, from %s pollution: %s do2: %s.'
                            % (self.previous_action, self.location_string(), pollution, do2))
                return self.previous_action
            else:
                action = random.choice((Agent.NEGX, Agent.POSX, Agent.NEGY, Agent.POSY, Agent.POSZ, Agent.NEGZ))
                debug_print('Moving %s from %s pollution: %s , DO2: %s'
                            % (action, self.location_string(), pollution, do2))
                return action

        if do2 > self.last_do2():
            action = random.choice((Agent.NEGX, Agent.POSX, Agent.NEGY, Agent.POSY, Agent.POSZ, Agent.NEGZ))
            # debug_print('DO2 increasing. Moving %s' % action)
            return action

        print("unknown status:", pollution)

    def is_at(self, x, y, z):
        # print(x, y, z)
        return self.x == x and self.y == y and self.z == z

    def update_utilities(self):
        exp_count = len(self.experiences)
        trial_u = [0] * exp_count
        for exp_idx in range(exp_count, 0, -1):
            experience = self.experiences[exp_idx-1]
            exp_reward = experience[3]
            for r_idx in range(exp_idx, 0, -1):
                trial_u[r_idx-1] += exp_reward
                exp_reward *= self.gamma

        for exp_idx in range(exp_count):
            experience = self.experiences[exp_idx]
            x, y, z = experience[0]
            current_utility = self.utility_table[y * self.width + x * self.height + z]
            self.utility_table[y * self.width + x * self.height + z] = (current_utility + trial_u[exp_idx]) / 2

    def print_utilities(self):
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    print('{:.2f} '.format(self.utility_table[y * self.width + x * self.height + z]), end='')
            print()

    def reset(self):
        self.epsilon *= self.epsilon_decay
        self.x = 0
        self.y = 0
        self.z = 0
        self.experiences.clear()

    # def reward(self, environment):
    #     reward = 0
    #     if environment.is_goal(self.x, self.y):
    #         reward = REWARD
    #     return reward

    # Pollution reward
    def reward(self, environment):
        return environment.get_pollution(self.x, self.y, self.z)

    def act(self, action, environment: Environment):
        # allows agent to know action and status of prior environment
        pollution = environment.get_pollution(self.x, self.y, self.z)
        do2 = environment.get_do2(self.x, self.y, self.z)

        self.previous_action = action

        # if action = NONE that means agent is at the source and should stop.
        if action == Agent.NONE:
            return

        # in case the action is left location equals location - 1
        if action == Agent.NEGX:
            self.move_NEGX()

        #   in case the action is right location equals location + 1
        if action == Agent.POSX:
            self.move_POSX()

        #   in case the action is right location equals location + 1
        if action == Agent.POSY:
            self.move_POSY()

        #   in case the action is right location equals location + 1
        if action == Agent.NEGY:
            self.move_NEGY()

        #   in case the action is right location equals location + 1
        if action == Agent.POSZ:
           self.move_POSZ()

        #   in case the action is left location equals location - 1
        if action == Agent.NEGZ:
          self.move_NEGZ()

        reward = self.reward(environment)
        # Make experiences a dict with key being x, y, z
        self.experiences.append(
            (
                (self.x, self.y, self.z),
                pollution,
                do2,
                reward
            )
        )

    def move(self, delta_x, delta_y, delta_z):
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

    def move_POSX(self):
        self.move(1, 0, 0)

    def move_NEGX(self):
        self.move(-1, 0, 0)

    def move_NEGY(self):
        self.move(0, -1, 0)

    def move_POSY(self):
        self.move(0, 1, 0)

    def move_POSZ(self):
        self.move(0, 0, 1)

    def move_NEGZ(self):
        self.move(0, 0, -1)

    def location(self):
        return self.x, self.y, self.z

    def set_utility(self, location, utility):
        self.utility_table[location] = utility

    def next_local(self, move):
        return self.x + move[0], self.y + move[1], self.z + move[2]
