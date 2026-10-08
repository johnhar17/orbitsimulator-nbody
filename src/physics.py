import numpy as np

# Menggunakan G=1 (satuan tereduksi) agar simulasi lebih proporsional secara visual
GRAVITATIONAL_CONSTANT = 1.0 

def compute_accelerations(positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """
    Menghitung vektor akselerasi gravitasi untuk setiap benda
    berdasarkan hukum Gravitasi Universal Newton.
    """
    n = len(masses)
    accelerations = np.zeros_like(positions)
    
    for i in range(n):
        for j in range(n):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_mag = np.linalg.norm(r_vec)
                
                # Softening parameter (1e-5) mencegah singularitas/pembagian nol 
                # saat dua benda sangat berdekatan
                if r_mag > 1e-5:
                    force_magnitude = (GRAVITATIONAL_CONSTANT * masses[j]) / (r_mag**3)
                    accelerations[i] += force_magnitude * r_vec
                    
    return accelerations