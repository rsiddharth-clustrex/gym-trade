import gym

class TradeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        
        self.game = None
        self.state = None
        self.reward = 0.0
        self.done = False
        self.buy = 0.0
        self.sell = 0.0
        self.state_gen = None
        self.long = False
        self.info = ''
        self.short = False
        self.max_neg_reward = 0.0

    def gen_next_state(self):
        """ function to generate next state """
        
        for _, row in self.game.iterrows():
                yield(row)
        
    def step(self, action):
        """ function to get reward and next state given an action """
        
        if action == 0:
            # buy call
            if self.long == True:
                # already on long
                
                # self.info = 'Can\'t buy. Already on long.'
                self.reward = self.max_neg_reward
            
            elif self.short == True:
                # exiting short
                
                self.info = 'Exiting Short at ' + str(self.state['close'])
                
                discount = self.state['close'] * 0.0009
                profit = self.sell - (self.state['close'] + discount)
                brokerage = profit * 0.01 if profit * 0.01 <= 20 else 20
                
                self.reward = profit - brokerage
                self.short = False
                self.sell = 0
                
            else:
                # entering short
                
                self.info = 'Entering Long at ' + str(self.state['close'])
                self.buy = self.state['close']
                self.long = True
            
            try:
                self.state = next(self.state_gen)
            except StopIteration:
                self.done = True
                    
        
        elif action == 1:
            """ sell call """
            
            if self.short == True:
                # already on short
                
                # self.info = 'Can\'t sell. Already on short.'
                self.reward = self.max_neg_reward
            
            elif self.long == True:
                # exiting long
                
                self.info = 'Exiting Long at ' + str(self.state['close'])
                
                discount = self.buy * 0.0009
                profit = self.state['close'] - (self.buy + discount)
                brokerage = profit * 0.01 if profit * 0.01 <= 20 else 20
                
                self.reward = profit - brokerage
                self.buy = 0
                self.long = False
            
            else:
                # entering short
                
                self.info = 'Entering Short at ' + str(self.state['close'])
                self.sell = self.state['close']
                self.short = True
            
            try:
                self.state = next(self.state_gen)
            except StopIteration:
                self.done = True
                
            
        else:
            """ skipping trade """
            
            if self.long == True:
                # holding long
                
                self.reward = 0
                # self.info = 'Holding Long, reward: ' + str(self.reward)
            
            elif self.short == True:
                # holding short
                
                self.reward = 0
                # self.info = 'Holding Short, reward: ' + str(self.reward)
                
            else:
                # skipping trade
                
                self.reward = 0
                # self.info = 'Skipping trade'
            
            try:
                self.state = next(self.state_gen)
            except StopIteration:
                self.done = True
        
        if self.done == True:
            # game over
            
            if self.long == True:
                # exiting long
                
                self.info = 'Exiting Long at ' + str(self.state['close'])
                
                discount = self.buy * 0.0009
                profit = self.state['close'] - (self.buy + discount)
                brokerage = profit * 0.01 if profit * 0.01 <= 20 else 20
                
                self.reward = profit - brokerage
                self.buy = 0
                self.long = False
                
            elif self.short == True:
                # exiting short
                
                self.info = 'Exiting Short at ' + str(self.state['close'])
                
                discount = self.state['close'] * 0.0009
                profit = self.sell - (self.state['close'] + discount)
                brokerage = profit * 0.01 if profit * 0.01 <= 20 else 20
                
                self.reward = profit - brokerage
                self.short = False
                self.sell = 0
            
            else:
                # skipping
                self.reward = self.max_neg_reward
                
        return self.state, self.reward, self.done, self.info
        

    def reset(self, game):
        
        self.game = game
        self.reward = 0.0
        self.done = False
        self.buy = 0.0
        self.sell = 0.0
        self.state_gen = self.gen_next_state()
        self.long = False
        self.short = False
        self.state = next(self.state_gen)
        
        return self.state
        
        
    def render(self, mode='human', close=False):
        pass