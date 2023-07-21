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

fifa_ranking = {}

grupper = [['Sveits', 'New Zealand', 'Norge', 'Filipinene'],
           ['Australia', 'Nigeria', 'Canada', 'Irland'],
           ['Spania', 'Costa Rica', 'Zambia', 'Japan'],
           ['England', 'Haiti', 'Danmark', 'Kina'],
           ['USA', 'Vietnam', 'Nederland', 'Portugal'],
           ['Frankrike', 'Jamaica', 'Brasil', 'Panama'],
           ['Sverige', 'Sør-Afrika', 'Italia', 'Argentina'],
           ['Tyskland', 'Marokko', 'Columbia', 'Sør-Korea']]

def p(ranking1, ranking2):
    return 1/(10**(-(ranking1 - ranking2)/600) + 1)


df = pd.DataFrame({'poeng' :  [1694.51, 1627.48, 1773.88, 1488.72, 1559.54, 1645.64, 1841.3, 1530.3, 1728.47, 1584.38, 1759.78, 1548.59, 1563.5, 1715.22, 1676.56, 1635.92],
                   'p16' : 1,
                   'p8' : 0,
                   'pq' : 0,
                   'ps' : 0,
                   'p1' : 0},
                  index = ['Nederland', 'USA', 'Argentina', 'Austraila', 'Japan', 'Kroatia', 'Brazil', 'Sør-Korea', 'England', 'Senegal', 'Frankrike', 'Polen', 'Marokko', 'Spania', 'Portugal', 'Sveits'])

#For å finne sannsynlighetene må vi gå gjennom listen og bruke formelen for total sannsynlighet. For å finne vinneren i 8.delsfinalen er det relativt rett fram.

for i in range(8):
    a = df.index[2*i] #Det første laget
    b = df.index[2*i + 1] #Det andre laget
    df.at[a, 'p8'] += df.at[a,'p16']*df.at[b,'p16']*p(df.at[a, 'poeng'], df.at[b, 'poeng'])
    df.at[b, 'p8'] += df.at[a,'p16']*df.at[b,'p16']*p(df.at[b, 'poeng'], df.at[a, 'poeng'])

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

print(df)

#Som vi kan fremstille grafisk.

df.p1.plot.barh()

#%%
df.plot.scatter(x='poeng', y='p1')
print(df[['poeng','p1']].rank())
print(df[['poeng','p1']].rank().diff(axis=1))
