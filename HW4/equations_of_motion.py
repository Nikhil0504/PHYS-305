import numpy as np
import matplotlib.pyplot as plt

def initialize_conditions():
    mass = 1.0
    constant1 = 1
    alpha = 1
    beta = 1
    
    # Initial Positions
    r1 = np.array([0.0, 0.0, 0.0])
    r2 = np.array([1.0, 0.0, 0.0])
    
    # Initial Directions (unit vectors)
    d1 = np.array([1.0, 0.0, 0.0])
    d2 = np.array([0.0, 0.0, 1.0])
    
    dt = 0.1
    timestep = 1000
    v0 = 10
    
    return r1, r2, d1, d2, mass, constant1, alpha, beta, dt, timestep, v0

def compute_accelerations(r1, r2, d1, d2, v1, v2, v0, zeta, alpha, beta, mass):
    r = np.linalg.norm(r1 - r2)

    dv1_dt = (zeta * ((v0 * d1) - v1) + (alpha / r) * (v2 - v1)) / mass
    dd1_dt = beta / (r * r) * np.cross(np.cross(d1, d2), d1)

    dv2_dt = (zeta * ((v0 * d2) - v2) + (alpha / r) * (v1 - v2)) / mass
    dd2_dt = beta / (r * r) * np.cross(np.cross(d2, d1), d2)

    return dv1_dt, dd1_dt, dv2_dt, dd2_dt

def update_positions_and_directions(r1, r2, d1, d2, v1, v2, dv1_dt, dv2_dt, dd1_dt, dd2_dt, dt, v0):
    d1 = d1 + dd1_dt * dt
    d2 = d2 + dd2_dt * dt

    # Normalizing these vectors
    d1 = d1 / np.linalg.norm(d1)
    d2 = d2 / np.linalg.norm(d2)
    
    v1 = v0 * d1
    v2 = v0 * d2
    
    r1 = r1 + (dv1_dt * dt)
    r2 = r2 + (dv2_dt * dt)
    
    return r1, r2, d1, d2, v1, v2

def question_1_equations(r1, r2, d1, d2, mass, constant1, alpha, beta, dt, timestep, v0):
    v1 = v0 * d1
    v2 = v0 * d2
    
    r1_total = np.zeros((timestep, 3))
    r2_total = np.zeros((timestep, 3))
    
    r1_total[0] = r1
    r2_total[0] = r2
    
    for step in range(1, timestep):
        dv1_dt, dd1_dt, dv2_dt, dd2_dt = compute_accelerations(r1, r2, d1, d2, v1, v2, v0, constant1, alpha, beta, mass)
        r1, r2, d1, d2, v1, v2 = update_positions_and_directions(r1, r2, d1, d2, v1, v2, dv1_dt, dv2_dt, dd1_dt, dd2_dt, dt, v0)
        
        r1_total[step] = r1
        r2_total[step] = r2
        
    return r1_total, r2_total

def plot_results(r1_total, r2_total):
    plt.plot(r1_total)
    plt.plot(r2_total)
    plt.show()

def question_1():
    r1, r2, d1, d2, mass, constant1, alpha, beta, dt, timestep, v0 = initialize_conditions()
    r1_total, r2_total = question_1_equations(r1, r2, d1, d2, mass, constant1, alpha, beta, dt, timestep, v0)
    plot_results(r1_total, r2_total)
    print(r1_total[-1])
        
question_1()