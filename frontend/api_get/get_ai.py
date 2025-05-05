from api import get_requests, preprocess_name

def get_ai(name, surname, mode, day):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/ai/%s/%s/%s/%s" % (name, surname, mode, day)
    return get_requests(endpoint)
    
if __name__ == '__main__': 
    from datetime import date, timedelta
    import random
    day = date.today() - timedelta(days=1)
    choices = ["day", "month", "year"]
    mode = random.choice(choices)

    val = get_ai("supawitH", "Sansuk", mode, day)
    print(val)