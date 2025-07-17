# optimization/run_optimization.py
from minizinc import Instance, Model, Solver

def run_optimization(gold, btc, eth, weeks, initial_cap=50000):
    model = Model("optimization/model.mzn")
    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, model)

    instance["weeks"] = weeks
    instance["gold_price"] = gold
    instance["bitcoin_price"] = btc
    instance["eth_price"] = eth
    instance["initial_capital"] = initial_cap

    result = instance.solve()
    return result
