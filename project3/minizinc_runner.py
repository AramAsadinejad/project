from minizinc import Model, Solver, Instance

def run(
    capital: float,
    bonds: list,
    p_g: float,
    p_b: float,
    p_e: float,
    p_bm: float,
    p_em: float,
    c_g: float,
    c_b: float,
    c_e: float,
):
    # لود مدل
    model = Model("investment.mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)

    # پاس دادن مقادیر
    instance["capital"] = capital
    instance["bonds"] = bonds
    instance["p_g"] = p_g
    instance["p_b"] = p_b
    instance["p_e"] = p_e
    instance["p_bm"] = p_bm
    instance["p_em"] = p_em
    instance["c_g"] = c_g
    instance["c_b"] = c_b
    instance["c_e"] = c_e

    # اجرا
    result = instance.solve()

    return {
        "gold": result["gold"],
        "bit": list(result["bit"]),
        "eth": list(result["eth"]),
        "b_new": result["b_new"],
        "spent": result["spent"]
    }
