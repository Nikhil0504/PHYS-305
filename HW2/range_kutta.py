# dm_dt = c(1-m) - 10*w*m
# dc_dt = 5*m*(1-c) - 1.25*c + S(t)
# dw_dt = 0.01*(1-w) - 4*m*w

# S(t) = alpha when 3 < t < 3.2 and 0 otherwise
# m(0) = 0.0114, c(0) = 0.0090, and w(0) = 0.9374
# delta_t = 0.002 and t_end = 30

# use 4th order Runge-Kutta method to solve the system of equations
#  Vary α to find a value for which the equilibrium 
# switches to a new location.  You should use a ∆t = 0.002 and run for a total time of 30.  Make a 
# plot showing m, c, and w as functions of time when the equilibrium position switches.  

import numpy as np
import matplotlib.pyplot as plt


# Define the function from question

def S(t, alpha):
    return alpha if 3 < t < 3.2 else 0

def dm_dt(m, c, w):
    return c*(1 - m) - 10*w*m

def dc_dt(m, c, w, t, alpha=0.2):
    return 5*m*(1-c) - 1.25*c + S(t, alpha)

def dw_dt(m, c, w):
    return 0.01*(1-w) - 4*m*w


def runge_kutta_step(m, c, w, t, dt, alpha):
    """
    Runge-Kutta 4th order method for a single step
    
    Parameters
    ----------
    
    m : float
        Value of m at the current time step
    c : float
        Value of c at the current time step
    w : float
        Value of w at the current time step
    t : float
        Current time
    dt : float
        Time step
    alpha : float
        Value of alpha
    
    Returns
    -------
    m_next : float
        Value of m at the next time step
    c_next : float
        Value of c at the next time step
    w_next : float
        Value of w at the next time step
    """
    k1_m = dt * dm_dt(m, c, w)
    k2_m = dt * dm_dt(m + 0.5 * k1_m, c, w)
    k3_m = dt * dm_dt(m + 0.5 * k2_m, c, w)
    k4_m = dt * dm_dt(m + k3_m, c, w)

    k1_c = dt * dc_dt(m, c, w, t, alpha)
    k2_c = dt * dc_dt(m, c + 0.5 * k1_c, w, t, alpha)
    k3_c = dt * dc_dt(m, c + 0.5 * k2_c, w, t, alpha)
    k4_c = dt * dc_dt(m, c + k3_c, w, t, alpha)

    k1_w = dt * dw_dt(m, c, w)
    k2_w = dt * dw_dt(m, c, w + 0.5 * k1_w)
    k3_w = dt * dw_dt(m, c, w + 0.5 * k2_w)
    k4_w = dt * dw_dt(m, c, w + k3_w)

    m_next = m + (k1_m + 2 * k2_m + 2 * k3_m + k4_m) / 6
    c_next = c + (k1_c + 2 * k2_c + 2 * k3_c + k4_c) / 6
    w_next = w + (k1_w + 2 * k2_w + 2 * k3_w + k4_w) / 6

    return m_next, c_next, w_next


def solve_system(m0, c0, w0, alpha, dt, t_end):
    """
    Solve the system of equations using the 4th order Runge-Kutta method

    Parameters
    ----------
    m0 : float
        Initial value of m
    c0 : float
        Initial value of c
    w0 : float
        Initial value of w
    alpha : float
        Value of alpha
    dt : float
        Time step
    t_end : float
        End time
    
    Returns
    -------
    time : numpy.ndarray
        Array of time values
    m : numpy.ndarray
        Array of m values
    c : numpy.ndarray
        Array of c values
    w : numpy.ndarray
        Array of w values
    """

    time = np.arange(0, t_end, dt)

    m = np.zeros_like(time)
    c = np.zeros_like(time)
    w = np.zeros_like(time)

    m[0], c[0], w[0] = m0, c0, w0

    for i in range(1, len(time)):
        m[i], c[i], w[i] = runge_kutta_step(m[i-1], c[i-1], w[i-1], time[i-1], dt, alpha)

    return time, m, c, w


if __name__ == "__main__":
    # Initial conditions
    m0, c0, w0 = 0.0114, 0.0090, 0.9374
    dt = 0.002
    t_end = 30

    # Vary alpha to find equilibrium switch
    # alphas = np.arange(1., 20, 0.5)
    alphas = [5.5, 6]
    styles = ['-', '--', '-.']

    plt.figure(figsize=(10, 6), dpi=150)

    for alpha, style in zip(alphas, styles):
        time, m, c, w = solve_system(m0, c0, w0, alpha, dt, t_end)

        plt.plot(time, m, label=f"_m, alpha = {alpha:.2f}", color='k', linestyle=style)
        plt.plot(time, c, label=f"_c, alpha = {alpha:.2f}", color='b', linestyle=style)
        plt.plot(time, w, label=f"_w, alpha = {alpha:.2f}", color='g', linestyle=style)
        plt.plot([], [], f'k{style}', label=f'{alpha:.2f}')

        # Debugging for equilibrium switch
        print(f'Alpha: {alpha}')
        print(f'Differnce in m: {m[-1] - m[0]}')
        print(f'Differnce in c: {c[-1] - c[0]}')
        print(f'Differnce in w: {w[-1] - w[0]}')
        print('---------------------------------')

    # legend
    l1 = plt.legend(['m', 'c', 'w'])

    l2 = plt.legend(loc='upper left', title='$\\alpha$', title_fontsize='large', frameon=True)
    plt.gca().add_artist(l1)
    plt.gca().add_artist(l2)

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("System of Equations with Varying Alpha")
    plt.grid(True)

    plt.savefig("range_kutta.png")
    plt.show()