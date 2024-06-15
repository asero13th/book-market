class MyCallback:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def pack(self):
        return f"{self.name}:{self.id}"
    
    @staticmethod
    def unpack(data):
        name, id = data.split(':')
        return MyCallback(name, id)