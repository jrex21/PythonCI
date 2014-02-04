# Useless Trivia
#
# Jessica Rex
#
# Gets personal information from the user and then
# prints true but useless information about him or her
#
# added functionality: get a random fact based on user input

name = input("Hi. What's your name? ")

age = int(input("How old are you? "))

weight = int(input("Okay, last question. How many pounds do you weigh? " ))

print("\nIf poet ee cummings were to email you, he'd address you as", name.lower())
print("But if ee were mad, he'd call you", name.upper())

called = name * 5
print("\nIf a small child were trying to get your attention",)
print("your name would become:")
print(called)

seconds = age * 365 * 24 * 60 * 60
print("\nYou're over", seconds, "seconds old.")

moon_weight = weight / 6
print("\nDid you know that on the moon you would weigh only", moon_weight, "pounds?")

sun_weight = weight * 27.1
print("On the sun, you'd weigh", sun_weight, "(but, ah...not for long).")

choice = int(input("\n\nEnter 1, 2, or 3 for a random fact! "))

if choice == 1:
    print("You chose 1, did you know there is a waterfall in Antarctica that runs red as blood?")
if choice == 2:
    print("You chose 2, did you know hummingbirds have 2,000 meals a day?")
if choice == 3:
    print("You chose 3, did you know crocodiles have no lips?")
          


input("\n\nPress the enter key to exit.")

