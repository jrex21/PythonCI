# Jessica Rex
#
# Chapter 3 Challenge 1
#
# fortune cookie simulator
# displays 1 of 5 unique fortunes at random when run
# uses the random function, if, elif, and else statements

import random

fortune = random.randint(1, 5)

print("here is your random fortune:")

if fortune == 1:
    print("'Welcome' is a powerful word.")

elif fortune == 2:
    print("A dubious friend may be an enemy in camouflage.")

elif fortune == 3:
    print("A fresh start will put you on your way.")

elif fortune == 4:
    print("A friend is a present you give yourself.")

elif fortune == 5:
    print("A golden egg of opportunity falls into your lap this month.")

else:
    print("bad fortune, out of luck")

input("\n\nPress the enter key to exit.")
    
