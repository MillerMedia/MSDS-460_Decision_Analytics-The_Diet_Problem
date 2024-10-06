import pulp

def solve_diet_problem(
    foods,           # Dictionary of foods with their costs per unit
    nutrients,       # List of nutrients to consider
    food_nutrients,  # Dictionary of nutrient content per unit of food
    min_nutrients,   # Dictionary of minimum daily requirements for each nutrient
    max_nutrients    # Dictionary of maximum daily allowances for each nutrient
):
    # Create the optimization problem
    prob = pulp.LpProblem("Diet_Optimization", pulp.LpMinimize)
    
    # Decision variables: how much of each food to buy
    food_vars = pulp.LpVariable.dicts("Food", foods.keys(), lowBound=0)
    
    # Objective function: minimize cost
    prob += pulp.lpSum([foods[f] * food_vars[f] for f in foods])
    
    # Constraints for minimum nutrient requirements
    for nutrient in nutrients:
        prob += pulp.lpSum([food_nutrients[f][nutrient] * food_vars[f] for f in foods]) >= min_nutrients[nutrient], f"Min_{nutrient}"
    
    # Constraints for maximum nutrient allowances
    for nutrient in nutrients:
        if nutrient in max_nutrients:
            prob += pulp.lpSum([food_nutrients[f][nutrient] * food_vars[f] for f in foods]) <= max_nutrients[nutrient], f"Max_{nutrient}"
    
    # Solve the problem
    prob.solve()
    
    # Prepare the results
    results = {
        'status': pulp.LpStatus[prob.status],
        'optimal_cost': pulp.value(prob.objective),
        'food_amounts': {f: pulp.value(food_vars[f]) for f in foods},
        'nutrients_obtained': {
            n: sum(food_nutrients[f][n] * pulp.value(food_vars[f]) for f in foods)
            for n in nutrients
        }
    }
    
    return results

# Example usage
if __name__ == "__main__":
    # Sample data
    foods = {
        'chicken': 2.89,    # price per unit
        'beef': 3.84,
        'fish': 2.63,
        'eggs': 1.45,
        'beans': 0.95
    }
    
    nutrients = ['protein', 'fat', 'carbs']
    
    food_nutrients = {
        'chicken': {'protein': 27, 'fat': 14, 'carbs': 0},
        'beef': {'protein': 26, 'fat': 19, 'carbs': 0},
        'fish': {'protein': 22, 'fat': 12, 'carbs': 0},
        'eggs': {'protein': 13, 'fat': 10, 'carbs': 1},
        'beans': {'protein': 15, 'fat': 1, 'carbs': 40}
    }
    
    min_nutrients = {
        'protein': 70,  # minimum daily requirement
        'fat': 20,
        'carbs': 50
    }
    
    max_nutrients = {
        'fat': 70   # maximum daily allowance
    }
    
    # Solve the problem
    solution = solve_diet_problem(foods, nutrients, food_nutrients, min_nutrients, max_nutrients)
    
    # Print results
    print(f"Status: {solution['status']}")
    print(f"Optimal daily cost: ${solution['optimal_cost']:.2f}")
    print("\nOptimal food amounts:")
    for food, amount in solution['food_amounts'].items():
        if amount > 0:
            print(f"{food}: {amount:.2f} units")
    
    print("\nNutrients obtained:")
    for nutrient, amount in solution['nutrients_obtained'].items():
        print(f"{nutrient}: {amount:.2f} units")
