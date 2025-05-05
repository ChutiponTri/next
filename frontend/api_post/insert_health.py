from api import post_requests, preprocess_name

def post_health(data):
    endpoint = "update/health"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

if __name__ == '__main__':
    data = {    
        "name": "Supawith",
        "surname": "Sansuk",
        "evaluate_score": 2.0,
        "descr": "ไปหาหมอซะนะ"
    }
    val = post_health(data)
    print(val)