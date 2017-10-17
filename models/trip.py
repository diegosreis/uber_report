class Trip(object):
    pickup = ""   
    fare = ""

    def __init__(self, pickup, fare):    
        self.pickup = pickup    
        self.fare = fare

    def make_trip(pickup, fare):
        trip = Trip(pickup, fare)
        return trip