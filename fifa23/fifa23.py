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
    return 1/(10**(-(score1 - score2)/400) + 1)

lag = [v[0], r[2],
       v[2], r[0],
       v[4], r[6],
       v[6], r[4],
       v[1], r[3],
       v[3], r[1],
       v[7], r[5],
       v[5], r[7]]

rating = 'FIFA-rating'
pg = 'Videre fra gruppe-spill'
p8 = 'Vinner åttendedels-finale'
pq = 'Vinner kvart-finale'
ps = 'Vinner semi-finale'
p1 = 'Vinner VM'

def beregn(lag):
    df = pd.DataFrame({rating : [score[l] for l in lag],
                       pg : 1,
                       p8 : 0,
                       pq : 0,
                       ps : 0,
                       p1 : 0},
                      index = lag)

    for n in range(0, 4):
        offset = 2**n
        for i in range(8//offset):
            forrige = df.columns[n + 1]
            neste = df.columns[n + 2]
            for j in range(offset):
                for k in range(offset):
                    a = df.index[2*offset*i + j]
                    b = df.index[2*offset*i + offset + k]
                    df.at[a, neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[a, rating], df.at[b, rating])
                    df.at[b,neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[b, rating], df.at[a, rating])

    return df

df = beregn(lag)


df[p1].plot.barh()

#%%
df.plot.scatter(x=rating, y=p1)
for idx, row in df.iterrows():
    plt.annotate(idx, (row[rating], row[p1]))

print(df[[rating, p1]].rank(ascending=False))
print(df[[rating, p1]].rank(ascending=False).diff(axis=1))

df.rank().plot.scatter(x=rating, y=p1)
for idx, row in df.rank().iterrows():
    plt.annotate(idx, (row[rating], row[p1]))
plt.axline((0,0), slope=1, color="black", linestyle="--")
plt.show()
print((1-df[p1])/df[p1])
print(((1-df[p1])/df[p1]))

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 5.7, 4
plt.rcParams.update({'font.size': 14})
df[p1].sort_values().plot.barh(color="pink", width=0.8,title="VM kvinner (Australia og New Zealand)")
plt.xlim(0, 0.25)
plt.grid(True, axis='x')
plt.show()


#%%

from sympy import symbols, Eq

pp, x, R1, R2 = symbols(["p","x", "R1", "R2"])

likn1 = Eq(x, (R1-R2)/200)
likn2 = Eq(pp, 1/(1 + 10**(-x/2)))
likn3 = likn2.subs(x, likn1.rhs)

#%%


def bracket(lag):
    df = pd.DataFrame({rating : [score[l] for l in lag],
                       pg : 1,
                       p8 : 0,
                       pq : 0,
                       ps : 0,
                       p1 : 0},
                      index = lag)

    for n in range(0, 4):
        offset = 2**n
        for i in range(8//offset):
            forrige = df.columns[n + 1]
            neste = df.columns[n + 2]
            for j in range(offset):
                for k in range(offset):
                    a = df.index[2*offset*i + j]
                    b = df.index[2*offset*i + offset + k]
                    df.at[a, neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[a, rating], df.at[b, rating])
                    df.at[b, neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[b, rating], df.at[a, rating])
            df[neste] = round(df[neste])

    return df

dfb = bracket(lag)

print(dfb)
print(dfb.to_string(header=False))
