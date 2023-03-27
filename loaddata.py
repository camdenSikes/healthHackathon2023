import pandas as pd
import math
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

INFRATE = 1.06

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

    #In provided datset, cost.xlsx
    #Children TCOC
    ctcoc = None
    costMedGrp = None
    #Inpatient Admission Ratio
    inRat = None
    #ER Visits Ratio
    erRat = None
    #Primary Care Visits Ratio
    pcRat = None

    #In incomedata.csv
    totHouse = 0
    medIncome = 0
    meanIncome = 0

    #In ruralzip.xlsx
    isRural = False

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
        self.ctcoc = []
        self.costMedGrp = []
        self.inRat = []
        self.erRat = []
        self.pcRat = []
        self.isRural = False

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


df = pd.read_excel(r"C:\\Users\\gcdas\\Git\\healthHackathon2023\\cost.xlsx",0)
for row in df.index:
    year = df.loc[row,'Measurement Year']
    ctcoc = df.loc[row,'Children TCOC']
    medGrp = df.loc[row, 'Medical Group Name']
    inRat = df.loc[row, 'Inpatient Admission Ratio']
    erRat = df.loc[row, 'ER Visits Ratio']
    pcRat = df.loc[row, 'Primary Care Visits Ratio']
    if math.isnan(ctcoc):
        continue
    if year == 2021:
        totaldh2021.ctcoc.append(ctcoc)
        totaldh2021.costMedGrp.append(medGrp)
        totaldh2021.inRat.append(inRat)
        totaldh2021.erRat.append(erRat)
        totaldh2021.pcRat.append(pcRat)
    else:
        totaldh2018.ctcoc.append(ctcoc)
        totaldh2018.costMedGrp.append(medGrp)
        totaldh2018.inRat.append(inRat)
        totaldh2018.erRat.append(erRat)
        totaldh2018.pcRat.append(pcRat)


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

ruraldf = pd.read_excel(r"ruralzip.xlsx",1)
for row in ruraldf.index:
    zip = ruraldf.loc[row,'ZIP_CODE']
    ruca = ruraldf.loc[row,'RUCA1']
    if zip in zipdict2018:
        zipdict2018[zip].isRural = (ruca>3)


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

# #Plot med income vs. change in phq util
# medIncome = []
# deltascreen = []
# for zip,dh in zipdict2018.items():
#      if(dh.medIncome != 0) and zip in zipdict2021 and dh.adPHQDenom != 0 and zipdict2021[zip].adPHQDenom != 0:
#          medIncome.append(dh.medIncome)
#          deltascreen.append(zipdict2021[zip].adPHQ - dh.adPHQ)
# plt.plot(medIncome,deltascreen,'ro')
# plt.show()


# #Look at changes in various cost measures
# deltatcoc = []
# deltain = []
# deltaer = []
# deltapc = []
# for i,place in enumerate(totaldh2018.costMedGrp):
#     if place not in totaldh2021.costMedGrp:
#         continue
#     ind = totaldh2021.costMedGrp.index(place)
#     deltatcoc.append(totaldh2021.ctcoc[ind] - totaldh2018.ctcoc[i]*INFRATE)
#     deltain.append(totaldh2021.inRat[ind] - totaldh2018.inRat[i])
#     deltaer.append(totaldh2021.erRat[ind] - totaldh2018.erRat[i])
#     deltapc.append(totaldh2021.pcRat[ind] - totaldh2018.pcRat[i])
#
# plt.violinplot(deltatcoc)
# plt.axhline()
# plt.tick_params('x',which='both',top=False,bottom=False,labelbottom=False)
# plt.title("Change in Children's Total Cost of Care")
# plt.ylabel("Change in Cost (dollars)")
# plt.show()
# plt.violinplot(deltapc)
# plt.axhline()
# plt.tick_params('x',which='both',top=False,bottom=False,labelbottom=False)
# plt.title("Change in Primary Care Visits Ratio")
# plt.ylabel("Change in Ratio")
# plt.show()
# print(stats.ttest_1samp(deltatcoc,0))
# print(stats.ttest_1samp(deltain,0))
# print(stats.ttest_1samp(deltaer,0))
# print(stats.ttest_1samp(deltapc,0))

# #Plot med income vs. change in asthma
# medIncome = []
# meanIncome = []
# deltaasthma = []
# asthma = []
# for zip,dh in zipdict2018.items():
#      if(dh.medIncome != 0) and zip in zipdict2021 and dh.adasthmaDenom != 0 and zipdict2021[zip].adasthmaDenom != 0:
#          medIncome.append(dh.medIncome)
#          meanIncome.append(dh.meanIncome)
#          deltaasthma.append(zipdict2021[zip].adasthma - dh.adasthma)
#          asthma.append(dh.adasthma)
# plt.violinplot(deltaasthma)
# plt.axhline()
# plt.tick_params('x',which='both',top=False,bottom=False,labelbottom=False)
# plt.title("Change in Optimal Asthma Control in Children")
# plt.ylabel("Change in Proportion")
# plt.show()
# print(stats.ttest_1samp(deltaasthma,0))
# y = np.array(asthma)
# x = np.array(medIncome)
# A = np.vstack([x, np.ones(len(x))]).T
# alpha = np.linalg.lstsq(A,y)
# slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# plt.plot(medIncome,asthma,'b.')
# plt.plot(x,slope*x + intercept,'r')
# plt.title("Optimal Asthma Control in Children vs. Median Income by ZIP Code")
# plt.xlabel("Median Household Income (dollars)")
# plt.ylabel("Proportion of Children with Optimal Asthma Control")
# plt.show()
# print("r^2 =" + str(r_value**2))

#Plot asthma rural vs urban
deltaasthmaUrb = []
asthmaUrb = []
deltaasthmaRur = []
asthmaRur = []
for zip,dh in zipdict2018.items():
    if zip in zipdict2021 and dh.adasthmaDenom != 0 and zipdict2021[zip].adasthmaDenom != 0:
        if(zipdict2018[zip].isRural):
            deltaasthmaRur.append(zipdict2021[zip].adasthma - dh.adasthma)
            asthmaRur.append(dh.adasthma)
        else:
            deltaasthmaUrb.append(zipdict2021[zip].adasthma - dh.adasthma)
            asthmaUrb.append(dh.adasthma)
print(stats.ttest_ind(deltaasthmaRur,deltaasthmaUrb))
plt.violinplot([asthmaUrb,asthmaRur],showmedians=True)
plt.xticks([1,2],["Urban","Rural"])
plt.title("Distributions of Children's Optimal Asthma Control at Urban and Rural Clinics")
plt.ylabel("Proportion of Children with Optmal Asthma Control")
plt.show()
print(stats.ttest_ind(asthmaRur,asthmaUrb))









print("hi")