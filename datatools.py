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
