from pylab import *
from scipy.optimize import curve_fit 
import csv
import math

with open('R1 COVIDtall.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    data = list(reader)

#print(data[0])

dagArr = [] # en liste over dager i datasettet
totalArr = [] # totale mengden folk som har er syke/ har hat covid.
nyeArr = [] # mengden nye smittede folk per dag
totArrLong = [] # totalArr utvidet til flere steg med lineær interpolering.
totArrSmoothed = [] # en glattet-ut versjon av den utvidede Total-mengden med smittede folk.
totArrSmoothedDer = [] # verdiene til den deriverte av den glattet-ut grafen for totale mengden smittede folk.

for i in range (1,402): # fordi den første linja i filen er info om hva kolonnene er, så vi starter på 0, og range(0,n) itererer opp til n-1, så derfor bruker vi 402, fordi vi har 401 verider (0-400).
    #print(data[i])
    dagArr.append(int(data[i][0]))
    totalArr.append(int(data[i][1])-126521) # en verdi-offsett satt på per nå fordi vi er ute etter mengden flere folk som er syke fra starten av datasettet.
    nyeArr.append(int(data[i][2]))

def lerp(a,b,t): #standard lineær interpolerings funksjon
    return a + t * (b - a)

tidSub = linspace(0, 400, 800) # en liste for tidsenheter for høyere oppløsning en 0-400 dager, brukes så vi kan få mer presise derivasjons-verider og en glattere graf.
def interpolerData(i): #interpolerer dataen fra totalArr fra 0-400 dager til 0-x antall tidsenheter, med lineær interpolering. ( funksjonen funker best når x>400) 
    n = i%1
    heltall = int(i//1)
    if (heltall == 400):
        return totalArr[400]
    else:
        return lerp(totalArr[heltall],totalArr[heltall+1],n)

# Definerer et mer detaljert tidsrom innenfor de 400 dagene og interpolerer dataen med lineær interpolering for å få flere tids-steg for dataen, dette gjør vi fordi det gir oss mer presis derivering.
# 
# vi definerer en funksjon for lineær interpolering
# funksjonen fungerer ved å returnere tallet som er i mellom to tall, basert på en faktor t.
#
# funksjonen tar in et tids-steg, og gir ut hva det interpolerte tallet skal være der når vi bruker dataene for totale smittede.
# siden tids-stegene våre er float tall (fordi det går 343.0, 343.25, 343.5, 343.75, 344) så finner vi desimal-verdien ved å bruke modulo %1
# vi finner også heltallsverdien ved å bruke heltallsdivisjon med 1.
# så har vi en edge-case test, for om verdien vi prøver å finne er helt på enden av tids-rommet, altså dag 400, for da kan vi bare returnere den siste verdien. (dette gjør vi for å ungå error)
# så bruker vi lineær interpoleringsfunksjonen, for å finne verdien av det spesifikke tids-steget vi leter etter.
#


dt = tidSub[1] - tidSub[0]

def derivertTotArrSmoothed(a):
    return (totArrSmoothed[i+1] - totArrSmoothed[i-1]) / (2*dt)

for i in tidSub:
    totArrLong.append(interpolerData(i))


for i in range(0,len(tidSub)):
    dist = min(i-0,len(tidSub)-i) #den forteller avstanden i er fra enten starten eller slutten av listen.
    smoothSize = math.floor(int(min(dist,100))/2) #tid her er hvor stort ommråde vi maks skal se på for å glatte ut funksjonen. vi gjør dette så vi ikke prøver å bruke verdier utenfor lista
    value = totArrLong[i]
    for j in range(0,smoothSize):
        value += totArrLong[i+j] + totArrLong[i-j]
    totArrSmoothed.append(value/(1+(smoothSize*2)))


for i in range(1,len(tidSub)-1):
    totArrSmoothedDer.append(derivertTotArrSmoothed(i))
totArrSmoothedDer.append(derivertTotArrSmoothed(1))
totArrSmoothedDer.append(derivertTotArrSmoothed(1))

#print(totArrLong)

dx = 0.0001

def hDerivert(t,C,a,b):
    return (h(t+dx,C,a,b)-h(t,C,a,b))/dx

def hDobbeltDerivert(t,C,a,b):
    return (hDerivert(t+dx,C,a,b)-hDerivert(t,C,a,b))/dx

def h(t, C, a, b): 
    return C / (1 + a * np.exp(-b * t))


#params, _ = curve_fit(h, dagArr, totalArr, p0=[1, 1, 1])
#C, a, b = params
C_s = 1000000
a_s = 1
b_s = 1
[C,a,b] = curve_fit(h, tidSub, totArrSmoothed, p0=[C_s,a_s,b_s])[0] 
print("C =", round(C, 2))
print("a =", round(a, 2))
print("b =", round(b, 2))  # Plotter dataene sammen med grafen til h

#plot(dagArr, totalArr)
#plot(tidSub, totArrSmoothed)
#plot(dagArr, nyeArr)
#plot(tidSub, h(tidSub, C, a, b), "r") 

#plot(tidSub, totArrSmoothedDer) 
#plot(tidSub, hDerivert(tidSub, C, a, b)) 
plot(tidSub, hDobbeltDerivert(tidSub, C, a, b)) 


axhline(0, color='black')
axvline(0, color='black')

plt.xlabel("Dager siden juni 2021")
#plt.ylabel("Antall nye korona tilfeller")
plt.ylabel("x")
#plt.title("Rå-data Totalt smittede")
plt.title("andre derivert av regresjonsfunksjonen")

legend()
show()