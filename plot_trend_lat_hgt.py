import glob
import xarray as xr
import vartimeproc 
import ensemble_functions
import plot_functions

#********************************************************************************************************
run = 'feedback'
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'U'
alpha = 0.05

#********************************************************************************************************
# presets for paper
runname   = {'rcp85'   : 'RCP8.5',\
             'feedback': 'GEO8.5'}

plotlett  = {'U'       :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'}}}

shading   = {'U'       :{'rcp85':(5,0.5), 'feedback':(5,0.5)}}

contours  = {'U'       :{'rcp85':(60,10), 'feedback':(60,10)}}

clabel    = {'U'       :'Zonal mean zonal wind (ms$^{-1}$ per 30 yrs)'}

#********************************************************************************************************
# Control Climatology
print("Calculating climatology for control")

members_control = []
for i in range(1,21):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".201001-*.nc")[0]
   vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2010, tim2=2030, varcode=varcode, zm=True)
   clim = vartimeobj.clim_mean(season)
   members_control.append(clim)

ncontrol = len(members_control)
ensmean_control, ensstd_control = ensemble_functions.stats(members_control)

#********************************************************************************************************
# Calculate trend for each member 
members = []

# RCP8.5
if run=='rcp85':
   print("Calculating trend for RCP8.5")
   for i in [1,2,3]:
      ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".201001-*.nc")[0]
      vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode, zm=True)
      trend = vartimeobj.trend_lat_hgt(season)
      members.append(trend)
# Feedback
elif run=='feedback':
   print("Calculating trend for Feedback")
   for i in range(1,21):
      ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".202001-*.nc")[0]
      vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode, zm=True)
      trend = vartimeobj.trend_lat_hgt(season)
      members.append(trend)

print("...done")

# Ensemble stats
nmembers = len(members)
ensmean, ensstd= ensemble_functions.stats(members) 
ttest = ensemble_functions.t_test_onesample(alpha, ensmean, ensstd, nmembers) 

# Plot ensemble mean
plot_functions.plot_single_lat_hgt(ensmean, ensmean_control,\
                                   plotlett[varcode][run][season]+' '+runname[run],\
                                   outdir+varcode+'_trend_'+run+'_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1], contours[varcode][run][0], contours[varcode][run][1],\
                                   clabel[varcode],\
                                   zsig=ttest)

# Plot members 
'''
plot_functions.plot_matrix_lat_hgt(members, ensmean_control,\
                                   '',\
                                   outdir+varcode+'_trend_'+run+'_members_'+season+'.png',\
                                   shading[run][varcode][0], shading[run][varcode][1], contours[run][varcode][0], contours[run][varcode][1],\
                                   clabel[varcode])
'''

#********************************************************************************************************
# END
#********************************************************************************************************

'''
t = xr.open_dataset('xrToE_Ts_trend_2stdev.nc')
#t = t.where(ttest_feedback==0)
plot_functions.plot_ToE(t.__xarray_dataarray_variable__,'ToE','ToE_Ts_trend_2stdev.png',2020,2095,5,'year')

t = xr.open_dataset('xrToE_Ts_clim_2stdev_stdcontrol.nc')
print(t.__xarray_dataarray_variable__[0,:])
plot_functions.plot_ToE(t.__xarray_dataarray_variable__,'ToE','ToE_2stdev_stdcontrol.png',2020,2095,5,'year')
#plot_functions.plot_ToE(t.__xarray_dataarray_variable__[:,:,-1],'ToE','ToE_2stdev_stdcontrol.png',0,1,0.1,'year')
'''

#********************************************************************************************************