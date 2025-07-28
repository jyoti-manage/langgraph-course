# example

class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self):
        import time

        time.sleep(1)
        print(f"Adding {self._value} to {[]}")
        return {"aggregate": [self._value]}

a = ReturnNodeValue("I'm A")
print(a())

