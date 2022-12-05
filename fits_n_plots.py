import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from lmfit import Model
import scienceplots
#plt.style.use(['science','nature'])


#____________AVISO: TEMOS QUE FAZER OS FITS EM CANAIS POR CAUSA DAS INTENSIDADES____________#
#__________________________OU ARRANJAR MANEIRA DE CONVERTER EM EN__________________________#


vol = [0,20,40,150,200,300,500]

fig0,ax0 = plt.subplots(1,1,subplot_kw={'projection': '3d'})
for i in vol:
    df=np.array(pd.read_csv('s_brem/'+str(i)+'.csv'))
    ax0.plot(df[120:-1500,0],i*np.ones(len(df[120:-1500,0])),df[120:-1500,1],label=str(i)+' $\mu$L')
ax0.legend()



def gaussian(x,amp,cen,wid):
    return amp * np.exp(-(x-cen)**2 / wid)
def linmod(x,a,b,c):
    return a*x**2 +b*x+c

volume = 200
def fitdata(volume):
    df=np.array(pd.read_csv('s_brem/'+str(volume)+'.csv'))
    for i in range(len(df)):
        if df[i,1]<=0:
            df[i,1]=0


    fig1,ax1=plt.subplots(1,1)
    ax1.plot(df[340:-2900,0],df[340:-2900,1],label=str(i)+' $\mu$L')

    Ca_model=Model(gaussian,prefix='Ca_alpha_')+Model(gaussian,prefix='Ca_beta_')
    Sc_model=Model(gaussian,prefix='Sc_alpha_')+Model(gaussian,prefix='Sc_beta_')
    Ti_model=Model(gaussian,prefix='Ti_alpha_')+Model(gaussian,prefix='Ti_beta_')
    V_model=Model(gaussian,prefix='V_alpha_')+Model(gaussian,prefix='V_beta_')
    Cr_model=Model(gaussian,prefix='Cr_alpha_')+Model(gaussian,prefix='Cr_beta_')
    Mn_model=Model(gaussian,prefix='Mn_alpha_')+Model(gaussian,prefix='Mn_beta_')
    Fe_model=Model(gaussian,prefix='Fe_alpha_')+Model(gaussian,prefix='Fe_beta_')
    Co_model=Model(gaussian,prefix='Co_alpha_')+Model(gaussian,prefix='Co_beta_')
    Ni_model=Model(gaussian,prefix='Ni_alpha_')+Model(gaussian,prefix='Ni_beta_')
    Cu_model=Model(gaussian,prefix='Cu_alpha_')+Model(gaussian,prefix='Cu_beta_')
    Zn_model=Model(gaussian,prefix='Zn_alpha_')+Model(gaussian,prefix='Zn_beta_')

    if volume==0:
        total_model=Ca_model+Ti_model+Cr_model+Fe_model+Ni_model+Cu_model+Zn_model
    else:
        total_model=Ca_model+Sc_model+Ti_model+V_model+Cr_model+Mn_model+Fe_model+Co_model+Ni_model+Cu_model+Zn_model
    params = total_model.make_params()

    """"
    params['Ca_beta_amp'].set(expr='Ca_alpha_amp*0.01')
    params['Sc_beta_amp'].set(expr='Sc_alpha_amp*0.01')
    params['Ti_beta_amp'].set(expr='Ti_alpha_amp*0.01')
    params['V_beta_amp'].set(expr='V_alpha_amp*0.01')
    params['Mn_beta_amp'].set(expr='Mn_alpha_amp*0.01')
    params['Fe_beta_amp'].set(expr='Fe_alpha_amp*0.01')
    params['Co_beta_amp'].set(expr='Co_alpha_amp*0.01')
    params['Ni_beta_amp'].set(expr='Ni_alpha_amp*0.01')
    params['Cu_beta_amp'].set(expr='Cu_alpha_amp*0.01')
    params['Zn_beta_amp'].set(expr='Zn_alpha_amp*0.01')
    """
    #params['lin_a'].set(value=0)
    #params['lin_b'].set(value=0)
    #params['lin_c'].set(value=0)


    params['Ca_alpha_cen'].set(value=3.692,vary=False)
    params['Ca_beta_cen'].set(value=4.013,vary=False)
    params['Ca_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Ca_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Ca_alpha_amp'].set(min=0,value=1000)
    params['Ca_beta_amp'].set(min=0.1*params['Ca_alpha_amp'].min,max=0.2*params['Ca_alpha_amp'].max,value=0.17*params['Ca_alpha_amp'].value)
    #################################################
    if volume!=0:
        params['Sc_alpha_cen'].set(value=4.093,vary=False)
        params['Sc_beta_cen'].set(value=4.464,vary=False)
        params['Sc_alpha_wid'].set(min=0,value=0.001,max=0.1)
        params['Sc_beta_wid'].set(min=0,value=0.001,max=0.1)
        params['Sc_alpha_amp'].set(min=0,value=1000)
        params['Sc_beta_amp'].set(min=0.1*params['Sc_alpha_amp'].min,max=0.2*params['Sc_alpha_amp'].max,value=0.17*params['Sc_alpha_amp'].value)
    #################################################
    params['Ti_alpha_cen'].set(value=4.512,vary=False)
    params['Ti_beta_cen'].set(value=4.933,vary=False)
    params['Ti_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Ti_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Ti_alpha_amp'].set(min=0,value=10000)
    params['Ti_beta_amp'].set(min=0.1*params['Ti_alpha_amp'].min,max=0.2*params['Ti_alpha_amp'].max,value=0.17*params['Ti_alpha_amp'].value)
    #################################################
    if volume!=0:
        params['V_alpha_cen'].set(value=4.953,vary=False)
        params['V_beta_cen'].set(value=5.428,vary=False)
        params['V_alpha_wid'].set(min=0,value=0.001,max=0.1)
        params['V_beta_wid'].set(min=0,value=0.001,max=0.1)
        params['V_alpha_amp'].set(min=0,value=10000)
        params['V_beta_amp'].set(min=0.1*params['V_alpha_amp'].min,max=0.2*params['V_alpha_amp'].max,value=0.17*params['V_alpha_amp'].value)
    #################################################
    params['Cr_alpha_cen'].set(value=5.415,vary=False)
    params['Cr_beta_cen'].set(value=5.947,vary=False)
    params['Cr_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Cr_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Cr_alpha_amp'].set(min=0,value=10000)
    params['Cr_beta_amp'].set(min=0.1*params['Cr_alpha_amp'].min,max=0.2*params['Cr_alpha_amp'].max,value=0.17*params['Cr_alpha_amp'].value)
    #################################################
    if volume!=0:
        params['Mn_alpha_cen'].set(value=5.900,vary=False)
        params['Mn_beta_cen'].set(value=6.492,vary=False)
        params['Mn_alpha_wid'].set(min=0,value=0.001,max=0.1)
        params['Mn_beta_wid'].set(min=0,value=0.001,max=0.1)
        params['Mn_alpha_amp'].set(min=0,value=10000)
        params['Mn_beta_amp'].set(min=0.1*params['Mn_alpha_amp'].min,max=0.2*params['Mn_alpha_amp'].max,value=0.17*params['Mn_alpha_amp'].value)
    #################################################
    params['Fe_alpha_cen'].set(value=6.405,vary=False)
    params['Fe_beta_cen'].set(value=7.059,vary=False)
    params['Fe_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Fe_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Fe_alpha_amp'].set(min=0,value=10000)
    params['Fe_beta_amp'].set(min=0.1*params['Fe_alpha_amp'].min,max=0.2*params['Fe_alpha_amp'].max,value=0.17*params['Fe_alpha_amp'].value)
    #################################################
    if volume!=0:
        params['Co_alpha_cen'].set(value=6.931,vary=False)
        params['Co_beta_cen'].set(value=7.649,vary=False)
        params['Co_alpha_wid'].set(min=0,value=0.001,max=0.1)
        params['Co_beta_wid'].set(min=0,value=0.001,max=0.1)
        params['Co_alpha_amp'].set(min=0,value=10000)
        params['Co_beta_amp'].set(min=0.1*params['Co_alpha_amp'].min,max=0.2*params['Co_alpha_amp'].max,value=0.17*params['Co_alpha_amp'].value)
    #################################################
    params['Ni_alpha_cen'].set(value=7.480,vary=False)
    params['Ni_beta_cen'].set(value=8.267,vary=False)
    params['Ni_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Ni_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Ni_alpha_amp'].set(min=0,value=10000)
    params['Ni_beta_amp'].set(min=0.1*params['Ni_alpha_amp'].min,max=0.2*params['Ni_alpha_amp'].max,value=0.17*params['Ni_alpha_amp'].value)
    #################################################
    params['Cu_alpha_cen'].set(value=8.046,vary=False)
    params['Cu_beta_cen'].set(value=8.904,vary=False)
    params['Cu_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Cu_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Cu_alpha_amp'].set(min=0,value=10000)
    params['Cu_beta_amp'].set(min=0.1*params['Cu_alpha_amp'].min,max=0.2*params['Cu_alpha_amp'].max,value=0.17*params['Cu_alpha_amp'].value)
    #################################################
    params['Zn_alpha_cen'].set(value=8.637,vary=False)
    params['Zn_beta_cen'].set(value=9.570,vary=False)
    params['Zn_alpha_wid'].set(min=0,value=0.001,max=0.1)
    params['Zn_beta_wid'].set(min=0,value=0.001,max=0.1)
    params['Zn_alpha_amp'].set(min=0,value=10000)
    params['Zn_beta_amp'].set(min=0.1*params['Zn_alpha_amp'].min,max=0.2*params['Zn_alpha_amp'].max,value=0.17*params['Zn_alpha_amp'].value)

    result=total_model.fit(data=df[340:-2900,1],params=params,x=df[340:-2900,0])
    #print(params.pretty_print())

    ax1.set_xlabel('Energy (keV)')
    ax1.set_ylabel('Counts')
    fig1.suptitle(str(volume)+' $\mu$L')
    ax1.plot(df[340:-2900,0],result.best_fit)
    plt.tight_layout()
    fig1.savefig(str(volume)+'uL.pdf',dpi=300)
    print(result.fit_report())

for i in [0,20,40,150,200,300,500]:
    fitdata(i)



plt.show()