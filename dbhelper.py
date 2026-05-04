import mysql.connector

class dbhelper:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="dadajimoni",
                database="hit-db-demo2"
            )
            self.mycursor = self.con.cursor()

        except Exception as e:
            print("Error while connecting to database:", e)

        else:
            print("Connection successful")

    def get_cursor(self):
     try:
        self.con.ping(reconnect=True)   # ← checks connection, reconnects if dropped
     except:
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dadajimoni",
            database="hit-db-demo2"
        )
     self.mycursor = self.con.cursor()
     

    def register(self, username, email, password):
        try:
            query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
            values = (username, email, password)
            self.mycursor.execute(query, values)
            self.con.commit()
            return 1
        except Exception as e:
            print("Register error:", e)
            return -1


    def login(self, email, password):
        try:
            query = "SELECT * FROM user WHERE email = %s AND password = %s"
            self.mycursor.execute(query, (email, password))
            result = self.mycursor.fetchall()
            return result
        except Exception as e:
            print("Login error:", e)
            return []


    def view_profile(self, email):          # ✅ FIX: only email needed, removed extra username param
        try:
            query = "SELECT username, email FROM user WHERE email = %s"
            self.mycursor.execute(query, (email,))
            result = self.mycursor.fetchall()
            return result
        except Exception as e:
            print("Profile error:", e)
            return []


    def update_password(self, email, old_password, new_password):
        try:
            query = "SELECT * FROM user WHERE email = %s AND password = %s"
            self.mycursor.execute(query, (email, old_password))
            result = self.mycursor.fetchall()

            if len(result) == 0:
                return -1                   # old password wrong

            query = "UPDATE user SET password = %s WHERE email = %s"
            self.mycursor.execute(query, (new_password, email))
            self.con.commit()
            return 1

        except Exception as e:
            print("Update password error:", e)
            return -1


    def delete_account(self, email, password):
        try:
            query = "SELECT * FROM user WHERE email = %s AND password = %s"
            self.mycursor.execute(query, (email, password))
            result = self.mycursor.fetchall()

            if len(result) == 0:
                return -1                   # wrong password

            self.mycursor.execute("DELETE FROM orders WHERE email = %s", (email,))
            self.mycursor.execute("DELETE FROM user WHERE email = %s", (email,))
            self.con.commit()
            return 1

        except Exception as e:
            print("Delete error:", e)
            return -1


    def add_order(self, email, product):    # ✅ FIX: was outside class before, now inside
        try:
            query = "INSERT INTO orders (email, product) VALUES (%s, %s)"
            self.mycursor.execute(query, (email, product))
            self.con.commit()
            return 1
        except Exception as e:
            print("Order error:", e)
            return -1


    def view_orders(self, email):
     try:
        self.get_cursor()
        # ✅ fetch all 3 columns — product, status, order_date
        query = "SELECT product, status, order_date FROM orders WHERE email = %s"
        self.mycursor.execute(query, (email,))
        result = self.mycursor.fetchall()
        return result
     except Exception as e:
        print("Error:", e)
        return []
        

    def search_products(self, keyword):
     try:
        # LIKE %keyword% means: find anything containing the keyword
        query = "SELECT name, category, price, stock FROM products WHERE name LIKE %s OR category LIKE %s"
        search_term = f"%{keyword}%"        # wrapping keyword with % on both sides
        self.mycursor.execute(query, (search_term, search_term))
        result = self.mycursor.fetchall()
        return result
     except Exception as e:
        print("Search error:", e)
        return []
     
    def cancel_order(self, email, product_name):
     try:
        # First check if a pending order exists for this product
        query = """SELECT order_id FROM orders 
                   WHERE email = %s AND product = %s AND status = 'Pending'"""
        self.mycursor.execute(query, (email, product_name))
        result = self.mycursor.fetchall()

        if len(result) == 0:
            return -1       # no pending order found

        # Get the order_id and update status to Cancelled
        order_id = result[0][0]
        self.mycursor.execute(
            "UPDATE orders SET status = 'Cancelled' WHERE order_id = %s",
            (order_id,)
        )
        self.con.commit()
        return 1

     except Exception as e:
        print("Cancel error:", e)
        return -1
     

    def add_review(self, email, product, rating, comment):
     try:
        self.get_cursor()

        # check if user already reviewed this product
        self.mycursor.execute(
            "SELECT * FROM reviews WHERE email = %s AND product = %s",
            (email, product)
        )
        existing = self.mycursor.fetchall()

        if len(existing) > 0:
            return -2       # already reviewed

        self.mycursor.execute(
            "INSERT INTO reviews (email, product, rating, comment) VALUES (%s, %s, %s, %s)",
            (email, product, rating, comment)
        )
        self.con.commit()
        return 1

     except Exception as e:
        print("Review error:", e)
        return -1


    def view_reviews(self, product):
        try:
          self.get_cursor()
          self.mycursor.execute(
            "SELECT email, rating, comment, review_date FROM reviews WHERE product = %s",
            (product,)
        )
          return self.mycursor.fetchall()
        except Exception as e:
          print("Error:", e)
        return []


    def average_rating(self, product):
        try:
          self.get_cursor()
          self.mycursor.execute(
            "SELECT AVG(rating) FROM reviews WHERE product = %s",
            (product,)
        )
          result = self.mycursor.fetchone()
        # AVG returns None if no reviews exist, so we check first
          return round(result[0], 1) if result[0] else 0
        except Exception as e:
          print("Error:", e)
          return 0
        

    def get_order_history_products(self, email):
      try:
        self.get_cursor()
        self.mycursor.execute(
            "SELECT product FROM orders WHERE email = %s",
            (email,)
        )
        result = self.mycursor.fetchall()
        # result = [("laptop",), ("headphones",)] 
        # we convert it to ["laptop", "headphones"]
        return [row[0] for row in result]
      except Exception as e:
        print("Error:", e)
        return []
      
    def save_complaint(self, email, complaint, ai_response):
     try:
        self.get_cursor()
        self.mycursor.execute(
            """INSERT INTO complaints 
               (email, complaint, ai_response) 
               VALUES (%s, %s, %s)""",
            (email, complaint, ai_response)
        )
        self.con.commit()
        return 1
     except Exception as e:
        print("Error:", e)
        return -1

    def view_complaints(self, email):
     try:
        self.get_cursor()
        self.mycursor.execute(
            """SELECT complaint, ai_response, complaint_date 
               FROM complaints WHERE email = %s 
               ORDER BY complaint_date DESC""",
            (email,)
        )
        return self.mycursor.fetchall()
     except Exception as e:
        print("Error:", e)
        return []
     

    def cancel_order_by_product(self, email, product):
     try:
        self.get_cursor()
        self.mycursor.execute(
            """UPDATE orders SET status = 'Cancelled' 
               WHERE email = %s AND product = %s 
               AND status != 'Cancelled'""",
            (email, product)
        )
        self.con.commit()
        return self.mycursor.rowcount   # returns how many rows updated
     except Exception as e:
        print("Error:", e)
        return -1

    def request_replacement(self, email, product):
     try:
        self.get_cursor()
        self.mycursor.execute(
            """UPDATE orders SET status = 'Replacement Requested' 
               WHERE email = %s AND product = %s 
               AND status != 'Cancelled'""",
            (email, product)
        )
        self.con.commit()
        return self.mycursor.rowcount
     except Exception as e:
        print("Error:", e)
        return -1