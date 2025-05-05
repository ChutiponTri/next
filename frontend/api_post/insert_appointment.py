from api import post_requests, preprocess_name

def post_appointment(data):
    endpoint = "update/appointment"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

if __name__ == '__main__':
    from datetime import datetime, timedelta
    appt_date = (datetime.now() + timedelta(days=3, hours=5)).isoformat() 
    data = {    
        "name": "Supawith",
        "surname": "Sansuk",
        "date": appt_date,
        "place": "Online"
    }
    val = post_appointment(data)
    print(val)