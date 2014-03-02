# Jessica Rex
# Chapter 5 Challenge 3
# Who's Your Daddy Program

# This program uses dictionaries, so when a person types in a name, the
# program looks up that person and returns his or her dad's name. The user
# can add, replace, or delete pairs.

dads = {"Harry" : "James",
        "Ron" : "Arthur",
        "Neville" : "Frank"}

print("Welcome to Who's Your Daddy!\n")

choice = None
while choice != "0":
    print("""
          Who's Your Daddy
          0 - Quit
          1 - Look Up a Dad
          2 - Add a Dad
          3 - Replace a Dad
          4 - Delete a Pair """)
