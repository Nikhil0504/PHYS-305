import math

def IdealGasWorkLH(Vi, Vf, Num):
    # Compute ideal gas work done

    # parameters in cgs units
    N = (16/44) * 6.022e23
    kbT = 4*10**(-14)

    # Step size
    dV = (Vf - Vi) / (Num-1)

    # initialize volume and work
    V = Vi
    Work = 0

    # calculate work done
    for i in range(Num - 1):
        Work = Work + (N * kbT/V) * dV
        V = V + dV
    
    Error = abs(Work - AnalyticGasWork(Vi, Vf))
    
    print('The work done by the gas when it expands from {:2.2f} ml to {:2.2f} ml is {:2.2f} ergs'.format(Vi, Vf, Work))

    return Work, V, Error

def AnalyticGasWork(Vi, Vf):
    # Compute ideal gas work done analytically

    # parameters in cgs units
    N = (16/44) * 6.022e23
    kbT = 4*10**(-14)

    # calculate work done
    Work = N * kbT * math.log(Vf/Vi)

    return Work


if __name__ == "__main__":
    steps = [10+10*i for i in range(10)]
    Work = [0 for i in range(10)]
    Error = [0 for i in range(10)]

    for step in steps:
        w, v, err = IdealGasWorkLH(34, 56, step)
        print('The error in the work done is {:2.2f} ergs'.format(err))
