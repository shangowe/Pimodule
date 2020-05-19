class GPIO:

    BCM = ''
    OUT = ''
    HIGH=''
    LOW=''
    IN=''
    def setmode(self):
        pass

    def setup(self,pin):
        pass

    def output(self,pin):
        pass

    def input(pin):
        """
        Should return a false for all non raspberry pi pins
        :return: False
        """
        return False
