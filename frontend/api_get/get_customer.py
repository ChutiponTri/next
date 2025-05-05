from api import get_requests, preprocess_name

def get_customer(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/customers/%s/%s" % (name, surname)
    return get_requests(endpoint)

if __name__ == '__main__':
    val = get_customer("supawitH", "Sansuk")
    print(val)