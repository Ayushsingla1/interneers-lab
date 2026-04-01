from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv

dotenv.load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# response = model.invoke("Generate 5 product names for a toy store")

# pprint(response)

# model2 = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 1.5)

# response2 = model2.invoke("Generate 5 product names for a toy store")

# pprint(response2.usage_metadata['total_tokens'])
