def inventory_plan(predictions):
    avg_sales = sum(predictions) / len(predictions)

    plan = []
    for val in predictions:
        if val > avg_sales * 1.2:
            plan.append("Reorder Stock")
        elif val < avg_sales * 0.8:
            plan.append("Excess Stock")
        else:
            plan.append("Optimal Stock")

    return plan
