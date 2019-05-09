class FakePopen(object):
    def __init__(self, args, stdout=None):
        super().__init__()
        self.args = args
        self.stdout = stdout

    def communicate(self, input=None, timeout=None):
        return "foo", "bar"
