#A list is declared and each element of list is a Dictionary used as a database, named bank_data
bank_data = [{"CustomerName": "Nofil", "AccountNumber":245645,"AccountType":"Savings Account","BankBalance":10000}, {"CustomerName": "Mujtaba", "AccountNumber":24555,"AccountType":"Current Account","BankBalance":1000}]
#Account_Number_value = int(input("Enter Account number: ")) #Code written to debug just complete rubbish
class Bank: #Parent Class hai yeh 
    def __init__(self,Database,Account_Number_value): #Initilization function hai yeh aur () main parameters hain 
        self.database = Database #Instance Variable hai yeh, and the value assigned is of Parameters
        self.Account_Number_value = Account_Number_value #Instance Variable hai yeh, and the value assigned is of Parameters
    def Search_All_Account_Getter(Database): #Search Function made for retriving information of all bank accounts
        for element in range(len(Database)):
            print( Database[element])
        
    def CreateAccount(Database): #takes necessary data to make account and adds into database 
        global bank_data
        CustomerName = input("Enter Customer Name: ")
        AccountNumber = int(input("Enter Account Number: "))
        AccountType = input("Enter Account type Current Account or Saving Account?: ")
        Deposit_Amount = int(input("Enter Bank Deposit amount: "))
        Updated_dict = {"CustomerName":CustomerName,"AccountNumber":AccountNumber,"AccountType":AccountType,"Deposit_Amount":Deposit_Amount}
        bank_data.append(Updated_dict)
        return f'Your Account has been added with details {Updated_dict}'            
class Customer(Bank): #This a child Class, it inherits some functionalities from, Bank class 
    def __init__(self, Database): #This is the Initiliazation function of Class Customer
        super().__init__(Database) #Yeh Inherited function hai Bank class ka 
    def BankBalanceGetter(Database,Account_Number_value): #Returns Bank Balance of the searched Account number 
        for element in Database: #Each Element is being compared with the searched Account number
            if element['AccountNumber'] == Account_Number_value:  # If the search value matches, bank balance is printed               
                return f'Your Bank  Balance is {element["BankBalance"]}'
        return None 
    def WithdrawSetter(Database,Account_Number_value): #it subtracts drawn value and returns the bank balance after 
        withdraw_value = int(input("Enter withdraw amount: ")) 
        for element in Database:
            if element['AccountNumber'] == Account_Number_value:
                updated_Database_value = element.get("BankBalance") - withdraw_value
                element.update({"BankBalance":updated_Database_value})
                return f'Your Bank Balance after withdraw is {element["BankBalance"]}'
        return None 
    #print(WithdrawSetter(Database)) #Code written for debugging purposes
    def DepositSetter(Database,Account_Number_value): # it sums the value of deposited amount into the bank balance 
        Deposit_value = int(input("Enter withdraw amount: "))
        for element in Database:
            if element['AccountNumber'] == Account_Number_value:
                updated_Database_value = element.get("BankBalance") + Deposit_value
                element.update({"BankBalance":updated_Database_value})
                return f'Your Bank Balance after deposit is {element["BankBalance"]}'
        return None 
    #print(DepositSetter(Database))    #Code written for debugging
def Options():
    print("""Enter Options: 
    1) Check Bank Balance
    2) Withdraw 
    3) Deposit
    4) Create Account
    5) Search information of all the Bank Accounts """)
    choose = int(input("Enter the Number of choice:"))
    if choose == 1:
        print(Customer.BankBalanceGetter(bank_data,Account_Number_value=int(input("Enter Account Number: "))))
    elif choose == 2:
        print(Customer.WithdrawSetter(bank_data,Account_Number_value=int(input("Enter Account Number: "))))
    elif choose == 3:
        print(Customer.DepositSetter(bank_data,Account_Number_value=int(input("Enter Account Number: "))))
    elif choose == 4:
        print(Bank.CreateAccount(bank_data))
    elif choose == 5:
        Bank.Search_All_Account_Getter(bank_data)
Options()
#print(bank_data) #code written for debugging 