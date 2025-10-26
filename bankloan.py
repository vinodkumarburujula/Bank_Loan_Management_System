import os
from datetime import datetime
import json

file="loan.json"

min_salary=20000


def load_data():
    if not os.path.exists(file):
        return []
    with open(file,"r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def safe_date_input(msg):
    while True:
        date_str=input(msg)
    
        try:
            datetime.strptime(date_str,"%d-%m-%Y")
            return date_str
        except ValueError:
            print("❌ Invalid date. Please Provide a valid Date \n")
    
def next_due(start_date):
    d=datetime.strptime(start_date,"%d-%m-%Y")
    
    if d.month == 12:
        nxt=d.replace(year=d.year+1, month=1)
    else:
        nxt=d.replace(month=d.month+1)
    return nxt.strftime("%d-%m-%Y")

def genegrate_id(data):
    if not data:
        return 1001
    max_id=max(loan['loan_id'] for loan in data)
    return max_id + 1
        
def save_data(data):
    with open(file,'w') as f:
        json.dump(data,f, indent=4)

def find_loan(data,loan_id):
    for loan in data:
        if loan['loan_id'] == loan_id:
            return loan
    return None

def pay_emi(data):
    
    try:
        loan_id=int(input("Enter your loan id: "))
    except ValueError:
        print("❌ Invalid loan id. \n")
        return
    loan=find_loan(data,loan_id)
    
    if not loan:
        print("❌ Loan not Found! \n")
        return
    if loan['status']=='Cleared':
        print("🙌 Loan Already Cleared\n")
        return
    print(f'Next Emi Due: {loan['next_due']}')
    
    try:
        amt=int(input(f'Enter Emi ({loan['emi']}): '))
    except ValueError:
        print("❌ Invalid Amount.\n")
        return
    if amt != loan['emi']:
        print(f'❌ Wrong Emi Amount, Expected ({loan['emi']}), got {amt}')
        return
    
    loan['balance'] -= amt
    loan['tenure'] -=1
    loan['history'].append({"date": loan['next_due'], "amount": amt})
    loan['next_due']=next_due(loan["next_due"])
    
    if loan['balance'] <= 0:
        loan['balance']=0
        loan['tenure']=0
        loan['status']="cleared"
        print("✅ Loan Cleared Sucessfull, Thank you & Visit Again")
    else:
        print(f'✅ EMI Paid sucessfull, \nBalance Left: {loan['balance']}\nRemaining Tenure: {loan['tenure']} months \n')
    save_data(data)

def apply_loan(data):
    name=input("Enter your name: ")
    
    try:
        salary=int(input("Enter your monthly Salary: "))
    except ValueError:
        print("❌ Please enter valid salary")
        return
    
    if salary <= min_salary:
        print(f"Salary must be {min_salary} to get a loan")
        return
    
    loan_amount=salary * 5
    emi_amount=salary * 0.10
    tenure= loan_amount // emi_amount
    
    print(f"✅ congrats {name} your elgible to get a Loan")
    print(f"loan amount: {loan_amount}")
    print(f"EMI: {emi_amount}")
    print(f"Tenure: {tenure}")
    
    confirm= input("Do You Want To continue (Yes/No): ").lower()
    
    if confirm != "yes":
        print("⛔loan Cancelled and thank you visit again ! \n")
    
    start_date=safe_date_input("Enter Loan Start Date(dd-mm-yyy): ")
    
    first_due= next_due(start_date)
    
    loan_id=genegrate_id(data)
    
    record={
        "loan_id":loan_id ,
        "name": name,
        "salary":salary ,
        "loan_amount":loan_amount ,
        "emi": emi_amount,
        "tenure": tenure,
        "balance":loan_amount ,
        "status":"Ongoing",
        "next_due": first_due,
        "history":[]
    }
    
    data.append(record)
    save_data(data)
    print(f'\n🏦 Loan Approved sucessful. your Loan Id is: {loan_id} \n========================================\n========================================')

def clear_loan(data):
    
    try:
        loan_id=int(input("Enter your Loan id: "))
    except ValueError:
        print("❌ Invalid Loan Id.\n")
        return
    loan=find_loan(data,loan_id)
    
    if not loan:
        print("Loan not Found! \n")
        return 
    if loan['status'] == "Cleared":
        print("✅ Loan Already Cleared\n")
        return
    print(f"Balance Left : {loan['balance']} \nTotal EMI's Remaining: {loan['tenure']}")
    
    try:
        amt=int(input("Enter amount to clear (full/partial- divisible by 2 ): "))
    except ValueError:
        print("❌ Invalid amount\n")
        return
    
    if amt == loan['balance']:
        pay_date= safe_date_input("Enter payment Date(dd-mm-yyyy): ")
        loan['history'].append({'date':pay_date,"amount":amt})
        loan['balance']=0
        loan['status']="Cleared"
        loan['tenure']=0
        print("✅ Loan Cleared sucessfully thank you & visit again! \n")
    elif amt <loan['balance'] and amt % loan['emi']==0:
        months_reduced=amt // loan['emi']
        pay_date=safe_date_input("Enter Payment date (dd-mm-yyyy): ")
        loan['history'].append({'date':pay_date,"amount":amt})
        loan['balance'] -= amt
        loan['tenure'] -= months_reduced
        print(f"✅ partial Clearence Done. paid {amt}")
        print(f'Remaining Balance: {loan['balance']}, New Tenure: {loan['tenure']}')
    else:
        print("❌ Invalid amount. Must Match balance (full) or be multiple of EMI(partial)")
        return
    save_data(data)

def view_history(data):
    
    try:
        loan_id=int(input("Enter your loan id: "))
    except ValueError:
        print("❌ Invalid Loan id. please enter valid loan id")
        return
    loan=find_loan(data,loan_id)
    
    if not loan:
        print("⛔ Loan not found.\n")
        return
    print(f'\n✅ Payment History for loan id {loan['loan_id']} -- {loan['name']}')
    
    for p in loan['history']:
        print(f'Date{p['date']} - Amount{p['amount']}')
    print(f'\nBalance Remaining: {loan['balance']}')
    print(f'Status: {loan['status']}')
    
    if loan['status']=='Ongoing':
        print(f'Next EMI Due: {loan["next_due"]} \n Remaining Tenure{loan['tenure']}')
        
        

def main():
    data=load_data()

    while True:
        print("\n======= 🏦 Bank Loan Management System ==========")
        print("1. Apply for Loan")
        print("2. Pay EMI")
        print("3. Clear Loan")
        print("4. View Payment History")
        print("5. Exit")
        
        choice=int(input("\nEnter Your Choice: "))
        
        if (choice == 1):
            apply_loan(data)
        elif (choice == 2):
            pay_emi(data)
        elif (choice == 3):
            clear_loan(data)
        elif (choice ==4):
            view_history(data)
        elif(choice == 5):
            print("🤝 Thank You Visit Again")
            break
        else:
            print("⏺️ Invalid choice Please Enter Valid Choice ")
            
main()