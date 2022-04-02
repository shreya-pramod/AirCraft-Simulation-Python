"""
file: airit_simulation.py
description: This program is a simulation program for the airport. Here there are various classes which ensure the proper
simulation.The gate and the aircraft have the maximum capacities that cannot be crossed while filling the space.
language: python3
author: Shreya Pramod, sp3045@rit.edu

"""

import sys

class Passenger:
    """

    Passenger class defines the passengers in the aircraft simulation
    The passengers have a ticket number which helps in segregating them
    and the presence of a carry on bag or no is also a part of this.

    """
    __slots__ = "name", "ticketnumber", "carryon"

    def __init__(self, name, ticketnumber, carryon):
        self.name = name
        self.ticketnumber = ticketnumber
        self.carryon = carryon

    def __str__(self):
        return str(self.name + ", ticket: " + str(self.ticketnumber) + " , carry_on : " + str(self.carryon))


class Stack:
    """

    We use the stack class to implement stacks in the aircraft to ensure the
    proper segregation of the passengers is done based on if they carry bags or not.

    """

    def __init__(self, size):
        self.arr = [None] * size
        self.capacity = size
        self.top = -1

    def push(self, x): #push data on top of a stack
        if self.isFull():
            print("Stack Overflow!! Calling exit()…")
            exit(1)
        self.top = self.top + 1
        self.arr[self.top] = x

    def pop(self):  #pop the top most element of the stack
        # check for stack underflow
        if self.isEmpty():
            print("Stack Underflow!! Calling exit()…")
            exit(1)
        top = self.arr[self.top]
        self.top = self.top - 1
        return top

    def size(self): #size of stack
        return self.top + 1

    # Function to check if the stack is empty or not
    def isEmpty(self):
        return self.size() == 0

    # Function to check if the stack is full or not
    def isFull(self):
        return self.size() == self.capacity


class Queue:
    """
        This class helps in implementing queues which are used in our program to check
        and segregate the passengers into different boarding queues (zones) based on the ticket number.

    """

    def __init__(self):
        self.queue = []

    def isEmpty(self) -> bool:
        return True if len(self.queue) == 0 else False

    def front(self) -> int: #set front of the queue
        return self.queue[-1]

    def rear(self) -> int: #set rear of the queue
        return self.queue[0]

    def enqueue(self, x: int) -> None:  #insertion into the queue at the end of it
        self.x = x
        self.queue.insert(0, x)

    def dequeue(self): #deletion from the from of the queue
        val = self.front()
        self.queue.pop()
        return val


def readpassengerfile():
    """
    Here we are using this method to read the passenger file
    :return: list with passenger details

    """

    if(len(sys.argv)!=2):
        print("Usage: python3 airit_simulation.py {filename} ")

    try:
        passenger = sys.argv[1]             #text file name given as command line argument
        passengerlist = []
        for line in open(passenger):
            passengerlist.append([line.strip("\n")])
        # print(passengerlist)
    except Exception as e:
        print("File not found {" + passenger + "}")

    return passengerlist


def printpassengers(aircraftlist):
    """
    This function is used to print the passenger details
    :param      aircraftlist:    list containing the passenger details

    """
    for data in aircraftlist:  # to get ticket numbers
        for passdetails in data:
            new = passdetails.split(",")
            passname = new[0]
            passticket = new[1]
            passcarry = new[2]
            pas = Passenger(passname, passticket, passcarry)
            print(pas)


def deboard(passwithcarry, passnocarry):
    """
    This method is called to deboard all the passengers from the plan in the format
    where all the passengers without carry bag leave before the ones with carry bag.
    :param      passwithcarry:  stack containing those passengers which have a carry on baggage.
    :param      passnocarry:    stack containing those passengers which do not have a carry on baggage.
    """
    poppedlist = []
    print('''\nThe aircraft has landed.
Passengers are disembarking...''')
    while (not (passnocarry.isEmpty())):
        poppedlist.append(passnocarry.pop())
    while (not (passwithcarry.isEmpty())):
        poppedlist.append(passwithcarry.pop())
    printpassengers(poppedlist)


def passengerinflight(aircraftlist):
    """
    This function check the passengers in the flight and calls the deboard function
    when required.
    :param      aircraftlist:   list containing all the passenger details
    """
    passwithcarry = Stack(len(aircraftlist))
    passnocarry = Stack(len(aircraftlist))

    for data in aircraftlist:
        for val in data:
            newval = val.split(",")
            if newval[2] == "True":
                #checking if carry on bag present or no and push in correct stack accordingly
                passwithcarry.push(data)
            else:
                passnocarry.push(data)

    deboard(passwithcarry, passnocarry)

def boardflight(zone1, zone2, zone3, zone4, aircraftcapacity, passengercount, gatecapacity):
    """
    This is the function which is used to perform the boarding of the passengers
    keeping in mind the requirement of fire mandate code and the max capacity of the aircraft.
    Here we have queues to check which zone the passanger belongs to based on ticket number.

    :param zone1:      queue for those passengers whose ticket number starts with 1
    :param zone2:      queue for those passengers whose ticket number starts with 2
    :param zone3:      queue for those passengers whose ticket number starts with 3
    :param zone4:      queue for those passengers whose ticket number starts with 4
    :param aircraftcapacity:    the maximum number of passengers permitted in the aircraft at a particular time
    :param passengercount:      counter which check if the passenger count has reached the gate capacity
    :param gatecapacity:        the maximum number of passengers permitted in the gate at a particular time
    :return: passengercount     counter which check if the passenger count has reached the gate capacity

    """
    aircraftlist = []
    if (zone4.isEmpty() and zone3.isEmpty() and zone2.isEmpty() and zone1.isEmpty()):
        return -1
    print("\nPassengers are boarding the aircraft...")
    for i in range(aircraftcapacity):               #ensuring the aircraft capacity is not crossed
        #appending passengers based on the ticket number
        if (not (zone4.isEmpty())):
            aircraftlist.append(zone4.dequeue())
            passengercount += 1
        elif (not (zone3.isEmpty())):
            aircraftlist.append(zone3.dequeue())
            passengercount += 1
        elif (not (zone2.isEmpty())):
            aircraftlist.append(zone2.dequeue())
            passengercount += 1
        elif (not (zone1.isEmpty())):
            aircraftlist.append(zone1.dequeue())
            passengercount += 1
    printpassengers(aircraftlist)

    if passengercount == aircraftcapacity:                  #max capacity of aircraft is reached
        print("The aircraft is full")
    # when the passengers at the gate ended up filling up
    if passengercount == gatecapacity or (zone4.isEmpty() and zone3.isEmpty() and zone2.isEmpty() and zone1.isEmpty()):
        print("There are no more passengers at the gate.")
    print("Ready for taking off ...")
    passengerinflight(aircraftlist)
    return passengercount

def embarkingpass(passengerlist, aircraftcapacity, gatecapacity, newpassfront):
    """
    This function embarks the passengers into the respective zones at the gate and enusring that no more passengers
    other than the gate capacity would enter the gate at a time.

    :param passengerlist:       list containing all the passenger details
    :param aircraftcapacity:    the maximum number of passengers permitted in the aircraft at a particular time
    :param gatecapacity:        the maximum number of passengers permitted in the gate at a particular time
    :param newpassfront:        counter used to check the number of passengers that have already flew in the aircraft.
    :return: newpassfront:      counter used to check the number of passengers that have already flew in the aircraft.
    """
    zone1 = Queue()
    zone2 = Queue()
    zone3 = Queue()
    zone4 = Queue()
    passcount = 0
    passengercount = 0

    passval = newpassfront + gatecapacity
    print("\nPassengers are lining up at the gate...")
    if (passval < len(passengerlist)):
        pass
    elif (passval > len(passengerlist)):
        passval = len(passengerlist) + 1
    for passdetails in passengerlist[newpassfront:passval]:
        for data in passdetails:
            new = data.split(",")
            passname = new[0]
            passticket = new[1]
            passcarry = new[2]
            first_digit = str(passticket)[0]
            pas = Passenger(passname, passticket, passcarry)
            newpassfront = passengerlist.index(passdetails)
            if (passcount < gatecapacity):
                print(pas)
                if first_digit == "4":
                    zone4.enqueue(passdetails)
                    passcount += 1
                elif first_digit == "3":
                    zone3.enqueue(passdetails)
                    passcount += 1
                elif first_digit == "2":
                    zone2.enqueue(passdetails)
                    passcount += 1
                else:
                    zone1.enqueue(passdetails)
                    passcount += 1
    newpassfront = newpassfront + 1

    if (passcount == gatecapacity):
        print("The gate is full; remaining passengers must wait.")

    while (passengercount < gatecapacity and passengercount != -1):
        passengercount = boardflight(zone1, zone2, zone3, zone4, aircraftcapacity, passengercount, gatecapacity)
    return newpassfront

def airit_simulation():
    """
    This is the main code where the simulation is happening
    and where the various properties are getting checked.
    """
    newpassfront = 0
    gatecapacity = input("Gate capacity: ")
    while not gatecapacity.isdigit():
        print("Enter valid number")
        gatecapacity = input("Gate capacity: ")

    aircraftcapacity = input("Aircraft capacity: ")
    while not aircraftcapacity.isdigit():
        print("Enter valid number")
        aircraftcapacity = input("Aircraft capacity: ")

    print("Beginning simulation...")
    passengerlist = readpassengerfile()

    while (newpassfront != len(passengerlist)):
        newpassfront = embarkingpass(passengerlist, int(aircraftcapacity), int(gatecapacity), newpassfront)

    print("Simulation complete; all passengers are at their destination!")

def main():
    airit_simulation()

if __name__ == '__main__':
    main()