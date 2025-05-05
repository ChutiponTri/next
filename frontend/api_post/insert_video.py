from api import post_requests, preprocess_name

def post_video(data):
    endpoint = "update/video"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

if __name__ == '__main__':
    data = {    
        "name": "Supawith",
        "surname": "Sansuk",
        "video": "ระหว่างมะพร้าวกับส้มโอ อันไหนหวานกว่ากัน"
    }
    val = post_video(data)
    print(val)