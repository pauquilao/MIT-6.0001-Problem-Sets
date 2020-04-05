#  Problem Set 1b
#  with minimal modifications in displaying results


running = True
while True:
    try:
        annual_salary = float(input("Enter your annual salary: "))
        portion_saved = float(
            input("Enter the percent of your salary to save, as a decimal: "))
        total_cost = float(input("Enter the cost of your dream home: "))
        semi_annual_raise = float(
            input("Enter you semi-annual salary raise: "))
        break

    except ValueError:
        print("Please type float or integers only.")

#  fixed values
portion_downpayment = total_cost * 0.25
monthly_r = 0.04 / 12

#  increasing values
current_savings = 0
months = 0

while current_savings < portion_downpayment:
    months += 1
    #  monthly salary will be increased after every 6 months so it is now placed inside the loop block
    monthly_salary = annual_salary / 12
    #  inrement in savings after each month
    current_savings += (monthly_salary * portion_saved) + \
        (current_savings * monthly_r)

    #  increase in annual salary every 6 months.
    #  remainder of 0 means that it is the 6th, 12th, 18th count and so on.
    if months % 6 == 0:
        annual_salary += (annual_salary * semi_annual_raise)
print()
print("Needed downpayment: {0:.2f} pesos".format(portion_downpayment))
print("Total savings: {0:.2f} pesos".format(round(current_savings, 2)))
print("Number of months: {} months".format(months))
