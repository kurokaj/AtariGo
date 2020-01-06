import copy
class Game:

    def to_move(self,s):
        """return the player to move to the next state"""
        if s[0][1] == 1:
            return 1
        else:
            return 2

    def check_liberty(self,i, j, s, p):     
        """Checks recursively the liberties of consecutive stones of player p in state s, starting from point (i,j);
        Returns the total amount of liberties the consecutive stone row has"""
        tot = 0
        apu = 0
        s[i][j] = -(s[i][j])                # When spot is checked it turns negative

        # Below if-statements check the liberties and player p's own stones in the surrounding of (i,j)

        if (i+1) < len(s):
            if s[i+1][j] == 0:
                tot += 1
            elif s[i+1][j] == p:
                apu = self.check_liberty(i+1, j, s, p)
                if apu > 0:
                    tot += apu

        if (i-1) >= 1:
            if s[i-1][j] == 0:
                tot += 1
            elif s[i-1][j] == p:
                apu = self.check_liberty(i-1, j, s, p)
                if apu > 0:
                    tot += apu

        if (j+1) < len(s)-1:
            if s[i][j+1] == 0:
                tot += 1
            elif s[i][j+1] == p:
                apu = self.check_liberty(i, j+1, s, p)
                if apu > 0:
                    tot += apu

        if (j-1) >= 0:
            if s[i][j-1] == 0:
                tot += 1
            elif s[i][j-1] == p:
                apu = self.check_liberty(i, j-1, s, p)
                if apu > 0:
                    tot += apu
        return tot

    def terminal_test_by_player(self,s,p):	
        """Checks if there is any consecutive line of player p's stones in state s without liberty; 
        Returns 0 if there is a line without any liberty and sth else if liberties can be found in every consecutive line"""

        liberty = 0                         
        for i in range(1, len(s)):
            for j in range(len(s)-1):         
                if s[i][j] == p:
                    liberty = self.check_liberty(i, j, s, p)
                    if liberty == 0:
                        return liberty
    
        return liberty

    def terminal_test(self,s): 
        """Returns True if state is terminal and False if both players have still liberties (=not terminal)"""

        black_liberty = self.terminal_test_by_player(s, 1)
        white_liberty = self.terminal_test_by_player(s, 2)

        for l in range(1 ,len(s)):                      #Because list is immutable in Python so we need to
            for k in range(len(s)-1):                   #change it back to its original form.
                if s[l][k] < 0:                         #Immutability means that the list always points to certain spot in memory
                    s[l][k] = s[l][k] * -1

        if (black_liberty != 0) and (white_liberty != 0):   
            return False
        else:
            return True

    def utility(self,s,p):
        """Returns the payoff of state s if it is terminal, otherwise, its evaluation with respect to player p"""

        payoff = 0
        stone = 0       # Number of stones on field
        v = abs(p-2)+1  # Opponent

        # Check if board is full -> draw
        eq = 1
        for i in range(1,len(s)):
            for j in range(len(s)-1):
                if s[i][j] == 0:		
                    eq = 0
                break

        # Counts the number of the stones 
        for i in range(1,len(s)):
            for j in range(len(s)-1):
                if s[i][j] == p:
                    stone += 1

        opponent_liberty = self.terminal_test_by_player(s, v)
        player_liberty = self.terminal_test_by_player(s, p)

        for l in range(1 ,len(s)):                     	#Because list is immutable in Python, we need to
            for k in range(len(s)-1):                   #change it back to its original form (-) -> (+) every time we use this function
                if s[l][k] < 0:                         #Immutability means that the list always points to certain spot in memory
                    s[l][k] = -(s[l][k])

        #determine if draw, win / lose 

        if(opponent_liberty == 0 and player_liberty==0):    # If both have no liberty, check who placed the rock last
            if s[0][1] != p:
                payoff = 1
                return payoff
            else:
                payoff = -1
                return payoff

        elif opponent_liberty == 0:	# Player has one ore more rocks with no liberty -> player loses
            payoff = 1
            return payoff

        elif player_liberty == 0:	# Opponent has one ore more rock with no liberty -> player wins
            payoff = -1
            return payoff

        elif eq == 1:				# Draw, all the spots are filled
            payoff = 0
            return payoff

        # Not terminal state ->  determines the payoff by number of liberties in that state
    
        for i in range(1, len(s)):
            for j in range(len(s)-1):  
                if self.terminal_test_by_player(s,v) == 0:
                    payoff = 0.999
                elif s[i][j] == p:
                    payoff += self.check_liberty(i, j, s, p)
     
        for l in range(1 ,len(s)):                     #Because list is immutable in Python so we need to
            for k in range(len(s)-1):                   #change it back to its original form.
                if s[l][k] < 0:                         #Immutability means that the list always points to certain spot in memory
                    s[l][k] = s[l][k] * -1     

        payoff = payoff / (4 * stone)       # Evaluation is the number of liberties divided by the number of stones times 4
        return payoff

    def actions(self,s): 			
        """Returns the lis of valid moves at state s"""

        p = s[0][1]
        v = abs(p-2)+1              # Determines opponent
        idx = []                    # List of possible actions 

        for i in range(1,len(s)):
            for j in range(len(s)-1):
                if s[i][j] == 0:
                    s[i][j] = p
                    if self.check_liberty(i, j, s, p) != 0:
                        idx.append((p, i, j+1));

                    elif self.terminal_test_by_player(s, v) == 0:
                        idx.append((p, i, j+1))

                    for l in range(1 ,len(s)):                      #Because list is immutable in Python, we need to
                        for k in range(len(s)-1):                   #change it back to its original form (-) -> (+) every time we use this function
                            if s[l][k] < 0:                         #Immutability means that the list always points to certain spot in memory
                                s[l][k] = s[l][k] * -1

                    s[i][j] = 0
        return idx

    def result(self,s,a):			
        """ Returns the successor game state after playing move a at state s"""

        pos_x = a[1]
        pos_y = a[2]
        h = copy.deepcopy(s)

        h[pos_x][pos_y-1] = a[0]        # Inserts the action to the copied state
        h[0][1] = abs(h[0][1]-2)+1      # Gives the next turn for the opponent
        return h

    def load_board(self,file):
        """ Loads a board from a file object f and returns the corresponding state"""

        board = []

        for line in file:
            board.append(line.strip())

        state = board.copy()

        for i in range(len(board)):
            state[i] =[state[i]]
            row = []
            for j in range(len(board[i])):
                if board[i][j] == " ":
                    pass
                else:
                    row.append(board[i][j])
                    state[i] = row

        for i in range(len(board)):
            state[i] = [int(j) for j in state[i]]

        return state

