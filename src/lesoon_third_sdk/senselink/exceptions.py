class SenseLinkException(Exception):

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return f'Error code: {self.errcode}, message: {self.errmsg}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.errcode}, {self.errmsg})'


class SenseLinkClientException(SenseLinkException):

    def __init__(self,
                 errcode,
                 errmsg,
                 client=None,
                 request=None,
                 response=None):
        super(SenseLinkException, self).__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response

    def __repr__(self):
        return f'{self.__class__.__name__}({self.errcode}, {self.errmsg}, {self.response.text})'
