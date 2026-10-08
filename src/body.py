import numpy as np

class CelestialBody:
    """
    Abstraksi benda langit dalam sistem N-Body.
    Menyimpan state (massa, posisi, kecepatan) untuk proses komputasi.
    """
    def __init__(self, name: str, mass: float, position: list, velocity: list, color: str):
        self.name = name
        self.mass = float(mass)
        # Konversi ke array float64 agar presisi numerik terjaga
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.color = color

    def update_state(self, new_position: np.ndarray, new_velocity: np.ndarray):
        """Memperbarui posisi dan kecepatan benda ke siklus berikutnya."""
        self.position = new_position
        self.velocity = new_velocity