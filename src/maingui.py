from gui import HBaseGUI
import tkinter as tk
from hbase import HBaseSimulator
from utils import load_initial_data

def main():
    root = tk.Tk()
    simulator = HBaseSimulator()
    load_initial_data(simulator, "./data/initial_data.json")
    app = HBaseGUI(root, simulator)
    root.mainloop()

if __name__ == "__main__":
    main()
