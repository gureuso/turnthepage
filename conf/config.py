import os
import json


class JsonConfig:
    DATA = json.loads(open('{}/config.json'.format(os.path.dirname(os.path.abspath(__file__)))).read())

    @staticmethod
    def get_data(varname, value=None):
        return JsonConfig.DATA.get(varname) or os.getenv(varname) or value
