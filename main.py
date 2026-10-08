import sys
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from src.body import CelestialBody
from src.solver import RK4Solver
from src.visualizer import OrbitVisualizer

def load_environment(filepath: str) -> list:
    """Melakukan parsing dari file config JSON ke dalam Object."""
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    bodies = []
    for b in data['bodies']:
        body = CelestialBody(
            name=b['name'],
            mass=b['mass'],
            position=b['position'],
            velocity=b['velocity'],
            color=b['color']
        )
        bodies.append(body)
    return bodies

def main():
    app = QApplication(sys.argv)
    
    # Mencoba meload sistem font Open Sans (Akan jatuh fallback secara otomatis jika OS tidak punya)
    font_id = QFontDatabase.addApplicationFont("Open Sans")
    if font_id == -1:
        pass # Handle gracefully 
        
    # Memuat konfigurasi initial state
    bodies = load_environment('config/chaotic_three_body.json')
    
    # Inisiasi integrator dengan timestep (dt)
    solver = RK4Solver(dt=0.005)
    
    # Memulai Antarmuka Grafis
    visualizer = OrbitVisualizer(bodies, solver)
    visualizer.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()