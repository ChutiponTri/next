from api import get_requests, preprocess_name

def get_check_list(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/check/list/%s/%s" % (name, surname)
    return get_requests(endpoint)

if __name__ == '__main__':
    tasks = get_check_list("chutipon", "trirattananurak")
    print(tasks["result"])