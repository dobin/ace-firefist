
class AceRoute():
    def __init__(self, url: str, data: bytes):
        self.url = url
        self.data = data


class AceFile():
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
