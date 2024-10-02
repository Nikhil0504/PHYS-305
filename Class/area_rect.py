# Calculate areas of shapes

def rectangle_area(length, width):
    return length * width

def circle_area(radius):
    return 3.14159 * radius**2


print("This program calculates areas.")
print()
print("What shape would you like to know the area for?")
print("1: Rectangle")
print("2: Circle")
shape = int(input("> "))

if shape == 1:
    length = float(input("Enter the length of the rectangle: "))
    width = float(input("Enter the width of the rectangle: "))

    Area = rectangle_area(length, width)

    print("The area of the rectangle is: ", Area)
elif shape == 2:
    radius = float(input("Enter the radius of the circle: "))

    Area = circle_area(radius)

    print("The area of the circle is: ", Area)
else:
    print("Invalid choice.")