#  Problem Set 1a
#  with minimal modifications in displaying results

running = True
while True:
    try:
        annual_salary = float(input("Enter your annual salary: "))
        portion_saved = float(
            input("Enter the percent of your salary to save, as a decimal: "))
        total_cost = float(input("Enter the cost of your dream home: "))
        break

    except ValueError:
        print("Please type float or integers only.")

percent_downpayment = 0.25
monthly_salary = annual_salary / 12
monthly_r = 0.04 / 12

current_savings = 0
months = 0  # 1 counter represents a month

while current_savings < total_cost * percent_downpayment:
    current_savings += (monthly_salary * portion_saved) + \
        (current_savings * monthly_r)
    months += 1

print()
print("Needed downpayment: {0:.2f} pesos".format(
    round(total_cost * percent_downpayment, 2)))
print("Total savings: {0:.2f} pesos".format(round(current_savings, 2)))
print("Number of months: {} months".format(months))
