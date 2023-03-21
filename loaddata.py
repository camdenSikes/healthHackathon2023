import pandas as pd
import math
from matplotlib import pyplot as plt

class DataHolder:
    #In provided dataset, qualmeas.xlsx
    #Adolescent Mental Health and/or Depression Screening
    adscreen = None
    adscreenDenom = None
    #Depression PHQ-9 Utilization Adol
    adPHQ = None
    adPhQDenom = None
    #Optimal Asthma Control Children
    adasthma = None
    adasthmaDenom = None

    #In incomedata.csv
    totHouse = 0
    medIncome = 0
    meanIncome = 0

    def __init__(self) -> None:
        self.adscreen = 0
        self.adscreenDenom = 0
        self.adPHQ = 0
        self.adPHQDenom = 0
        self.adasthma = 0
        self.adasthmaDenom = 0
        self.totHouse = 0
        self.medIncome = 0
        self.meanIncome = 0

    def updateAdscreen(self, rate, denom):
        newDenom = self.adscreenDenom + denom
        self.adscreen = (self.adscreen*self.adscreenDenom + rate*denom)/newDenom
        self.adscreenDenom = newDenom

    def updatePHQ(self, rate, denom):
        newDenom = self.adPHQDenom + denom
        self.adPHQ = (self.adPHQ*self.adPHQDenom + rate*denom)/newDenom
        self.adPHQDenom = newDenom

    def updateAsthma(self, rate, denom):
        newDenom = self.adasthmaDenom + denom
        self.adasthma = (self.adasthma*self.adasthmaDenom + rate*denom)/newDenom
        self.adasthmaDenom = newDenom


    def setIncome(self,totHouse,medIncome,meanIncome):
        self.totHouse = totHouse
        self.medIncome = medIncome
        self.meanIncome = meanIncome

totaldh2018 = DataHolder()
totaldh2021 = DataHolder()

zipdict2018 = dict()
zipdict2021 = dict()

df = pd.read_excel(r"C:\\Users\\gcdas\\Git\\healthHackathon2023\\qualmeas.xlsx",1)
for row in df.index:
    measure = df.loc[row,"Measure Name"]
    zip = df.loc[row,"Clinic Zip Code"]
    year = df.loc[row,'Measurement Year']
    if measure == "Adolescent Mental Health and/or Depression Screening":
        rate = df.loc[row,"Actual Rate"]
        denom = df.loc[row,"Denominator"]
        if year == 2021:
            totaldh2021.updateAdscreen(rate,denom)
            if not math.isnan(zip):
                if zip not in zipdict2021:
                    zipdict2021[zip] = DataHolder()
                zipdict2021[zip].updateAdscreen(rate,denom)
        else:
            totaldh2018.updateAdscreen(rate,denom)
            if not math.isnan(zip):
                if zip not in zipdict2018:
                    zipdict2018[zip] = DataHolder()
                zipdict2018[zip].updateAdscreen(rate,denom)

    elif measure == "Depression PHQ-9 Utilization Adol":
        rate = df.loc[row,"Actual Rate"]
        denom = df.loc[row,"Denominator"]
        if year == 2021:
            totaldh2021.updatePHQ(rate,denom)
            if not math.isnan(zip):
                if zip not in zipdict2021:
                    zipdict2021[zip] = DataHolder()
                zipdict2021[zip].updatePHQ(rate,denom)
        else:
            totaldh2018.updatePHQ(rate,denom)
            if not math.isnan(zip):
                if zip not in zipdict2018:
                    zipdict2018[zip] = DataHolder()
                zipdict2018[zip].updatePHQ(rate,denom)


df = pd.read_excel(r"C:\\Users\\gcdas\\Git\\healthHackathon2023\\qualmeas.xlsx",0)
for row in df.index:
    measure = df.loc[row,"Measure Name"]
    zip = df.loc[row,"Clinic Zip Code"]
    year = df.loc[row,'Measurement Year']
    if measure == "Optimal Asthma Control Children":
        rate = df.loc[row,"Actual Rate"]
        denom = df.loc[row,"Denominator"]
        if year == 2021:
            totaldh2021.updateAsthma(rate,denom)
            if not math.isnan(zip):
                if zip not in zipdict2021:
                    zipdict2021[zip] = DataHolder()
                zipdict2021[zip].updateAsthma(rate,denom)
        else:
            totaldh2018.updateAsthma(rate,denom)
            if not math.isnan(zip):
                if zip not in zipdict2018:
                    zipdict2018[zip] = DataHolder()
                zipdict2018[zip].updateAsthma(rate,denom)

incomedf = pd.read_csv(r"incomedata.csv")
sumtotHouse2018 = 0
summedIncome2018 = 0
summeanIncome2018 = 0
sumtotHouse2021 = 0
summedIncome2021 = 0
summeanIncome2021 = 0
for row in incomedf.index:
    zip = incomedf.loc[row,"Geographic Area Name"]
    totHouse = incomedf.loc[row,"Total Households"]
    medIncome = int(incomedf.loc[row,"Median income"])
    meanIncome = int(incomedf.loc[row,"Mean income"])
    if zip in zipdict2018:
        zipdict2018[zip].setIncome(totHouse,medIncome,meanIncome)
        sumtotHouse2018 = sumtotHouse2018 + totHouse
        summedIncome2018 = summedIncome2018 + medIncome*totHouse
        summeanIncome2018 = summeanIncome2018 + meanIncome*totHouse
    if zip in zipdict2021:
        zipdict2021[zip].setIncome(totHouse,medIncome,meanIncome)
        sumtotHouse2021 = sumtotHouse2021 + totHouse
        summedIncome2021 = summedIncome2021 + medIncome*totHouse
        summeanIncome2021 = summeanIncome2021 + meanIncome*totHouse
totaldh2018.setIncome(sumtotHouse2018,summedIncome2018/sumtotHouse2018,summeanIncome2018/sumtotHouse2018)
totaldh2021.setIncome(sumtotHouse2021,summedIncome2021/sumtotHouse2021,summeanIncome2021/sumtotHouse2021)

## plot med income vs screen for both years
# medIncome2018 = []
# adscreen2018 = []
# for zip,dh in zipdict2018.items():
#     if(dh.medIncome != 0):
#         medIncome2018.append(dh.medIncome)
#         adscreen2018.append(dh.adscreen)
# plt.plot(medIncome2018,adscreen2018,'ro')

# medIncome2021 = []
# adscreen2021 = []
# for zip,dh in zipdict2021.items():
#     if(dh.medIncome != 0):
#         medIncome2021.append(dh.medIncome)
#         adscreen2021.append(dh.adscreen)
# plt.plot(medIncome2021,adscreen2021,'bo')

#Plot med income vs. change in phq util
medIncome = []
deltascreen = []
for zip,dh in zipdict2018.items():
     if(dh.medIncome != 0) and zip in zipdict2021 and dh.adPHQDenom != 0 and zipdict2021[zip].adPHQDenom != 0:
         medIncome.append(dh.medIncome)
         deltascreen.append(zipdict2021[zip].adPHQ - dh.adPHQ)
plt.plot(medIncome,deltascreen,'ro')

plt.show()

#Plot med income vs. change in asthma
medIncome = []
deltascreen = []
for zip,dh in zipdict2018.items():
     if(dh.medIncome != 0) and zip in zipdict2021 and dh.adasthmaDenom != 0 and zipdict2021[zip].adasthmaDenom != 0:
         medIncome.append(dh.medIncome)
         deltascreen.append(zipdict2021[zip].adasthma - dh.adasthma)
plt.plot(medIncome,deltascreen,'ro')

plt.show()






print("hi")