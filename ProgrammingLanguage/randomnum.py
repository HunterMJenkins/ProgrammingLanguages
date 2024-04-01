#Hunter Jenkins
def random():
    # Create a memory address of an object 
    num = id({})
    return (num % 100)

print(random())
