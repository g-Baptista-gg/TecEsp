import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from lmfit import Model
import scienceplots
plt.style.use(['science','nature'])


#____________AVISO: TEMOS QUE FAZER OS FITS EM CANAIS POR CAUSA DAS INTENSIDADES____________#
#__________________________OU ARRANJAR MANEIRA DE CONVERTER EM EN__________________________#


vol = [0,20,40,150,200,300,500]

fig0,ax0 = plt.subplots(1,1,subplot_kw={'projection': '3d'})
for i in vol:
    df=np.array(pd.read_csv('s_brem/'+str(i)+'.csv'))
    ax0.plot(df[120:-1500,0],i*np.ones(len(df[120:-1500,0])),df[120:-1500,1],label=str(i)+' $\mu$L')
ax0.legend()
fig0.tight_layout()

def en_to_sig(en):
    return 0.00412*en+0.0355

def gaussian(x,amp,cen,sig):
    return amp * np.exp(-(x-cen)**2 / (2*sig**2))

volume = 200
def fitdata(volume):
    df=np.array(pd.read_csv('s_brem/'+str(volume)+'.csv'))
    for i in range(len(df)):
        if df[i,1]<=0:
            df[i,1]=0

    df=df[340:-3000]
    fig1,ax1=plt.subplots(1,1)
    ax1.plot(df[:,0],df[:,1],label=str(volume)+' $\mu$L')

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
        elements=['Ca','Ti','Cr','Fe','Ni','Cu','Zn']
        alphas=[3.692,4.512,5.415,6.405,7.480,8.046,8.637]
        betas= [4.013,4.933,5.947,7.059,8.267,8.904,9.570]
    else:
        total_model=Ca_model+Sc_model+Ti_model+V_model+Cr_model+Mn_model+Fe_model+Co_model+Ni_model+Cu_model+Zn_model
        elements=['Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn']
        alphas=[3.692,4.093,4.512,4.953,5.415,5.900,6.405,6.931,7.480,8.046,8.637]
        betas= [4.013,4.464,4.933,5.428,5.947,6.492,7.059,7.649,8.267,8.904,9.570]
    params = total_model.make_params()

    for i in range(len(elements)):
        params[elements[i]+'_alpha_cen'].set(value=alphas[i],vary=False)
        params[elements[i]+'_beta_cen'].set(value=betas[i],vary=False)
        params[elements[i]+'_alpha_sig'].set(value=en_to_sig(params[elements[i]+'_alpha_cen'].value),vary=False)
        params[elements[i]+'_beta_sig'].set(value=en_to_sig(params[elements[i]+'_beta_cen'].value),vary=False)
        params[elements[i]+'_alpha_amp'].set(min=0,value=1000)
        params[elements[i]+'_beta_amp'].set(value=params[elements[i]+'_alpha_amp'].value)
    
    #print(params.pretty_print())
    result=total_model.fit(data=df[:,1],params=params,x=df[:,0])
    ax1.set_xlabel('Energy (keV)')
    ax1.set_ylabel('Counts')
    #fig1.suptitle(str(volume)+' $\mu$L')
    ax1.plot(df[:,0],result.best_fit,label='Fit')
    plt.tight_layout()
    ax1.legend()
    fig1.savefig(str(volume)+'uL.pdf',dpi=300)
    print(result.fit_report())

for i in [0,20,40,150,200,300,500]:
    fitdata(i)



plt.show()