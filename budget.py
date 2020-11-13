import itertools


class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = []

    def __repr__(self):
        out = "{:*^30}\n".format(self.category_name)
        for el in self.ledger:
            out += "{d:23}{a:7.2f}\n".format(d=el["description"][:23], a=el["amount"])
        out += "Total: {t:.2f}".format(t=self.get_balance())
        return out

    def get_balance(self):
        return sum(el["amount"] for el in self.ledger)

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def transfer(self, amount, destination):
        if self.withdraw(amount, f"Transfer to {destination.category_name}"):
            destination.deposit(amount, f"Transfer from {self.category_name}")
            return True
        return False



def create_spend_chart(categories):
    out = "Percentage spent by category\n"
    cat_withdraw = lambda ledger: sum(el["amount"] for el in ledger if el["amount"] < 0)
    expense_dic = {category.category_name: cat_withdraw(category.ledger) for category in categories}
    tot_spent = sum(expense_dic.values())
    expense_dic_perc = {key: (100 * value / tot_spent) for key, value in expense_dic.items()}
    for level in range(100, -1, -10):
        out += "{l:3.0f}|".format(l=level)
        for value in expense_dic_perc.values():
            if value > level:
                out += ' o '
            else:
                out += '   '
        out += ' \n'
    out += '    -' + '---' * len(expense_dic_perc) + '\n'
    for x in range(max(len(w) for w in expense_dic_perc.keys())):
        out += '    '
        for key in expense_dic_perc.keys():
            if len(key) > x:
                out += f' {key[x]} '
            else:
                out += '   '
        out += ' \n'
    return out[:-1]
