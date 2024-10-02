def derivatives(state, t, q_m):
    x, y, dx_dt, dy_dt = state
    r = (x**2 + y**2)**0.5
    d2x_dt2 = -x/r + q_m*x/r**3
    d2y_dt2 = -y/r + q_m*y/r**3
    return [dx_dt, dy_dt, d2x_dt2, d2y_dt2]


def rk4_step(state, t, dt, q_m):
    k1 = np.array(derivatives(state, t, q_m)) * dt
    k2 = np.array(derivatives(state + 0.5 * k1, t + 0.5 * dt, q_m)) * dt
    k3 = np.array(derivatives(state + 0.5 * k2, t + 0.5 * dt, q_m)) * dt
    k4 = np.array(derivatives(state + k3, t + dt, q_m)) * dt
    
    return state + (k1 + 2 * k2 + 2 * k3 + k4) / 6

# Initial conditions and parameters
def solve_orbit(q_m, t_end=100, dt=0.01):
    # Initial state: [x, y, vx, vy]
    x0, y0 = 1.0, 0.0  # Starting at (1, 0)
    vx0, vy0 = 0.0, 1.0  # Circular velocity for q = 0
    state = np.array([x0, y0, vx0, vy0])
    
    # Time array
    t_values = np.arange(0, t_end, dt)
    
    # Arrays to store the trajectory
    x_values = []
    y_values = []
    
    # Time stepping
    for t in t_values:
        x_values.append(state[0])
        y_values.append(state[1])
        state = rk4_step(state, t, dt, q_m)
    
    return x_values, y_values, t_values


# Plot the orbits for different q/m values
q_m_values = [0.0, 0.5, 1.0, 2.0]  # Vary q/m

plt.figure(figsize=(6, 6))
for q_m in q_m_values:
    x_values, y_values, _ = solve_orbit(q_m)
    plt.plot(x_values, y_values, label=f'q/m = {q_m}')
    
plt.xlabel('x')
plt.ylabel('y')
plt.title('2D Orbits for Different Values of q/m')
plt.legend()
plt.grid(True)
plt.show()
