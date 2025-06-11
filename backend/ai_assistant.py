def get_budget_advice(income, expenses):
    if income == 0:
        return "Add some income data first."
    percent = (expenses / income) * 100
    if percent > 70:
        return "You are spending over 70% of your income. Consider reducing expenses."
    elif percent < 30:
        return "You're doing great! Less than 30% spent."
    else:
        return f"You're spending about {percent:.1f}% of your income."