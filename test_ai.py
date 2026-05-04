from google import genai

client = genai.Client(api_key="AIzaSyANWktiwCz3JV3qOBUsBV8HVjSnp4TMfl4")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say hello!"
)

print(response.text)