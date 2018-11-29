import pandas as pd
from random import randint
pd.options.display.max_rows = None



def fum1(maxPower):
    return randint(0,maxPower)


def fum2(P, reduce):
    return P*reduce


def fum3(P, offset):
    if(P>offset):
        return P-offset
    else:
        return 0


def fu_data(data, failNum=2, minFaulty=4, maxFaulty=7, minBroken=3, maxBroken=5, fum=0, maxPower=7500000, reduce=0.75, offset=10000, test=0):
    data0=data.copy()
    n=failNum
    m=0
    s=len(data0)/n
    
    if test==1: 
        faultyStart=100
        brokenStart=randint(minFaulty*24,maxFaulty*24)+faultyStart
        brokenEnd=randint(minBroken*24,maxBroken*24)+brokenStart
        
        m=m+1

        i=0
        if (fum==0):
            method=randint(1,3)
        else:
            method=fum
            
        print("Starting {} iteration of faults. Fault starts at {};".format(m, faultyStart))
        print("the engine breaks at {} and is repaired at {}. Fault type was {}".format(brokenStart, brokenEnd,method))
        
        for p in data0['output_power']:
            i=i+1
            if ((i>faultyStart)&(i<brokenStart)):
                if method==1:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum1(maxPower)
                elif method==2:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum2(p,reduce)
                elif method==3:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum3(p, offset)
                data0.iloc[i, data0.columns.get_loc('state')] = 'f'
            elif ((i>=brokenStart)&(i<brokenEnd)):
                data0.iloc[i, data0.columns.get_loc('output_power')] = 0
                data0.iloc[i, data0.columns.get_loc('state')] = 'r'
        return data0
    while n>0:
        n=n-1
        faultyStart=randint(300+m*s,len(data0)-s*n-300)
        brokenStart=randint(minFaulty*24,maxFaulty*24)+faultyStart
        brokenEnd=randint(minBroken*24,maxBroken*24)+brokenStart
        
        m=m+1

        i=0
        if (fum==0):
            method=randint(1,3)
        else:
            method=fum
            
        print("Starting {} iteration of faults. Fault starts at {};".format(m, faultyStart))
        print("the engine breaks at {} and is repaired at {}. Fault type was {}".format(brokenStart, brokenEnd,method))
        
        for p in data0['output_power']:
            i=i+1
            if ((i>faultyStart)&(i<brokenStart)):
                if method==1:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum1(maxPower)
                    data0.iloc[i, data0.columns.get_loc('state')] = 'f'
                elif method==2:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum2(p,reduce)
                    data0.iloc[i, data0.columns.get_loc('state')] = 'f'
                elif method==3:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum3(p, offset)
                    data0.iloc[i, data0.columns.get_loc('state')] = 'f'
            elif ((i>=brokenStart)&(i<brokenEnd)):
                data0.iloc[i, data0.columns.get_loc('output_power')] = 0
                data0.iloc[i, data0.columns.get_loc('state')] = 'r'
    return data0
    
    
def fault_detected (data, dataR, posDet, repairTime=3):
    dataF=data.copy()
    gen = (i for i,x in enumerate(dataF['output_power']) if ((i>=posDet)&(i<posDet+24*repairTime)))
    for i in gen:
        dataF.iloc[i, dataF.columns.get_loc('output_power')] = 0
        dataF.iloc[i, dataF.columns.get_loc('state')] = 'r'
    i=0
    for s in dataF['state']:
        if i >= posDet + repairTime * 24:
            if s != 'w':
                dataF.iloc[i, dataF.columns.get_loc('output_power')] = dataR.iloc[i, dataR.columns.get_loc('output_power')]
                dataF.iloc[i, dataF.columns.get_loc('state')] = 'w'
            else:
                return dataF
        i=i+1
    return dataF


def server_error (data, dataR, posDet, repairTime=3):
    dataF=data.copy()
    gen = (i for i,x in enumerate(dataF['output_power']) if ((i>=posDet)&(i<posDet+24*repairTime)))
    for i in gen:
        dataF.iloc[i, dataF.columns.get_loc('output_power')] = 0;
        dataF.iloc[i, dataF.columns.get_loc('state')] = 'r'
    return dataF
