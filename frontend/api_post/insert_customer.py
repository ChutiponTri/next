from api import post_requests, preprocess_name

def post_register(data):
    endpoint = "update/register"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

if __name__ == '__main__':
    from datetime import date
    data = {    
        "name": "Chutipon",
        "surname": "Trirattananurak",
        "gender": "Male",
        "weight": 50,
        "height": 170,
        "disease": "Heart Broken",
        "birth": date.today().isoformat()
    }
    val = post_register(data)
    print(val)