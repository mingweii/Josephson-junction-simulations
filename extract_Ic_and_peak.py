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
    grad=np.abs(np.gradient(DVDI_array)) # find the sharpest step

    index_ic, _ =find_peaks(grad,distance=d,height=h)
    if num_Ic==2:
        nrecursion=1000
        while len(index_ic)!=2 and nrecursion>0:
            nrecursion=nrecursion-1
            if len(index_ic)>2:
                index_ic, _ =find_peaks(grad,distance=d+1,height=h*1.02)

            elif len(index_ic)==1:
                index_ic, _ =find_peaks(grad,distance=d-1,height=h)
            else:
                index_ic, _ =find_peaks(grad,distance=d-1,height=h*0.98)
        if len(index_ic)==2:
            return np.abs(IDC_array[index_ic[0]]), np.abs(IDC_array[index_ic[1]])
        else:
            print("Cannot find exactly two peaks within 1000 recursions")
            if len(index_ic)==1:
                return 0, np.abs(IDC_array[index_ic[0]])
            else:
                return 0,0
    elif num_Ic==1:
        nrecursion=1000
        while len(index_ic)!=1 and nrecursion>0:
            nrecursion=nrecursion-1
            if len(index_ic)>1:
                index_ic, _ =find_peaks(grad,distance=d+1,height=h*1.02)
            else:
                index_ic, _ =find_peaks(grad,distance=d-1,height=h*0.98)
        if len(index_ic)==1:
            return np.abs(IDC_array[index_ic[0]])
        else:
            print("Cannot find exactly one peak within 1000 recursions,try another guesses of d and h.")
            return 0
    else:
        print("the valid number of Ic can only be 1 or 2.")



def extract_height(DVDI_array,d,h):

    index_height, _ = find_peaks(DVDI_array,distance=d,height=h)
    nrecursion=1000
    while len(index_height)!=2 and nrecursion>0:
        nrecursion=nrecursion-1
        if len(index_height)>2:
            index_height, _ =find_peaks(DVDI_array,distance=d+1,height=h*1.02)

        elif len(index_height)==1:
            index_height, _ =find_peaks(DVDI_array,distance=d-1,height=h)
        else:
            index_height, _ =find_peaks(DVDI_array,distance=d-1,height=h*0.98)
    if len(index_height)==2:
        return np.abs(DVDI_array[index_height[0]]), np.abs(DVDI_array[index_height[1]])
    else:
        print("Cannot find exactly two peaks within 1000 recursions")
        if len(index_height)==1:
            return 0, np.abs(DVDI_array[index_height[0]])
        else:
            return 0,0
