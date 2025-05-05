from api import post_requests, preprocess_name

def post_feedback(data):
    endpoint = "update/feedback"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

if __name__ == '__main__':
    data = {    
        "name": "Supawith",
        "surname": "Sansuk",
        "doctor_name": "Thitikarn",
        "doctor_surname": "Jungteerapanich",
        "descr": "สุขภาพแข็งแรงดีจุ้บุ้"
    }
    val = post_feedback(data)
    print(val)