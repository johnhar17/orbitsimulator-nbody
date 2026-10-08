import numpy as np
from src.physics import compute_accelerations

class RK4Solver:
    """
    Integrator numerik Runge-Kutta 4th Order.
    Lebih stabil dibanding Euler Method untuk simulasi orbital jangka panjang.
    """
    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, bodies: list):
        n = len(bodies)
        # Ekstraksi matriks state terkini
        positions = np.array([b.position for b in bodies])
        velocities = np.array([b.velocity for b in bodies])
        masses = np.array([b.mass for b in bodies])

        # Step K1
        v_k1 = velocities
        a_k1 = compute_accelerations(positions, masses)

        # Step K2
        v_k2 = velocities + 0.5 * self.dt * a_k1
        a_k2 = compute_accelerations(positions + 0.5 * self.dt * v_k1, masses)

        # Step K3
        v_k3 = velocities + 0.5 * self.dt * a_k2
        a_k3 = compute_accelerations(positions + 0.5 * self.dt * v_k2, masses)

        # Step K4
        v_k4 = velocities + self.dt * a_k3
        a_k4 = compute_accelerations(positions + self.dt * v_k3, masses)

        # Kalkulasi state baru berdasarkan bobot Runge-Kutta
        new_positions = positions + (self.dt / 6.0) * (v_k1 + 2*v_k2 + 2*v_k3 + v_k4)
        new_velocities = velocities + (self.dt / 6.0) * (a_k1 + 2*a_k2 + 2*a_k3 + a_k4)

        # Sinkronisasi state kembali ke objek
        for i in range(n):
            bodies[i].update_state(new_positions[i], new_velocities[i])