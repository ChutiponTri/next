from api import post_requests, preprocess_name

def post_ai(data):
    endpoint = "update/ai"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

if __name__ == '__main__':
    data = {    
        "name": "supawith",
        "surname": "sansuk",
        "bedsore_grade": "grade 3-5",
        "suggestion": "Ok",
        "hospital": "No need",
        "wound_type": "Wet Dressing"
    }
    val = post_ai(data)
    print(val)