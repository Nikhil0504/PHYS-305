# Write code that takes a temperature in Fahrenheit that is input by the user from the keyboard  
# and converts it to Celsius.  The output should be print to the screen.

# Get the temperature in Fahrenheit from the user
fahrenheit = float(input("Enter the temperature in Fahrenheit: "))

# Convert the temperature to Celsius
celsius = (fahrenheit - 32) * 5.0/9.0

# Print the temperature in Celsius
print("The temperature in Celsius is: ", celsius)

