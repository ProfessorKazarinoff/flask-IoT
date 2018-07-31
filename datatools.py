# datatools.py

class DataPoint:
    def __init__(self, API_key='', date_time='', channel='', field='', data=None):
        self.API_key = API_key
        self.date_time = date_time
        self.channel= channel
        self.field = field
        self.data = data

    def data_point_dict(self):
        return {'API_key':self.API_key,
                'date_time':self.date_time,
                'channel':int(self.channel),
                'field':int(self.field),
                'data':float(self.data),}
    
    def __repr__(self):
        return f"Data Point: {self.data} Date: {self.date_time} Field: {self.field} Channel: {self.channel}"

def generate_API_key(N=8):
    """
    generates a random string N characters long
    made up of uppercase ASCII characters (letters and numbers)

    example:

        >>> generate_API_key(8)

        'AP9UB73A'

    :param N: int, length of random API key
    :return: str, random string of uppercase ASCII characters ex: 'NP9TRG54'
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))