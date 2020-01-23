
import requests,json

class Sender(object):
    """
    An http class to implement the sending of requests
    """

    def sendjson(self,endpoint):
        """
        Send json HTTP request

        :param endpoint:

        :param data: Json

        :return:
        """
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}  # create content type header for post request

        response = requests.post(endpoint, headers=headers)

        return response
