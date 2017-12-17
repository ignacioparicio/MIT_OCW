# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:36:34 2017

@author: S4XYMX
"""

annual_salary=float(input('What is your annual salary?\n'))
portion_saved=float(input('What is your savings rate?\n'))
total_cost=float(input('What is the cost of your dream home?\n'))
semi_annual_raise=float(input('What is your expected semi-annual rise?\n'))

portion_down_payment=0.25
r=0.04
down_payment=portion_down_payment*total_cost

current_savings=0
months=0
while current_savings<down_payment:
    current_savings+=(current_savings*r+annual_salary*portion_saved)/12
    months+=1
    if months%6 == 0:
        annual_salary*=(1+semi_annual_raise)

print('Months needed:', months)
    
    