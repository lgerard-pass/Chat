class Channel(object):

    def __init__(self, name):
        self.name = name
        self.clients = set()