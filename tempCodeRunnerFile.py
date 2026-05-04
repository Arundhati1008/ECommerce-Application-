5}")( f"{product:<15}" )(f"{status:<12} ")(f"{date}") 


    def search_products(self):
     keyword = input("Enter product name or category to search: ")
     results = self.db.search_products(keyword)

     if not results: