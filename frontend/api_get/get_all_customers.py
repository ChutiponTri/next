from api import get_requests, preprocess_name

def get_all_customers():
    endpoint = "retrieve/customers"
    return get_requests(endpoint)

if __name__ == '__main__':
    val = get_all_customers()
    print(val)