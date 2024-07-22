class Expense:
    """Main expense class"""
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f} >"