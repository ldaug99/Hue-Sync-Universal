

def method(**kwargs):
    print(kwargs)

def method2(**kwargs):
    method(**kwargs)

keywords = {"key1": "test1", "key2": "test2"}

method2(**keywords)