# Jessica Rex
#
# Chapter 4 Challenge 1
# This program counts for the user. It uses input from the user, for loops
# and the range function to count. The user provides the starting and
# ending values, as well as the amount by which to count
#
# I also added in an additional sum that will add the values it has counted.

print("Welcome to the counter program!")

start = int(input("Please enter a starting number: "))
end = int(input("Please enter an ending number: "))
count = int(input("Please enter the amount by which to count: "))

sum = 0

for i in range(start, end, count):
    print(i, end=" ")
    sum += i

print("\nThe sum of these numbers is: ", sum)

input("\n\nPress the enter key to exit.")
