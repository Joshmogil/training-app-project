import requests

def go_test():
    r = requests.get('http://127.0.0.1:10000/').content
    print(r)