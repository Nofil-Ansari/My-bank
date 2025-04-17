# Bank System with Object-Oriented Approach
class Bank: #Bank Class Object hai 
    def __init__(self, database): #yeh uska Initializing Function hai 
        self.database = database #self.database aik object variable hai

    def create_account(self):  #Bank Class ka method hai
        customer_name = input("Enter Customer Name: ")
        account_number = int(input("Enter Account Number: "))
        account_type = input("Enter Account type (Current Account or Saving Account): ")
        deposit_amount = int(input("Enter Bank Deposit amount: "))
        new_account = {
            "CustomerName": customer_name,
            "AccountNumber": account_number,
            "AccountType": account_type,
            "BankBalance": deposit_amount
        } #Dictionary hai jis k ander Key and value pairs main data stored hai
        self.database.append(new_account) #self.database aik list hai jis main new account variable ka data append ho raha hai
        return f'Your Account has been added with details {new_account}' #yeh aik formatted string hai

    def search_all_accounts(self): #Bank Class ka method hai
        for account in self.database: 
            print(account)

class Customer(Bank): #yeh aik diffrent Class Object hai, Bank Class iskay ander inherited hai
    def __init__(self, database): #yeh Class Customer ka Init function hai
        super().__init__(database) #yeh Bank Class ka inherited Init function hai

    def get_balance(self, account_number):  #Customer Class ka method hai
        for account in self.database:
            if account['AccountNumber'] == account_number:
                return f'Your Bank Balance is {account["BankBalance"]}'
        return "Account not found"

    def withdraw(self, account_number): #Customer Class ka method hai
        withdraw_value = int(input("Enter withdraw amount: "))
        for account in self.database:
            if account['AccountNumber'] == account_number: #Validation ho rahi hai self.database AccountNumber or account_number k beech main
                if account["BankBalance"] >= withdraw_value: #Bank Balance check ho raha hai for withdrawal
                    account["BankBalance"] -= withdraw_value #Bank Balance being updated 
                    return f'Your Bank Balance after withdraw is {account["BankBalance"]}'
                else:
                    return "Insufficient funds"
        return "Account not found"

    def deposit(self, account_number): #Customer Class ka method hai
        deposit_value = int(input("Enter Deposit amount: "))
        for account in self.database:
            if account['AccountNumber'] == account_number:
                account["BankBalance"] += deposit_value
                return f'Your Bank Balance after deposit is {account["BankBalance"]}'
        return "Account not found"

def Options(): #Global Function hai yeh 
    # Initialize the database
    bank_data = [
        {"CustomerName": "Nofil", "AccountNumber": 245645, "AccountType": "Savings Account", "BankBalance": 10000},
        {"CustomerName": "Mujtaba", "AccountNumber": 24555, "AccountType": "Current Account", "BankBalance": 1000}
    ] #Static Database hai yeh in form of Dictionary Data Structure
    
    # Create instances of Bank and Customer
    bank = Bank(bank_data) #Bank Object
    customer = Customer(bank_data)  # Customer inherits from Bank and shares the same database

    while True:
        print("""Enter Options: 
        1 Check Bank Balance
        2 Withdraw 
        3 Deposit
        4 Create Account
        5 Search information of all the Bank Accounts
        6 Exit""")
        choose = input("Enter the Number of choice: ")
        
        if choose == '1':
            account_number = int(input("Enter Account Number: "))
            print(customer.get_balance(account_number))
        elif choose == '2':
            account_number = int(input("Enter Account Number: "))
            print(customer.withdraw(account_number))
        elif choose == '3':
            account_number = int(input("Enter Account Number: "))
            print(customer.deposit(account_number))
        elif choose == '4':
            print(bank.create_account())
        elif choose == '5':
            bank.search_all_accounts()
        elif choose == '6':
            break
        else:
            print("Invalid choice")

# Run the program
if __name__ == "__main__":
    Options() #The first function to be executed in the entire code in This one