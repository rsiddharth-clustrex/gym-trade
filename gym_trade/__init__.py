# init

from gym.envs.registration import register

register(
    id='trade-v0',
    entry_point='gym_trade.envs:TradeEnv',
)