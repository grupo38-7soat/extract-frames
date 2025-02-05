from threading import Thread


class QueryResultThread(Thread):
    def __init__(self,  query_function):
        Thread.__init__(self)
        self.query_function = query_function
        self.query_result = None

    def run(self):
        self.query_result = self.query_function()
        