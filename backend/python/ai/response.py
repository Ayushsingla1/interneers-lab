from provider import model
from schema import ProductOutputSchema

def generate(prompt : str):
    try:
        response = model.with_structured_output(ProductOutputSchema).invoke(prompt)
        json_response = list(map(lambda x : x.model_dump_json(), response.products))
        return json_response
    except Exception as e:
       print(str(e))


def generate_toys():
    prompt = """Suppose you are a store manager and supposed to add toys to your database. 
                Generate data about 10 toys based on the schema given below"""
    return generate(prompt)
