from scipy import stats
import numpy as np

y = [1,2,34,3.4,6.6,10,23,10,22,1,2.3,65]
x = [6,4,2,9,10,2,3,25.3,2,5,10.2,10]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

print slope, intercept, r_value**2, p_value, std_err