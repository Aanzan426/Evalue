import json
import os
from datetime import datetime

class Evalue:
    def __init__(self):
        self.filename = "Evalue.json"
        self.data_by_date = {}
        self.monthly_allotment = {}
        self.saved_section = {}
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                file_data = json.load(f)
                self.data_by_date = file_data.get("data_by_date", {})
                self.monthly_allotment = file_data.get("monthly_allotment", {})
                loaded = file_data.get("saved_section", {})
                if isinstance (loaded, dict):
                    self.saved_section = loaded
                else:
                    print("⚠️ Resetting saved_section to an empty dict (old data was not a dict)")
        self.current_date = None
        self.specific_day = None
        
    def Listing (self, date):
        if date not in self.data_by_date:
            self.data_by_date[date] = {
                'Food' : [],
                'Travel' : [],
                'Extra' : []
            }
        self.current_date = date
        self.monthly_allowance()
    
    
    def Expenses (self, current_date):
        while True:
            print("\n=== Expense Management Menu ===")
            print("1. Add Expense")
            print("2. Delete Expense")
            print("3. Display Expenses")
            print("4. Return to Main Menu")
            try:
                user_choice = int(input("\nSelect an option (1-4): "))
                if user_choice == 1:
                    self.add_expense()
                elif user_choice == 2:
                    self.delete_expense()
                elif user_choice == 3:
                    self.display_expense()
                elif user_choice == 4:
                    print("\nReturning to main menu...")
                    break
                else:
                    print("\n❌ Invalid option. Please choose a number between 1 and 4.")
            except ValueError:
                print("\n❌ Please enter a valid number.")
            
                
    def add_expense (self):
        while(True):
            print("\n=== Add Expense ===")
            print("Available categories: Food, Travel, Extra, Exit")
            user_choice_subchoice = input("Enter category to add expense to: ").strip().capitalize()
            if(user_choice_subchoice == 'Exit'):
                break
            if user_choice_subchoice in self.data_by_date[self.current_date]:
                print(f"\nAdding expenses to {user_choice_subchoice} category.")
                print("Enter 'Done' to finish.")
                while True:
                    expense_str = input(f"Enter {user_choice_subchoice} expense amount: ")
                    if expense_str.lower() == 'done':
                        print("\n✅ Expenses added successfully!")
                        break
                    else:
                        try:
                            expense = float(expense_str)
                            self.data_by_date[self.current_date][user_choice_subchoice].append(expense)
                            self.save_data()
                            print(f"Added Rs.{expense} to {user_choice_subchoice}")
                        except ValueError:
                            print("❌ Please enter a valid number or 'Done'.")
            else:
                print("\n❌ Invalid category. Please choose Food, Travel, or Extra.")
            
            
    def delete_expense (self):
        while(True):
            print("\n=== Delete Expense ===")
            print("Available categories: Food, Travel, Extra, Exit")
            user_choice_subchoice = input("Enter category to delete from: ").strip().capitalize()
            if(user_choice_subchoice == 'Exit'):
                break
            if user_choice_subchoice in self.data_by_date[self.current_date]:
                print(f"\n📋 Current '{user_choice_subchoice}' Expenses:")
                expenses = self.data_by_date[self.current_date][user_choice_subchoice]
                if not expenses:
                    print("No expenses to display.")
                for i, amt in enumerate(expenses):
                    print(f"{i}: Rs.{amt}")
                print("\nEnter 'all done' to finish.")
                while True:
                    expense_str = input("Enter index to delete: ")
                    if expense_str.lower() == 'all done':
                        print("\n✅ Deletion completed!")
                        break
                    try:
                        index = int(expense_str)
                        removed = self.data_by_date[self.current_date][user_choice_subchoice].pop(index)
                        self.save_data()
                        print(f"\n✅ Removed Rs.{removed}")
                        self.display_category(user_choice_subchoice)
                    except (IndexError, ValueError):
                        print("\n❌ Invalid index. Please enter a valid number or 'all done'.")
            else:
                print("\n❌ Invalid category. Please choose Food, Travel, or Extra.")
        
        
    def display_expense(self):
        while True:
            try:
                date_obj = datetime.strptime(self.current_date, "%d/%m/%Y")
                day_name = date_obj.strftime("%A")
            except ValueError:
                day_name = "Unknown Day"
    
            print("\n=== Display Expenses ===")
            print("1. Current Day")
            print("2. Specific Day")
            print("3. Overall Summary")
            print("4. Full Database")
            print("5. Saved Amounts")
            print("6. Exit")
            try:
                display_date = int(input("\nSelect an option (1-6): "))
                if display_date == 1:
                    print(f"\n📅 {day_name}, {self.current_date}")
                    print("-" * 50)
                    lists = self.data_by_date[self.current_date]
                    max_len = max(len(lists['Food']), len(lists['Travel']), len(lists['Extra']))
                    print(f"{'Food':<15}{'Travel':<15}{'Extra':<15}")
                    print("-" * 45)
                    for i in range(max_len):
                        f = str(lists['Food'][i]) if i < len(lists['Food']) else ""
                        t = str(lists['Travel'][i]) if i < len(lists['Travel']) else ""
                        e = str(lists['Extra'][i]) if i < len(lists['Extra']) else ""
                        print(f"{f:<15}{t:<15}{e:<15}")
                    print("-" * 45)
    
                elif display_date == 2:
                    user_date = input("\nEnter Specific Date (DD/MM/YYYY): ")
                    try:
                        date = datetime.strptime(user_date, "%d/%m/%Y")
                        day_name = date.strftime("%A")
                    except ValueError:
                        day_name = "Unknown Day"
    
                    if user_date not in self.data_by_date:
                        print("\n❌ Date not registered in the database.")
                    else:
                        print(f"\n📅 {day_name}, {user_date}")
                        print("-" * 50)
                        lists = self.data_by_date[user_date]
                        max_len = max(len(lists['Food']), len(lists['Travel']), len(lists['Extra']))
                        print(f"{'Food':<15}{'Travel':<15}{'Extra':<15}")
                        print("-" * 45)
                        for i in range(max_len):
                            f = str(lists['Food'][i]) if i < len(lists['Food']) else ""
                            t = str(lists['Travel'][i]) if i < len(lists['Travel']) else ""
                            e = str(lists['Extra'][i]) if i < len(lists['Extra']) else ""
                            print(f"{f:<15}{t:<15}{e:<15}")
                        print("-" * 45)
    
                elif display_date == 3:
                    print("\n📅 Overall Summary")
                    print("-" * 36)
                    total = {'Food': 0, 'Travel': 0, 'Extra': 0}
                    for date, cats in self.data_by_date.items():
                        for cat in total:
                            total[cat] += sum(cats[cat])
                    print(f"{'Category':<15}{'Total Spent (Rs)':<20}")
                    print("-" * 35)
                    for cat, val in total.items():
                        print(f"{cat:<15}{val:<20}")
                    print("-" * 35)
    
                elif display_date == 4:
                    self.export_data()
    
                elif display_date == 5:
                    print("\n📅 Saved Amounts")
                    print("-" * 50)
                    if not self.saved_section:
                        print("No data found. Default: Rs.600")
                    else:
                        for month_key, val in self.saved_section.items():
                            print(f"{month_key} : Rs.{val}")
                        print("-" * 50)
    
                        extra_line = input("\nAny specifics? : ")
                        if extra_line.lower() == 'sum':
                            print("-" * 50)
                            if not self.saved_section:
                                print("No data to sum. Default: Rs.0")
                            else:
                                total = sum(val for _, val in self.saved_section.items())
                                print(f"\nEvaluation : Rs.{total}")
                            print("-" * 50)
    
                elif display_date == 6:
                    print("Exiting....")
                    break
    
                else:
                    print("\n❌ Invalid option. Please choose a number between 1 and 6.")
    
            except ValueError:
                print("\n❌ Please enter a valid number.")

        
        
    def display_category (self, category):
        print(f"{category} : {self.data_by_date[self.current_date][category]}")
        
    
    def monthly_allowance (self):
        datetime_obj = datetime.strptime(self.current_date, "%d/%m/%Y")
        month_key = datetime_obj.strftime("%m/%Y")
        if datetime_obj.day == 1:
            if month_key not in self.monthly_allotment:
                print("\n=== Set Monthly Allotment ===")
                self.monthly_allotment[month_key] = {
                    'Food' : int(input("Enter Food allowance for this month: ")),
                    'Travel' : int(input("Enter Travel allowance for this month: ")),
                    'Extra' : int(input("Enter Extra allowance for this month: "))
                }
                self.save_data()
                print("\n✅ Monthly allotment set successfully!")
                
        
        elif ((datetime_obj.day == 30 and datetime_obj.month in {4, 6, 9, 11}) or (datetime_obj.day == 31 and datetime_obj.month in {1, 3, 5, 7, 8, 10, 12})):
            self.saved_amount(month_key)
    
    
    def monthly_tally (self, month_key):
        total = { 'Food' : 0, 'Travel' : 0, 'Extra' : 0}
        for date, category in self.data_by_date.items():
            try:
                day, month, year = date.split('/')
                if f"{month}/{year}" == month_key:
                    for cat in total:
                        total[cat] += sum(category[cat])
            except Exception as e:
                print(f"Skipping {date} due to error: {e}")
    
        return total
                
    
    def saved_amount (self, month_key):
        print(f"\n📆 Saved Amount of {month_key}")
        print("-" * 50)
    
        if month_key not in self.monthly_allotment:
            print("No monthly allowance set for this month.")
            return

        spent = self.monthly_tally(month_key)
        allowance = self.monthly_allotment[month_key]

        print(f"{'Category':<10} | {'Spent':<11} | {'Allowance':<12} | {'Residue'}")
        print("-" * 50)
        
        for cat in ['Food', 'Travel', 'Extra']:
            spent_amt = spent.get(cat, 0)
            allowed_amt = allowance.get(cat, 0)
            saved = allowed_amt - spent_amt
            print(f"{cat:<10} | Rs.{spent_amt:<8} | Rs.{allowed_amt:<9} | {saved}")
        
        print("-" * 50)
        self.saved_money(month_key)
    
    
    def saved_money (self, month_key = None):
        if not isinstance(self.saved_section, dict):
            print("⚠️ saved_section was corrupted—resetting it.")
            self.saved_section = {}
            
        if not month_key:
            dt = datetime.strptime(self.current_date, "%d/%m/%Y")
            month_key = dt.strftime("%m/%Y")
        else:
            dt = datetime.strptime(f"01/{month_key}", "%d/%m/%Y")
            
        spent = self.monthly_tally(month_key)
        allowance = self.monthly_allotment[month_key]
        
        basic_spent = basic_allowed = saved = 0
        tally_amount = 2500
        
          
        for cat in ['Food', 'Travel', 'Extra']:
            spent_amt = spent.get(cat, 0)
            allowed_amt = allowance.get(cat, 0)
            basic_allowed += allowed_amt
            basic_spent += spent_amt
            saved += allowed_amt - spent_amt
            
            
        
        # kitna_save_karra_1 = tally_amount - basic_spent       # Spent Column - Changing Values
        kitna_save_karra_2 = tally_amount - basic_allowed     # Allowed Column - Stable Values 
        kitna_save_karra_3 = kitna_save_karra_2 + saved
        inp = input("Month End? (Manual Overriding) : ").lower().strip()
        
        if (inp == 'yes'):
            self.saved_section[month_key] = kitna_save_karra_3
            print(f"✅ Final saved amount for {month_key}: Rs.{kitna_save_karra_3}")
            self.save_data()
        
        elif (dt.month == 2 and dt.day in {28, 29}) or \
            (dt.month in {4, 6, 9, 11} and dt.day == 30) or \
            (dt.month in {1, 3, 5, 7, 8, 10, 12} and dt.day == 31):

            # Commit to saved_section on last day
            self.saved_section[month_key] = kitna_save_karra_3
            print(f"✅ Final saved amount for {month_key}: Rs.{kitna_save_karra_3}")
            self.save_data()
            
        else:
            # Track the temporary savings (without overwriting the actual saved_section yet)
            if month_key not in self.saved_section:
                self.saved_section[month_key] = kitna_save_karra_3  # Initially, 600 is the default saved amount.
            print(f"⚠️ Temporary saved amount for {month_key}: Rs.{self.saved_section[month_key]}")
    
                    
        total_saved = sum(self.saved_section.values())
        print(f"The total amount saved so far: Rs.{total_saved}")
            
                 
    def export_data(self):
        print("\n🗃️  FULL DATA BASE \n")
        print("=" * 50)
    
        print("\n📅 All Expenses by Date:")
        for date, categories in self.data_by_date.items():
            print(f"\n🗓️ {date}")
            for cat, values in categories.items():
                print(f"  {cat}: {values}")

        print("\n📆 Monthly Allotments:")
        for month, allotments in self.monthly_allotment.items():
            print(f"\n{month}:")
            for cat, val in allotments.items():
                print(f"  {cat}: Rs.{val}")

        print("\n Saved Section:")
        print(self.saved_section)
        
        print(f"Rs.{sum(self.saved_section.values())}")
        
        print("\n You can now copy all of the above and save it externally if needed.\n")
        print("=" * 50)


    def save_data (self):
        file_data = {
            "data_by_date": self.data_by_date,
            "monthly_allotment": self.monthly_allotment,
            "saved_section" : self.saved_section
        }
        with open(self.filename, "w") as f:
            json.dump(file_data, f)
            
    
    def delete_all_data(self):
        print("\n=== Delete All Data ===")
        confirm = input("Enter confirmation code to delete all data: ").strip()
        if confirm == 'D4EEP16AANSH8_S19IAL12_@_04/02/2006':
            self.data_by_date.clear()
            self.monthly_allotment.clear()
            self.saved_section.clear()
            self.save_data()
            print("\n✅ All data has been deleted successfully.")
        else:
            print("\n❌ Deletion cancelled. Incorrect confirmation code.")


if __name__ == "__main__":
    tracker = Evalue()
    
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        section = 'Morning'
    elif 12 <= hour < 17:
        section = 'Afternoon'
    else:
        section = 'Evening'
    print(f"\n=== Welcome, Deepaansh! Good {section} ===\n")
    
    while True:
        print("\n=== Main Menu ===")
        user_date = input("Enter Date (DD/MM/YYYY), 'LogOut' : ")
        if user_date.lower() == 'logout':
            print("\n=== Logging Out ===")
            summary_choice = input("Would you like to view a monthly summary? (yes/no): ").lower()
            if summary_choice == 'yes':
                month_input = input("Enter month to view summary (MM/YYYY): ").strip()
                tracker.saved_amount(month_input)
            print("\nExiting Platform. See you soon, Deepaansh!")
            break
        
        elif user_date == 'Z26ATCH8_W23INSTON14_@_04/02/2006':
            tracker.delete_all_data()
            continue
        else:
            try:
                datetime.strptime(user_date, "%d/%m/%Y")
                tracker.Listing(user_date)
                tracker.Expenses(user_date)
            except ValueError:
                print("\n❌ Invalid date format. Please use DD/MM/YYYY.")