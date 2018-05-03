class Trip(object):

    def make_trip(self, pickup, fare):
        trip = {}
        trip['pickup'] = pickup
        trip['fare'] = fare
        return trip
