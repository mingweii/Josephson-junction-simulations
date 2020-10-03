### extract Ic and peak heights of a dVdI vs bias current sweep
## Input: IDC_array, DVDI_array
## Return: Icn, Icp, peak_n, peak_p
# function: extract_Ic(IDC_array,DVDI_array,d,h)
# recursively find exactly 2 peaks in the dV/dI curve based on initial guess of peak distance d and peak height h
# Set Ic minus as zero if only one Ic is found
# Set both Ic minus and Ic plus as zeros if no Ic is found.

from scipy.signal import find_peaks
import numpy as np
def extract_Ic(IDC_array,DVDI_array,d=1,h=0,num_Ic=2):
    Icn=-IDC_array[np.argmax(DVDI_array[IDC_array<0])]
    Icp=IDC_array[len(IDC_array)//2+np.argmax(DVDI_array[IDC_array>=0])]
    return Icn,Icp



#    grad=DVDI_array#np.abs(np.gradient(DVDI_array)) # find the sharpest step
#    w=5

#    index_ic, _ =find_peaks(grad,distance=d,height=h,width=w,threshold=10)
#    if num_Ic==2:
#        nrecursion=10000
#        while len(index_ic)!=2 and nrecursion>0:
#            nrecursion=nrecursion-1
#            if len(index_ic)>2:
#                if nrecursion%3==0: d=d+1
#                elif nrecursion%3==1: w=w+1
#                else: h=h*1.02
#            else:
#                if nrecursion%3==0 and d>1: d=d-1
#                elif nrecursion%3==1 and w>1: w=w-1
#                else: h=h*0.98
#            index_ic, _ =find_peaks(grad,distance=d,height=h,width=w)
#        if len(index_ic)==2:
#            return np.abs(IDC_array[index_ic[0]]), np.abs(IDC_array[index_ic[1]])
#        else:
#            print("Cannot find exactly two peaks within 10000 recursions")
#            if len(index_ic)==1:
#                print("Only find one peak within 10000 recursions")
#                return 0, np.abs(IDC_array[index_ic[0]])
#            else:
#                print("Find no peak within 10000 recursions")
#                return 0,0
#    elif num_Ic==1:
#        nrecursion=1000
#        while len(index_ic)!=1 and nrecursion>0:
#            nrecursion=nrecursion-1
#            if len(index_ic)>1:
#                index_ic, _ =find_peaks(grad,distance=d+1,height=h*1.02)
#            else:
#                index_ic, _ =find_peaks(grad,distance=d-1,height=h*0.98)
#        if len(index_ic)==1:
#            return np.abs(IDC_array[index_ic[0]])
#        else:
#            print("Cannot find exactly one peak within 1000 recursions,try another guesses of d and h.")
#            return 0
#    else:
#        print("the valid number of Ic can only be 1 or 2.")



def extract_height(IDC_array,DVDI_array,d,h):
    peak_n=np.max(DVDI_array[IDC_array<0])
    peak_p=np.max(DVDI_array[IDC_array>=0])
    return peak_n,peak_p
#    index_height, _ = find_peaks(DVDI_array,distance=d,height=h)
#    nrecursion=1000
#    while len(index_height)!=2 and nrecursion>0:
#        nrecursion=nrecursion-1
#        if len(index_height)>2:
#            index_height, _ =find_peaks(DVDI_array,distance=d+1,height=h*1.02)
#
#        elif len(index_height)==1:
#            index_height, _ =find_peaks(DVDI_array,distance=d-1,height=h)
#        else:
#            index_height, _ =find_peaks(DVDI_array,distance=d-1,height=h*0.98)
#    if len(index_height)==2:
#        return np.abs(DVDI_array[index_height[0]]), np.abs(DVDI_array[index_height[1]])
#    else:
#        print("Cannot find exactly two peaks within 1000 recursions")
#        if len(index_height)==1:
#            return 0, np.abs(DVDI_array[index_height[0]])
#        else:
#            return 0,0
