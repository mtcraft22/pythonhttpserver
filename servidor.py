from httpclass import *

class api(httpmessage):
    def __init__(self):
        super().__init__()

Api=api()
Api.run_forever()