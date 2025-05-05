from api import get_requests, preprocess_name

def get_appointment(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/appointment/%s/%s" % (name, surname)
    return get_requests(endpoint)

if __name__ == '__main__':
    from datetime import date, timedelta
    import random

    day = date.today() - timedelta(days=1)
    choices = ["day", "month", "year"]
    mode = random.choice(choices)
    val = get_appointment("supawitH", "Sansuk")
    print(val)