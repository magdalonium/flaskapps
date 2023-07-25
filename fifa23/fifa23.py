# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 08:59:42 2023

@author: magdalon
"""

#Tittel

#Innledning

#---more---

##Biblioteker

#Vi begynner med å importere bibliotekene vi har tenkt å bruke.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp

score = {'Argentina' : 1682.45,
 'Australia' : 1919.69,
 'Brasil' : 1995.3,
 'Canada' : 1996.34,
 'Columbia' : 1702.64,
 'Costa Rica' : 1596.94,
 'Danmark' : 1866.25,
 'England' : 2040.76,
 'Filipinene' : 1512.97,
 'Frankrike' : 2026.65,
 'Haiti' : 1475.33,
 'Irland' : 1743.59,
 'Italia' : 1846.5,
 'Jamaica' : 1536.81,
 'Japan' : 1916.68,
 'Kina' : 1854.49,
 'Marokko' : 1334.08,
 'Nederland' : 1980.47,
 'New Zealand' : 1699.7,
 'Nigeria' : 1554.94,
 'Norge' : 1908.25,
 'Panama' : 1482.51,
 'Portugal' : 1745.13,
 'Spania' : 2002.28,
 'Sveits' : 1765.9,
 'Sverige' : 2049.71,
 'Sør-Afrika' : 1471.52,
 'Sør-Korea' : 1840.27,
 'Tyskland' : 2061.56,
 'USA' : 2090.03,
 'Vietnam' : 1648.,
 'Zambia' : 1298.31}

grupper = [['Sveits', 'New Zealand', 'Norge', 'Filipinene'],
           ['Australia', 'Nigeria', 'Canada', 'Irland'],
           ['Spania', 'Costa Rica', 'Zambia', 'Japan'],
           ['England', 'Haiti', 'Danmark', 'Kina'],
           ['USA', 'Vietnam', 'Nederland', 'Portugal'],
           ['Frankrike', 'Jamaica', 'Brasil', 'Panama'],
           ['Sverige', 'Sør-Afrika', 'Italia', 'Argentina'],
           ['Tyskland', 'Marokko', 'Columbia', 'Sør-Korea']]

v, r = zip(*[sorted(gruppe, key=score.get, reverse=True)[:2] for gruppe in grupper])



#%%
def p(score1, score2):
    return 1/(10**(-(score1 - score2)/200) + 1)

lag = [v[0], r[2],
       v[2], r[0],
       v[4], r[6],
       v[6], r[4],
       v[1], r[3],
       v[3], r[1],
       v[7], r[5],
       v[5], r[7]]

poeng = [score[l] for l in lag]

#%%

pg = 'Videre fra gruppespill'
p8 = 'Vinner åttendedelsfinale'
pq = 'Vinner kvartfinale'
ps = 'Vinner semifinale'
p1 = 'Vinner VM'

df = pd.DataFrame({'poeng' : poeng,
                   pg : 1,
                   p8 : 0,
                   pq : 0,
                   ps : 0,
                   p1 : 0},
                  index = lag)

#For å finne sannsynlighetene må vi gå gjennom listen og bruke formelen for total sannsynlighet. For å finne vinneren i 8.delsfinalen er det relativt rett fram.

for i in range(8):
    a = df.index[2*i] #Det første laget
    b = df.index[2*i + 1] #Det andre laget
    df.at[a, p8] += df.at[a, pg]*df.at[b, pg]*p(df.at[a, 'poeng'], df.at[b, 'poeng'])
    df.at[b, p8] += df.at[a, pg]*df.at[b, pg]*p(df.at[b, 'poeng'], df.at[a, 'poeng'])

#For de videre finalene er det litt mer komplisert. For kvartfinalene må vi se på grupper av fire lag for å regne ut sannsynlighetene, for semifinale må vi se på grupper av 8 lag, og for finalen må vi se på alle lagene. For hvert steg tar vi utgangspunkt i sannsynlighetene i det forrige steget.

for n in range(1, 4):
    offset = 2**n
    for i in range(8//offset):
        forrige = df.columns[n + 1]
        neste = df.columns[n + 2]
        for j in range(offset):
            for k in range(offset):
                a = df.index[2*offset*i + j]
                b = df.index[2*offset*i + offset + k]
                df.at[a, neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[a, 'poeng'], df.at[b, 'poeng'])
                df.at[b,neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[b, 'poeng'], df.at[a, 'poeng'])

#Til slutt får vi et resultat.

print(df.round(3))

#Som vi kan fremstille grafisk.

df[p1].plot.barh()

#%%
df.plot.scatter(x='poeng', y=p1)
for idx, row in df.iterrows():
    plt.annotate(idx, (row['poeng'], row[p1]))

print(df[['poeng',p1]].rank(ascending=False))
print(df[['poeng',p1]].rank(ascending=False).diff(axis=1))

df.rank().plot.scatter(x='poeng', y=p1)
for idx, row in df.rank().iterrows():
    plt.annotate(idx, (row['poeng'], row[p1]))
plt.axline((0,0), slope=1, color="black", linestyle="--")

print((1-df[p1])/df[p1])
print(((1-df[p1])/df[p1]))

