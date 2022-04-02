"""
file: airrit_tests.py
description: This program is a test file for the airit_simulation program.
language: python3
author: Shreya Pramod, sp3045@rit.edu

"""

import sys
import airit_simulation as air

def main():

    passlist = air.readpassengerfile()   #need to provide file name as command line argument
    print("\n------------------Reading the user input file and storing it as a list: -------------------------")
    print(passlist)
    print(
        "-------------------------------------------------------------------------------------------------------------------")

    print("\n---------Embarking passengers zonewise in the gate and boarding and deboarding in the flight till all the passengers have reached the destination:------------------")
    air.embarkingpass(passlist, 2, 3, 0)
    print("-------------------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':
    main()