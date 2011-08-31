# coding=utf-8
import math

principal = 1000000
installment = 100000
annual_rate = 0.05
monthly_rate = math.pow(1+annual_rate, 1.0/12) - 1

total_interest = 0;
month = 1
while True:
    interest = principal * monthly_rate
    total_interest += interest
    principal += installment + interest
    month += 1
    if principal > 100000000:
        break

print str(month/12.0)+'年('+str(month)+'ヶ月)後'
print u'利子合計:' + str(total_interest)
print u'合計:' + str(principal)

