from pylab import *
from scipy.optimize import curve_fit 
import csv
import math

with open('R1 COVIDtall.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    data = list(reader)

#print(data[0])

dagArr = []
totalArr = []
nyeArr = []
totArrLong = []
totArrSmoothed = []
totArrSmoothedDer = []

for i in range (1,402): # fordi den første linja i filen er info om hva kolonnene er, så vi starter på 0, og range(0,n) itererer opp til n-1, så derfor bruker vi 402, fordi vi har 401 verider (0-400).
    #print(data[i])
    dagArr.append(int(data[i][0]))
    totalArr.append(int(data[i][1])-126521)
    nyeArr.append(int(data[i][2]))


def finnGlatt(i):
    n = i%1
    heltall = int(i//1)
    if (heltall == 400):
        return totalArr[400]
    else:
        return lerp(totalArr[heltall],totalArr[heltall+1],n)


def lerp(a,b,t):
    return a + t * (b - a)

def derivertTotArrSmoothed(a):
    return (totArrSmoothed[a+1]-totArrSmoothed[a])

tidSub = linspace(0, 400, 800)

for i in tidSub:
    totArrLong.append(finnGlatt(i))


for i in range(0,len(tidSub)):
    dist = min(i-0,len(tidSub)-i) #den forteller avstanden i er fra enten starten eller slutten av listen.
    smoothSize = math.floor(int(min(dist,50))/2) #tid her er hvor stort ommråde vi maks skal se på for å glatte ut funksjonen. vi gjør dette så vi ikke prøver å bruke verdier utenfor lista
    value = totArrLong[i]
    for j in range(0,smoothSize):
        value += totArrLong[i+j] + totArrLong[i-j]
    totArrSmoothed.append(value/(1+(smoothSize*2)))


for i in range(0,len(tidSub)-1):
    totArrSmoothedDer.append(derivertTotArrSmoothed(i))
totArrSmoothedDer.append(derivertTotArrSmoothed(1))

#print(totArrLong)

dx = 0.0001

def hDerivert(t,C,a,b):
    return (h(t+dx,C,a,b)-h(t,C,a,b))/dx

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
plot(tidSub, totArrSmoothed)
#plot(dagArr, nyeArr)
plot(tidSub, h(tidSub, C, a, b), "r") 
plot(tidSub, totArrSmoothedDer) 
plot(tidSub, hDerivert(tidSub, C, a, b)) 
show() 