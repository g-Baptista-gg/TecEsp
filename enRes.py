import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import scienceplots

elements=['Al','Mo','Ni','Ti','Zn']
alphas=[1.486,17.480,7.480,4.512,8.637]
mpos=[200,1600,800,500,900]
Mpos=[-3800,-2100,-3200,-3525,-3100]
resolutions=[]
res_unc=[]


def gaussian(x,amp,cen,sig):
    return amp * np.exp(-(x-cen)**2 / (2*sig**2))

fit_mod=Model(gaussian)
params_gauss=fit_mod.make_params()
params_gauss['amp'].set(min=0,value=10000)
params_gauss['sig'].set(min=0,value=0.01,max=10)
print(params_gauss.pretty_print())
for i in range(len(elements)):
    df=np.array(pd.read_csv('res_spec/'+elements[i]+'.csv'))
    params_gauss['cen'].set(value=alphas[i])
    result=fit_mod.fit(df[mpos[i]:Mpos[i],1],params=params_gauss,x=df[mpos[i]:Mpos[i],0])
    print(result.fit_report())
    fig,ax=plt.subplots(1,1)
    ax.plot(df[mpos[i]:Mpos[i],0],result.best_fit,label='Fit')
    ax.plot(df[mpos[i]:Mpos[i],0],df[mpos[i]:Mpos[i],1],label='Data')
    fig.suptitle(elements[i]+' '+str(result.params['sig']*2.35))
    resolutions.append(result.params['sig'].value)
    res_unc.append(result.params['sig'].stderr)
    ax.legend()

fig,ax=plt.subplots(1,1)

def linear_res(x,dec,inter):
    return dec*x+inter


lin_Mod=Model(linear_res)
param_lin = lin_Mod.make_params()
print(param_lin.pretty_print())
param_lin['dec'].set(min=0,value=0.5)
param_lin['inter'].set(value=0)



result =lin_Mod.fit(resolutions,params=param_lin,x=alphas)
print(result.fit_report())
ax.plot(alphas,result.best_fit)
ax.plot(alphas,resolutions,'.')

plt.show()