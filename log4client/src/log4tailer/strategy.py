class TailOneLineMethod(object):
    def __init__(self):
        self.read_method = "readLine"
    
    def get_trace(self, log):
        return getattr(log, self.read_method)()


class TailMultiLineMethod(object):

    def __init__(self):
        self.read_method = "readLines"

    def get_trace(self, log):
        return getattr(log, self.read_method)()
        

class TailContext(object):

    def __init__(self, throttle_time, default_tail_method=TailMultiLineMethod):
        self.tail_method = default_tail_method()
        self.throttle_time = throttle_time

    def change_tail_method(self, tail_method):
        self.tail_method = tail_method

    def get_trace(self, log):
        return self.tail_method.get_trace(log)
