# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:36:34 2017

@author: S4XYMX
"""

annual_salary=float(input('Enter the starting salary:\n'))

months=36
total_cost=1e6
semi_annual_raise=0.07

portion_down_payment=0.25
r=0.04
down_payment=portion_down_payment*total_cost

def final_savings(months,semi_annual_raise,annual_salary,r,guess):
    portion_saved=guess/10000.0
    current_savings=0
    months_passed=0
    for i in range(months):
        current_savings+=(current_savings*r+annual_salary*portion_saved)/12
        months_passed+=1
        if months_passed%6 == 0:
            annual_salary*=(1+semi_annual_raise)
    return current_savings
    
epsilon=100
low=0
high=10000
guess=(high+low)//2 # guess for the portion saved

num_guesses=0

if final_savings(months,semi_annual_raise,annual_salary,r,high)<down_payment:
    print("It is not possible to pay the down payment in three years.")

else:

    for i in range(14): # having 10000 elements, it cannot take longer than 14 attempts
        savings=final_savings(months,semi_annual_raise,annual_salary,r,guess)
        num_guesses+=1
        if(abs(down_payment-savings)>epsilon):
            if(savings>down_payment): 
                high=guess # case "I saved too much" -> search lower end
            else:
                low=guess # case "I didn't save enough" -> search higher end
        else:
            best_saving_rate=guess/10000.0
            break
        guess=(high+low)//2

if num_guesses !=0:
    print("Steps in bisection search:",num_guesses)
    print("Best savings rate: ", best_saving_rate)
    
        


    
    