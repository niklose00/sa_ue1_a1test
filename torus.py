from glowworm import Glowworm
import random
import random
import math
import numpy as np

class Torus:
    def __init__(self, rows, cols, coupling_strength):
        """
        Initialisiert ein Torus-Gitter mit der angegebenen Anzahl von Zeilen und Spalten.
        :param rows: Die Anzahl der Zeilen im Torus-Gitter.
        :param cols: Die Anzahl der Spalten im Torus-Gitter.
        :param coupling_strength: Die Kopplungsstärke K für die Synchronisation.
        """
        self.rows = rows
        self.cols = cols
        self.coupling_strength = coupling_strength
        self.grid = [[Glowworm(natural_frequency=random.uniform(0.5, 1.5)) for _ in range(cols)] for _ in range(rows)]
        self._set_neighbors()

    def _set_neighbors(self):
        """
        Setzt die Nachbarn für jedes Glühwürmchen im Gitter unter Berücksichtigung der Torus-Randbedingungen.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                # Aktuelles Glühwürmchen
                glowworm = self.grid[row][col]

                # Nachbarn unter Berücksichtigung der Torus-Verbindungen
                top = self.grid[(row - 1) % self.rows][col]  # Nachbar oberhalb
                bottom = self.grid[(row + 1) % self.rows][col]  # Nachbar unterhalb
                left = self.grid[row][(col - 1) % self.cols]  # Nachbar links
                right = self.grid[row][(col + 1) % self.cols]  # Nachbar rechts

                # Hinzufügen der Nachbarn
                glowworm.add_neighbor(top)
                glowworm.add_neighbor(bottom)
                glowworm.add_neighbor(left)
                glowworm.add_neighbor(right)

    def update(self):
        # Zuerst die neuen Phasen berechnen und zwischenspeichern
        new_phases = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        for row in range(self.rows):
            for col in range(self.cols):
                # Berechne die neue Phase, ohne sie sofort zu aktualisieren
                new_phases[row][col] = self.grid[row][col].phase + \
                    self.grid[row][col].natural_frequency + \
                    (self.coupling_strength / len(self.grid[row][col].neighbors)) * \
                    sum(math.sin(neighbor.phase - self.grid[row][col].phase) for neighbor in self.grid[row][col].neighbors)
                
                # Begrenze die Phase auf den Bereich [0, 2π]
                new_phases[row][col] %= (2 * np.pi)
        
        # Aktualisiere alle Phasen gleichzeitig
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].phase = new_phases[row][col]

    def __repr__(self):
        """
        Gibt eine einfache Textdarstellung des Torus zurück.
        """
        representation = ""
        for row in self.grid:
            representation += " | ".join(f"{worm.phase:.2f}" for worm in row) + "\n"
        return representation


# Testen der Torus-Struktur
if __name__ == "__main__":
    # Erstellen eines 4x4-Torus-Gitters mit Kopplungsstärke K=1.0
    torus = Torus(rows=2, cols=2, coupling_strength=1.0)

    # Initialen Zustand des Torus ausgeben
    print("Initialer Zustand des Torus:")
    print(torus)

    # Update-Schritte zur Synchronisation durchführen
    for step in range(100000):
        torus.update()
        # Zustand des Torus nur alle 100 Schritte anzeigen
        if step % 1000==0 == 0:
            print(f"Aktualisierter Zustand des Torus nach {step + 1} Schritten:")
            print(torus)
