from pylab import *
from scipy.optimize import curve_fit 
import csv

with open('R1 COVIDtall.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    data = list(reader)

#print(data[0])

dagArr = []
totalArr = []
nyeArr = []
nyeArrSmoothed = []

for i in range (1,402): # fordi den første linja i filen er info om hva kolonnene er, så vi starter på 0, og range(0,n) itererer opp til n-1, så derfor bruker vi 402, fordi vi har 401 verider (0-400).
    #print(data[i])
    dagArr.append(int(data[i][0]))
    totalArr.append(int(data[i][1])-126521)
    nyeArr.append(int(data[i][2]))

nyeArrSmoothed.append(nyeArr[0])
nyeArrSmoothed.append(nyeArr[1])
nyeArrSmoothed.append(nyeArr[2])
nyeArrSmoothed.append(nyeArr[3])
for i in range (4,397):
    nyeArrSmoothed.append((nyeArr[i-4]+nyeArr[i-3]+nyeArr[i-2]+nyeArr[i-1]+nyeArr[i]+nyeArr[i+1]+nyeArr[i+2]+nyeArr[i+3]+nyeArr[i+4])/9)
nyeArrSmoothed.append(nyeArr[397])
nyeArrSmoothed.append(nyeArr[398])
nyeArrSmoothed.append(nyeArr[399])
nyeArrSmoothed.append(nyeArr[400])



from pylab import *
from scipy.optimize import curve_fit  # Leser inn dataene
import math

def h(t, C, a, b): 
    return C / (1 + a * np.exp(-b * t))

#params, _ = curve_fit(h, dagArr, totalArr, p0=[1, 1, 1])
#C, a, b = params
C_s = 1000000
a_s = 1
b_s = 1
[C,a,b] = curve_fit(h, dagArr, totalArr, p0=[C_s,a_s,b_s])[0] 
print("C =", round(C, 2))
print("a =", round(a, 2))
print("b =", round(b, 2))  # Plotter dataene sammen med grafen til h
plot(dagArr, totalArr)
plot(dagArr, nyeArr)
plot(dagArr, nyeArrSmoothed)
t = linspace(0, 400, 1000)
plot(t, h(t, C, a, b), "r") 
show() 