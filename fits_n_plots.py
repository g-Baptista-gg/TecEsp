import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from lmfit import Model
import scienceplots

import matplotlib.cm as cm
from matplotlib.offsetbox import AnchoredText
from matplotlib.collections import PolyCollection


#____________AVISO: TEMOS QUE FAZER OS FITS EM CANAIS POR CAUSA DAS INTENSIDADES____________#
#__________________________OU ARRANJAR MANEIRA DE CONVERTER EM EN__________________________#

def polygon_under_graph(xlist, ylist):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (xlist, ylist) line graph.  Assumes the xs are in ascending order.
    """
    return [(xlist[0], 0.), *zip(xlist, ylist), (xlist[-1], 0.)]



vol = [0,20,40,150,200,300,500]

fig0,ax0 = plt.subplots(1,1,subplot_kw={'projection': '3d'})
verts=[]
ys=[]
facecolors = plt.colormaps['viridis_r'](np.linspace(0, 1, len(vol)))
cc=0
for i in vol[::-1]:
    df=np.array(pd.read_csv('s_brem/'+str(i)+'.csv'))
    ax0.plot(df[120:-3000,0],i*np.ones(len(df[120:-3000,0])),df[120:-3000,1],label=str(i)+' $\mu$L',color=facecolors[cc])
    ax0.add_collection3d(plt.fill_between(df[120:-3000,0],df[120:-3000,1],0,color=facecolors[cc], alpha=0.2,label="filled plot"),i, zdir='y')
    cc+=1

ax0.set_xlabel('Energy (keV)')
ax0.set_ylabel('Deposited Volume ($\mu$L)')
ax0.set_zlabel('Counts')
#ax0.legend()
fig0.tight_layout()
fig0.savefig('3D_s_brem.pdf',dpi=300)

plt.style.use(['science','nature'])

def en_to_sig(en):
    return 0.00412*en+0.0355

def gaussian(x,amp,cen,sig):
    return amp * np.exp(-(x-cen)**2 / (2*sig**2))
def lin_func(x,a,b):
    return a*x+b

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
        params[elements[i]+'_beta_amp'].set(min=0,value=0.10*params[elements[i]+'_alpha_amp'].value)
    
    #print(params.pretty_print())
    result=total_model.fit(data=df[:,1],params=params,x=df[:,0])
    ax1.set_xlabel('Energy (keV)')
    ax1.set_ylabel('Counts')
    #fig1.suptitle(str(volume)+' $\mu$L')
    colors = cm.gist_ncar(np.linspace(0, 1, len(elements)+3))
    ax1.plot(df[:,0],result.best_fit,label='Fit',color='k')

    cj=0
    for i in elements:
        ma=result.params[i+'_alpha_cen'].value
        mb=result.params[i+'_beta_cen'].value
        aa=result.params[i+'_alpha_amp'].value
        ab=result.params[i+'_beta_amp'].value
        sa=result.params[i+'_alpha_sig'].value
        sb=result.params[i+'_beta_sig'].value
        color = next(ax1._get_lines.prop_cycler)['color']
        ax1.plot(df[:,0],gaussian(df[:,0],aa,ma,sa),'-.',label= i,c=colors[cj])
        ax1.plot(df[:,0],gaussian(df[:,0],ab,mb,sb),'-.',c=colors[cj])
        cj+=1


    plt.tight_layout()
    ax1.legend()
    fig1.savefig('spectra/'+str(volume)+'uL.pdf',dpi=300)
    #print(result.fit_report())
    return result.params


fit_res=[]
for i in [0,20,40,150,200,300,500]:
    fit_res.append(fitdata(i))

elements0=['Ca','Ti','Cr','Fe','Ni','Cu','Zn']
elements=['Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn']



a=['45','51','61','64' ,'62','61','53','52']
au=['3','3' ,'4' ,'3'  ,'4' ,'3' ,'3' ,'3']
b=['3' ,'11','0' ,'$5$','-1','0','1','16']
bu=['5','5','5','3','5','3','2','3']
bnot=['$\cdot 10$','','$\cdot 10$','$\cdot 10$','$\cdot 10$','$\cdot 10$','$\cdot 10$','$\cdot 10$']


fig2,ax2=plt.subplots(1,1)
colors = cm.jet(np.linspace(0, 1, len(elements)+2))
for i in range(len(elements)):
    if elements[i] not in ['Ca','Sc','Ti']:
        intensity=[]
        intensity_unc=[]
        if elements[i] in elements0:
            quantity=[0,20,40,150,200,300,500]
        else:
            quantity=[20,40,150,200,300,500]

        for j in range(len(quantity)):

            if elements[i] in elements0:
                intensity.append(np.sqrt(2*np.pi)*fit_res[j][elements[i]+'_alpha_amp'].value*fit_res[j][elements[i]+'_alpha_sig'].value)
                intensity_unc.append(np.sqrt(2*np.pi)*fit_res[j][elements[i]+'_alpha_amp'].stderr*fit_res[j][elements[i]+'_alpha_sig'])
            else:
                intensity.append(np.sqrt(2*np.pi)*fit_res[j+1][elements[i]+'_alpha_amp'].value*fit_res[j+1][elements[i]+'_alpha_sig'].value)
                intensity_unc.append(np.sqrt(2*np.pi)*fit_res[j+1][elements[i]+'_alpha_amp'].stderr*fit_res[j+1][elements[i]+'_alpha_sig'])
        #ax2.plot(quantity,intensity,'.',label=elements[i],color=colors[i])
        quantity=np.array(quantity)*0.1
        intensity=np.array(intensity)/(20*60)
        intensity_unc=np.array(intensity_unc)/(20*60)
        ax2.errorbar(quantity,intensity,yerr=intensity_unc,xerr=0.05*quantity,color=colors[i],linestyle='',fmt='.',capsize=1,label=elements[i])
    
        linear_Mod=Model(lin_func)
        lin_par=linear_Mod.make_params()
        lin_par['a'].set(value=50)
        lin_par['b'].set(value=0)
        result=linear_Mod.fit(data=intensity,x=quantity,params=lin_par,weights=1/np.sqrt(intensity_unc**2 +0*(0.05*quantity)**2))
        #print('-----------'+elements[i]+'-----------------')
        print(result.fit_report())
        ax2.plot(quantity,result.best_fit,color=colors[i],linestyle=':')
        print('AQUI')
ax2.legend()
ax2.set_xlabel('Quantity ($\mu$g)')
ax2.set_ylabel(r'K$_\alpha$ counts /s')
#ax2.add_artist(AnchoredText("$y=a\cdot x +b$\n $a=$"+a.pop(0)+'$\pm$'+au.pop(0)+'\n$b=$('+b.pop(0)+'$\pm$'+bu.pop(0)+')'+bnot.pop(0), loc=7))
fig2.tight_layout()
fig2.savefig('calibration_curves/all_elements.pdf',dpi=300)


#COISAS A FAZER: METER CONTAGENS/AREA/TEMPO
#plt.show()