from hbase import HBaseSimulator
from command_line import CommandLineInterface
from utils import load_initial_data

def main():
    simulator = HBaseSimulator()
    load_initial_data(simulator, "../data/initial_data.json")  # Asegúrate de tener la ruta correcta al archivo JSON
    cli = CommandLineInterface(simulator)
    cli.run()

if __name__ == "__main__":
    main()
