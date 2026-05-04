from datetime import date
from typing import Self

from streamlit import status

from ai_helper import get_recommendations, handle_complaint, smart_order_assistant
from dbhelper import dbhelper

class flipkart:
    def __init__(self):
        self.db = dbhelper()
        self.current_user_email = None      # ✅ initialize these here so they always exist
        self.current_user_name = None
        self.menu()


    def menu(self):
        user_input = input("""
           1. Enter 1 to Register
           2. Enter 2 to Login
           3. Enter 3 to Exit
           Enter choice: """)

        if user_input == "1":
            self.register()
        elif user_input == "2":
            self.login()
        elif user_input == "3":
            exit()
        else:
            print("Invalid input")
            self.menu()


    def login_menu(self):
        print(f"\nWelcome, {self.current_user_name}!")
        
        while True:          # ← keep looping until user logs out or deletes account
            choice = input("""
        1. View Profile
        2. Update Password
        3. Search Products
        4. Place Order
        5. View My Orders
        6. Cancel an Order
        7. Add a Review
        8. View Reviews for a Product
        9. Get AI Recommendations
        10. Smart AI Order Assistant
        11. AI Customer Support
        12. Delete Account
        13. Logout
        Enter choice: """)

            if choice == "1":
                self.view_profile()
            elif choice == "2":
                self.update_password() 
            elif choice == "3":
                self.search_products()
            elif choice == "4":
                self.place_order()
            elif choice == "5":
                self.view_orders()
            elif choice == "6":
                self.cancel_order()

            elif choice == "7":
                self.add_review()
            elif choice == "8":
                self.view_reviews()
            elif choice == "9":
                self.ai_recommendations()
            elif choice == "10":
                self.ai_smart_order()
            elif choice == "11":
                self.ai_complaint()
            elif choice == "12":
                self.delete_account()
                break        # ← exit loop after delete
            elif choice == "13":
                print("Logged out successfully!")
                break        # ← exit loop after logout
            else:
                print("Invalid choice.")
        
        self.menu()          # ← only runs once, after loop ends                 # ✅ stay in login menu after every action except logout/delete


    def register(self):
        username = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        response = self.db.register(username, email, password)
        if response == 1:
            print("Registration successful!")
        else:
            print("Registration failed. Email may already exist.")
        self.menu()


    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        response = self.db.login(email, password)

        if len(response) == 0:
            print("Incorrect email/password.")
            self.login()
        else:
            self.current_user_name = response[0][1]     # column 1 = username
            self.current_user_email = email
            self.login_menu()


    def view_profile(self):
        data = self.db.view_profile(self.current_user_email)   # ✅ FIX: pass email only
        if data:
            print("\n---- Profile Details ----")
            print("Username:", data[0][0])
            print("Email   :", data[0][1])
        else:
            print("Error fetching profile details.")


    def update_password(self):
        old_pass = input("Enter current password: ")
        new_pass = input("Enter new password: ")
        confirm = input("Confirm new password: ")

        if new_pass != confirm:             # ✅ FIX: indentation was wrong before
            print("Passwords do not match!")
            return

        response = self.db.update_password(self.current_user_email, old_pass, new_pass)
        if response == 1:
            print("Password updated successfully!")
        else:
            print("Old password is incorrect.")


    def delete_account(self):
        print("⚠ This will permanently delete your account!")
        confirm = input("Type YES to confirm: ")

        if confirm != "YES":                # ✅ FIX: indentation was wrong before
            print("Cancelled.")
            

        password = input("Enter your password to confirm: ")
        response = self.db.delete_account(self.current_user_email, password)

        if response == 1:
            print("Account deleted. Goodbye!")
            self.menu()
        else:
            print("Incorrect password. Account not deleted.")


    def place_order(self):
        print("\n-- Available Products --")
        print("1. Phone")                   # ✅ FIX: indentation was wrong before
        print("2. Laptop")
        print("3. Headphones")
        print("4. Charger")
        product = input("Enter product name: ")

        response = self.db.add_order(self.current_user_email, product)
        if response == 1:
            print(f"Order placed for '{product}' successfully!")
        else:
            print("Failed to place order.")


    def view_orders(self):
     orders = self.db.view_orders(self.current_user_email)
     if not orders:
        print("No orders found.")
     else:
        print("\n-- Your Orders --")
        print(f"{'No.':<5} {'Product':<15} {'Status':<12} {'Date'}")
        print("-" * 50)
        for i, order in enumerate(orders, 1):
            product = order[0]    # ← SELECT product
            status  = order[1]    # ← SELECT status  
            date    = order[2]    # ← SELECT order_date
            print(f"{i:<5} {product:<15} {status:<12} {date}")


    def search_products(self):
     keyword = input("Enter product name or category to search: ")
     results = self.db.search_products(keyword)

     if not results:
        print("No products found.")
     else:
        print(f"\n{'Product':<20} {'Category':<15} {'Price':<10} {'Stock'}")
        print("-" * 55)
        for row in results:
            # row[0]=name, row[1]=category, row[2]=price, row[3]=stock
            print(f"{row[0]:<20} {row[1]:<15} ₹{row[2]:<9} {row[3]}")

    def cancel_order(self):
        self.view_orders()

        product_name = input("\nEnter product name to cancel: ")
        confirm = input(f"Are you sure you want to cancel '{product_name}'? (YES/no): ")

        if confirm != "YES":
            print("Cancellation aborted.")
            return

        response = self.db.cancel_order(self.current_user_email, product_name)
        if response == 1:
            print(f"Order for '{product_name}' cancelled successfully.")  # ← 12 spaces
        else:                                                              # ← 8 spaces
            print("No pending order found for that product.")             # ← 12 spaces3



    def add_review(self):
        self.view_orders()          # show orders so user knows what to review
        product = input("\nEnter product name to review: ")

        while True:
            try:
                 rating = int(input("Enter rating (1-5): "))
                 if 1 <= rating <= 5:
                  break
                 else:
                      print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid! Enter a number only.")

        comment = input("Enter your comment: ")

        response = self.db.add_review(self.current_user_email, product, rating, comment)
        if response == 1:
         print("✅ Review added successfully!")
        elif response == -2:
          print("You already reviewed this product.")
        else:
          print("Failed to add review.")


    def view_reviews(self):
        product = input("Enter product name to see reviews: ")

        # show average rating first
        avg = self.db.average_rating(product)
        print(f"\n⭐ Average Rating for '{product}': {avg}/5")

        reviews = self.db.view_reviews(product)
        if not reviews:
            print("No reviews yet for this product.")
        else:
            print(f"\n{'Email':<25} {'Rating':<8} {'Comment':<25} {'Date'}")
            print("-" * 70)
            for r in reviews:
                stars = "⭐" * r[1]          # r[1] = rating number → show as stars
                print(f"{r[0]:<25} {stars:<8} {r[2]:<25} {r[3]}")

    def ai_recommendations(self):
        from ai_helper import get_recommendations

        print("\n🤖 Getting AI recommendations for you...")
        # fetch user's order history from DB
        order_history = self.db.get_order_history_products(self.current_user_email)

        recommendations = get_recommendations(order_history)
        print("\n✨ AI Recommends:")
        print(recommendations)

    def ai_smart_order(self):
        from ai_helper import smart_order_assistant

        wants_to_order = smart_order_assistant()

        if wants_to_order:
            product = input("Enter the product name to order: ")
            response = self.db.add_order(self.current_user_email, product)
            if response == 1:
                print(f"✅ Order placed for '{product}'!")
            else:
                print("Failed to place order.")
        else:
            print("No order placed.")

    def ai_complaint(self):
        from ai_helper import handle_complaint

        print("\n📝 AI Customer Support")
        print("Type your complaint and our AI will respond!\n")

        complaint = input("Describe your issue: ")

        print("\n🤖 AI Support is responding...")
        ai_response = handle_complaint(self.current_user_email, complaint)

        print("\n💬 Support Response:")
        print(ai_response)

        # save complaint to DB
        self.db.save_complaint(
            self.current_user_email,
            complaint,
            ai_response
        )
        print("\n✅ Your complaint has been recorded.")

        # ── Action Section ──────────────────────────────
        print("\nWhat action would you like to take?")
        print("1. Cancel order & refund")
        print("2. Request replacement")
        print("3. No action needed")
        action = input("Enter choice: ")

        if action == "1" or action == "2":
            # show their orders first so they know product name
            self.view_orders()
            product = input("\nEnter product name from your orders: ")

            if action == "1":
                result = self.db.cancel_order_by_product(
                    self.current_user_email, product
                )
                if result > 0:      # rowcount > 0 means update worked
                    print(f"✅ Order for '{product}' cancelled.")
                    print("💰 Refund will be processed in 5-7 business days.")
                else:
                    print("❌ No active order found for that product.")

            elif action == "2":
                result = self.db.request_replacement(
                    self.current_user_email, product
                )
                if result > 0:
                    print(f"✅ Replacement requested for '{product}'.")
                    print("📦 Our team will contact you within 24 hours.")
                else:
                    print("❌ No active order found for that product.")

        elif action == "3":
            print("No action taken. We hope your issue gets resolved!")
        else:
            print("Invalid choice. No action taken.")

    def view_my_complaints(self):
        complaints = self.db.view_complaints(self.current_user_email)
        if not complaints:
            print("No complaints raised yet.")
        else:
            print("\n-- Your Complaints --")
            for i, c in enumerate(complaints, 1):
                print(f"\n{i}. Complaint : {c[0]}")
                print(f"   AI Response: {c[1]}")
                print(f"   Date       : {c[2]}")


obj = flipkart()