#  Problem Set 1b
#  with minimal modifications in displaying results

running = True
while True:
    try:
        base_annual_salary = float(input("Enter your annual salary: "))
        break

    except ValueError:
        print("Please type float or integers only.")

#  fixed data
total_cost = 1000000         # total cost of dream house
percent_down_payment = 0.25  # 25% of total cost
monthly_r = 0.04 / 12        # monthly rate of return of investment
semi_annual_raise = 0.07     # increae in annual salary every after six months
down_payment = total_cost * percent_down_payment
months = 36                  # minimum months to pay for down payment

#  margin of error for bisection search
epsilon = 100   # within 100 pesos of the required down payment

#  bounds for bisection search
initial_high = 10000  # 10000 for 100%
high = initial_high   # high boundary for the formula (High + Low)/2
low = 0               # lower boundary

#  initial values for the while loop
current_savings = 0
step = 0   # step in bisection search
# floor division to get the integer quotient
portion_saved = (high + low) // 2

#  start of bisection search
while abs(current_savings - down_payment) > epsilon:
    #  for each iteration in for loop, all variable are reset to initial values except step variable
    step += 1
    current_savings = 0
    annual_salary = base_annual_salary
    monthly_salary = annual_salary / 12
    monthly_deposit = monthly_salary * (portion_saved / 10000)

    #  computes current savings every month for 36 months
    #  iteration start from 1 intead of 0 since 0%6 = 0
    #  and this will satisfy the condition of semi-annual increase
    for month in range(1, months + 1):
        #  increase in annual salary every 6 months.
        #  remainder of zero means that it is the 6th, 12th, 18th count and so on
        current_savings += (current_savings * monthly_r)
        current_savings += monthly_deposit
        if month % 6 == 0:
            annual_salary += (annual_salary * semi_annual_raise)
            monthly_salary = annual_salary / 12
            monthly_deposit = monthly_salary * (portion_saved / 10000)

    #  assigns portion_saved to variable prev_portion_saved
    #  to be used as conditional statement to exit from the loop
    prev_portion_saved = portion_saved
    if current_savings < down_payment:
        low = portion_saved
    else:
        high = portion_saved

    #  computes new savings rate with new bounds
    #  cast to integer so that low and high bounds will converge completely
    #  if the solution is outside the search space with respect to high bound
    portion_saved = int(round((high + low) / 2))
    #  if portion_saved remains constant with comparison to prev_portion_saved, solution is outside search space
    #  break to exit from infinite loop
    if prev_portion_saved == portion_saved:
        break

print()
#  after 36 iterations, if current savings does not suffice the required down payment,
#  base annual salary is not enough for the required down payment
if portion_saved == initial_high:
    print("Not possible to acquire the house within 36 months.")
else:
    print("Best savings rate: {}".format(round(portion_saved / 10000, 4)))
    print("Steps in Bisection search: {}".format(step))
