from google import genai

# ← paste your existing key here, it'll work tomorrow
API_KEY = "AIzaSyANWktiwCz3JV3qOBUsBV8HVjSnp4TMfl4"
client = genai.Client(api_key=API_KEY)

def get_recommendations(order_history):
    # order_history is a list of products the user bought
    # example: ["laptop", "headphones", "charger"]

    if not order_history:
        return "No order history found to make recommendations."

    # we tell AI what the user bought and ask for suggestions
    prompt = f"""
    A customer has bought these products: {', '.join(order_history)}.
    Based on their purchase history, suggest 3 other products they might like.
    Keep it short, just list 3 product names with one line reason each.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI unavailable: {e}"


def smart_order_assistant():
    print("\n🤖 AI Order Assistant")
    print("I'll help you find the right product!\n")

    # AI asks questions one by one
    budget = input("What is your budget? (e.g. 5000, 10000): ")
    category = input("What type of product? (Phone/Laptop/Headphones/Charger): ")
    brand = input("Any preferred brand? (or type 'no preference'): ")

    prompt = f"""
    A customer wants to buy a product with these preferences:
    - Budget: ₹{budget}
    - Category: {category}
    - Brand preference: {brand}
    
    Suggest the best product for them from this list:
    iPhone 15 (₹79999), Samsung Galaxy (₹59999), 
    Dell Laptop (₹55000), HP Laptop (₹45000),
    Sony Headphones (₹3999), boAt Headphones (₹1499),
    iPhone Charger (₹1999).
    
    Give one recommendation with a short reason why it fits their needs.
    Also mention if their budget is too low for their category.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("\n🤖 AI Recommendation:")
        print(response.text)

        # ask if they want to place the order
        confirm = input("\nDo you want to place this order? (yes/no): ")
        return confirm.lower() == "yes"

    except Exception as e:
        print(f"AI unavailable: {e}")
        return False
    



def handle_complaint(email, complaint):
    prompt = f"""
    You are a customer support agent for Flipkart India.
    A customer with email {email} has raised this complaint:
    "{complaint}"
    
    Respond politely and professionally. 
    Acknowledge their issue, apologize, and suggest a resolution.
    Keep response under 5 lines.
    End with "Thank you for your patience!"
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "⏳ AI busy. Try again in a few minutes."
        return "❌ AI unavailable."




