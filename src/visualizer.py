import numpy as np
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg

class OrbitVisualizer(QMainWindow):
    """
    Mesin rendering real-time dengan antarmuka modern menggunakan PyQtGraph.
    """
    def __init__(self, bodies, solver):
        super().__init__()
        self.bodies = bodies
        self.solver = solver
        
        self.trail_length = 600  # Panjang jejak trajektori
        self.history = {b.name: [] for b in self.bodies}

        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("N-Body Dynamics System")
        self.resize(1100, 800)
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        # Konfigurasi widget utama
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header modern dengan font Open Sans
        title = QLabel("N-Body Gravitational Simulator")
        title.setFont(QFont("Open Sans", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)
        
        # Inisialisasi Environment PyQtGraph
        pg.setConfigOptions(antialias=True)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1a1a1a')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.15)
        # Menjaga aspek rasio 1:1 (supaya orbit tidak gepeng)
        self.plot_widget.setAspectLocked(True) 
        self.layout.addWidget(self.plot_widget)
        
        # Setup item grafik per entitas benda
        self.scatter_items = []
        self.curve_items = []
        
        for body in self.bodies:
            # Garis jejak orbit (trail)
            curve = self.plot_widget.plot(pen=pg.mkPen(body.color, width=2.5))
            self.curve_items.append(curve)
            
            # Titik objek benda langit (scatter)
            scatter = pg.ScatterPlotItem(size=14, brush=pg.mkBrush(body.color))
            self.plot_widget.addItem(scatter)
            self.scatter_items.append(scatter)
        
        # Setup Timer UI Loop (Sekitar ~60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16) 
        
    def update_simulation(self):
        # Jalankan kalkulasi fisika (Multiple substeps per frame agar animasi lancar dan cepat)
        for _ in range(8):
            self.solver.step(self.bodies)
        
        # Render visual per objek
        for i, body in enumerate(self.bodies):
            pos = body.position
            self.history[body.name].append((pos[0], pos[1]))
            
            # Culling memori untuk membatasi array rendering jejak
            if len(self.history[body.name]) > self.trail_length:
                self.history[body.name].pop(0)
                
            hx = [p[0] for p in self.history[body.name]]
            hy = [p[1] for p in self.history[body.name]]
            
            self.curve_items[i].setData(hx, hy)
            self.scatter_items[i].setData([pos[0]], [pos[1]])