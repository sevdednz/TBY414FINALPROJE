import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import statsmodels
from statsmodels.tsa.stattools import adfuller

data = pd.read_csv("Hospitals.csv", sep=';') #yatak sayısı verilerini çekiyoruz
print("Hindistanda Bölgelere Göre Yatak Sayıları:")
print(data)
#bulduğumuz verilere göre ilk 100 gündeki hasta sayısı
df={'Günler':["Mar 13","Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20","Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27","Mar 28","Mar 29","Mar 30","Mar 31","Apr 01","Apr 02","Apr 03","Apr 04","Apr 05","Apr 06","Apr 07","Apr 08","Apr 09","Apr 10","Apr 11","Apr 12","Apr 13","Apr 14","Apr 15","Apr 16","Apr 17","Apr 18","Apr 19","Apr 20","Apr 21","Apr 22","Apr 23","Apr 24","Apr 25","Apr 26","Apr 27","Apr 28","Apr 29","Apr 30","May 01","May 02","May 03","May 04","May 05","May 06","May 07","May 08","May 09","May 10","May 11","May 12","May 13","May 14","May 15","May 16","May 17","May 18","May 19","May 20","May 21","May 22","May 23","May 24","May 25","May 26","May 27","May 28","May 29","May 30","May 31","Jun 01","Jun 02","Jun 03","Jun 04","Jun 05","Jun 06","Jun 07","Jun 08","Jun 09","Jun 10","Jun 11","Jun 12","Jun 13","Jun 14","Jun 15","Jun 16","Jun 17","Jun 18","Jun 19","Jun 20"],'Hasta':[70,88,99,114,126,152,170,221,304,365,455,486,602,662,794,879,902,1117,1239,1792,2280,2781,3260,3843,4267,4723,5232,5863,6577,7189,7794,8914,9735,10440,11214,11825,13381,14202,14674,15460,16319,17306,18171,19519,20486,21375,22569,23546,24641,26027,27557,29339,32024,33565,35871,37686,39823,41406,43980,45925,47457,49104,51379,52773,53553,55878,57939,60864,63172,66089,69244,73170,76820,80072,82172,85803,89755,85884,89706,93349,97008,101077,106665,111900,116302,120981,126431,129360,132896,138069,142810,146482,150101,153574,152791,154688,160564,163305,168636,170269]} 
df=pd.DataFrame(df)
print("13 Marttan itibaren 100 gündeki hasta sayısı:")
print(df)
#2. 50 günün tahmini hesaplanması
df_copy=df.iloc[50:].copy()
df_copy['Tahmin'] = df.iloc[:,1].rolling(window=7).mean() #moving average hesaplanması
print("Tahmin edilen sonraki 50 gün:")
print(df_copy)

toplam = 0  #fark toplamı
for i in range (0,50): 
    fark = df_copy.iloc[i,1]- df_copy.iloc[i,2] #finding the difference between observed and predicted value
    kare = fark**2  #farkın karesi
    toplam = toplam + fark  #farkların toplamı
MSE = toplam/50  #ort hesabı
print ("\nThe Mean Square Error: " , MSE)

x = datetime.datetime(2020, 6, 20) 
#sonraki 100 günü tahmin etmek
print("\nTahmini sonraki 100 gün:")
for i in range(0,100):
    x += datetime.timedelta(days=1) #sonraki gün belirlenmesi
    new={'Günler':x.strftime("%b %d"),'Hasta':df.iloc[:,1].rolling(window=7).mean().iloc[-1:]} #sonraki hasta sayısını tahmin etmek için hareketli ortalamayı buluyoruz
    new=pd.DataFrame(new)
    print(new)
    df=df.append(new,ignore_index = True,sort=False)

df_adf_test=df.iloc[:100,1].copy()
X = df_adf_test
result = adfuller(X)
print("\n"+'ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


toplam=0
for i in range(0,100):
    toplam+=df.iloc[100+i,1].item()
    if(toplam > data.iloc[-1,6].item()):
        print("\n"+str(df.iloc[100+i,0]) + " günü hasta sayısı toplamı: "+str(toplam)+" yatak kapasitesi: "+str(data.iloc[-1,6])+" aşar.")
        break

plt.plot(df_copy.iloc[:,0], df_copy.iloc[:,1], label = "Sonraki 50 günün Gerçek Değeri")
plt.plot(df_copy.iloc[:,0], df_copy.iloc[:,2], label = "Sonraki 50 günün Tahmini Değeri")
plt.xticks(rotation=45,size=6)
plt.xlabel('Günler') 
plt.ylabel('Hasta Sayısı')
plt.legend() 
plt.show()
