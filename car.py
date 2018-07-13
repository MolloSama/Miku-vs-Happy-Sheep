
class Car():
    def __init__(self,make,model,year):
        self.make=make
        self.model=model
        self.year=year
        self.odometer_reading=0

    def get_des(self):
        lname=str(self.year)+' '+self.make+' '+self.model
        return lname.title()

    def read(self):
        print('This car has run '+str(self.odometer_reading)+" miles!")

    def update(self,mile):
        self.odometer_reading=mile

    def increment_odometer(self,miles):
        self.odometer_reading+=miles


class Battery():
    def __init__(self,battery=70):
        self.battery=battery

    def des_battery(self):
        print("This car has a "+ str(self.battery)+ " -KWh battery.")


class ElectricCar(Car):
    def __init__(self,make,model,year):
        super().__init__(make,model,year)
        self.battery=Battery()
