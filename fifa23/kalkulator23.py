# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 20:59:45 2023

@author: magdalon
"""

#Hvem vinner fotball-VM for kvinner?

#Nå som gruppespillet er ferdig kan vi bruke sannsynlighetsregning til å si noe om hvilket lag som kommer til å gå seirende ut av utslagsspillet. På grunn av trekningen av lagene er det ikke nødvendigvis det høyest ratede laget, USA, som er favoritten.

#---more---

##Vinne en kamp

#Vi begynner med å finne en metode for å forutsi vinnersansynlighetene i en enkeltkamp. Til dette bruker vi Fifa-rankingen til de to lagene. Vi finner sannsynligheten <i>p</i> for at lag 1 vinner med formelen:

#<math xmlns = 'http://www.w3.org/1998/Math/MathML'><mrow><mi>p</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>1</mn><mo>+</mo><msup><mn>10</mn><mrow><mo>-</mo><mfrac><mi>x</mi><mn>2</mn></mfrac></mrow></msup></mrow></mfrac></mrow></math>
#Hvor <i>x</i> avhenger av forholdet mellom ratingen til de to lagene:
#<math xmlns = 'http://www.w3.org/1998/Math/MathML'><mrow><mi>x</mi><mo>=</mo><mrow><mrow><mfrac><msub><mi>R</mi><mi>1</mi></msub><mn>200</mn></mfrac></mrow><mo>-</mo><mrow><mfrac><msub><mi>R</mi><mi>2</mi></msub><mn>200</mn></mfrac></mrow></mrow></mrow></math>
#Siden vi ser på utslagsrundene ser vi vekk i fra sannsynligheten for uavgjort, så sannsynligheten for at lag 2 vinner blir <i>1 - p</i>.

#Vi kan lage en Python-funksjon som regner ut denne sannsynligheten.

def p(score1, score2):
    return 1/(10**(-(score1 - score2)/400) + 1)

###Regneeksempel

#Vi kan se på vinnersannsynlighetene i en eventuell finale.

usa = 2090
england = 2041
print(p(usa, england))

#Vi ser at i en eventuell finale er det 57% sannsynlighet for at USA vinner.

#Vi kan også se på en mulig semifinale.

norge = 1908
print(p(usa, norge))

#Vi ser at når lagene er nærme i ranking er vinnersjansene omtrent 50/50, mens når landene er langt unna er det mer sannsynlig at det beste landet vinner.

#Vi må også huske på at FIFA-rakningen er omstridt, vi bruker denne mest fordi den er lett å regne med. Hvis du har en bedre formel kan du gjerne bruke den i stedet.

##Videre fra delfinalene

#Da vi så på herre-fotball(hvem-vinner-vm) fant vi vinnersannsynlighetene ved simulering. Denne gangen skal vi bare finne sannsynlighetene for å gå videre med eksakte beregninger.

#For å vinne sannsynligheten for at et lag vinner kvart-, semi- og finalen må vi betinge på alle lagene de kan møte på veien.

#Hvis Norge (N) skal vinne kvartfinalen (N2) må de først vinne åttendedelsfinalen (N1) og så slå enten Sverige (S) eller USA (U) i kvartfinalen. Vi betinger derfor sannsynligheten på om Sverige (S1) eller USA (U1) vinner sin åttendedelsfinale.

#P(N2) = P(N1)*(P(N2|S1)*P(S1) + P(N2|U1)*P(U1))

japan = 1917
sverige = 2050

pN2 = p(norge, japan)*(p(norge, sverige)*p(sverige, usa) + p(norge, usa)*p(usa, sverige))
print(pN2)

#Vi ser at Norges sjanser er relativt dårlige.

##VM-vinner

#Vi kan nå finne alle sannsynlighetene i utslagspillet og bruke dette til å finne lagenes sannsynlighet til å finne finalen og hele VM.

#Vi begynner med å legge inn land, score i en [Pandas]-[pd.DataFrame]. Vi legger også inn kolonner for sannsynligheten for å vinne delfinalene og finalen. pg er sannsynligheten for å komme videre fra gruppespillet, p8 er sannsynligheten for å vinne åttendedelsfinalen, etc. Siden alle lagene er videre er den første sannsynligheten 1, mens de andre må vi regne ut.

lag = ['Sveits', 'Spania', 'Nederland', 'Sør-Afrika',
       'Japan', 'Norge', 'Sverige', 'USA',
       'Australia', 'Danmark', 'Frankrike', 'Marokko',
       'England', 'Nigeria', 'Colombia', 'Jamaica']

rating = [1765.90, 2002.28, 1980.47, 1471.52,
          1916.68, 1908.25, 2049.71, 2090.03,
          1919.69, 1866.25, 2026.65, 1334.08,
          2040.76, 1554.94, 1702.64, 1536.81]

import pandas as pd

df = pd.DataFrame({"rating" : rating,
                   "pg" : 1,
                   "p8" : 0,
                   "pq" : 0,
                   "ps" : 0,
                   "p1" : 0},
                   index = lag)

#Vi kan nå lage en løkke som bruker formelen for total sannsynlighet for å regne ut sannsynlighetene kolonne for kolonne. For åttendedelsfinalene ser vi på to og to lag, mens for kvartfinalene, semifinalene og finalen ser vi på grupper av 4, 8 og til slutt alle lagene.

for n in range(0, 4):
  offset = 2**n
  for i in range(8//offset):
    forrige = df.columns[n + 1]
    neste = df.columns[n + 2]
    for j in range(offset):
      for k in range(offset):
        a = df.index[2*offset*i + j]
        b = df.index[2*offset*i + offset + k]
        df.at[a, neste] += df.at[a, forrige]*df.at[b, forrige]*p(df.at[a, 'rating'], df.at[b, 'rating'])
        df.at[b, neste] += df.at[a, forrige]*df.at[b, forrige]*p(df.at[b, 'rating'], df.at[a, 'rating'])

#Til slutt får vi et resultat:

print(df.to_string(float_format=lambda x: f"{x:.2f}"))

#Vi kan fremstille dette resultatet grafisk.

df.p1.sort_values().plot.barh()

#Vi ser at England har den beste vinnersjansen. England som ligger best an fordi USA sin sin vei til finalen (Spania, Nederland, Sverige fra topp 6) er mye hardere enn Englands (bare Frankrike fra topp 6).

##Analyse

###Lette og tunge veier til gull

#Vi kan tegne vinnersjansene som en funksjon av ratingen.

import matplotlib.pyplot as plt
plt
df.plot.scatter(x='rating', y='p1')
for idx, row in df.iterrows():
    plt.annotate(idx, (row['rating'], row['p1']))

#Vi ser at sammenhengen mellom rating og vinnersannsynlighet ikke er lineær.

#Vi kan se på "lette" og "tunge" veier ved å sortere lagene etter rating og vinnersannsynlighet og tegne disse i et punktdiagram.

plt
df.rank().plot.scatter(x='rating', y='p1')
for idx, row in df.rank().iterrows():
    plt.annotate(idx, (row['rating'], row['p1']))
plt.axline((0,0), slope=1, color="black")
plt.show()

#Lagene som ligger over streken kommer høyere opp på listen over sannsynlige vinnere enn det ratingen skulle tilsi, og kan sies å ha en <i>lett</i> vei, mens lagene under streken kan sies å ha en <i>tung</i> vei.


##Konklusjon

#Det ser ut til at vi får høre mer av dette:

#https://youtu.be/6kRrQuVKiUE?t=40
