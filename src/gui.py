import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from hbase import HBaseSimulator
from utils import load_initial_data

class HBaseGUI:
    def __init__(self, root, simulator):
        self.simulator = simulator

        root.title("HBase Simulator")
        root.geometry("800x600")

        self.command_frame = tk.Frame(root)
        self.command_frame.pack(pady=10)

        self.command_label = tk.Label(self.command_frame, text="Enter command:")
        self.command_label.pack(side=tk.LEFT, padx=5)

        self.command_entry = tk.Entry(self.command_frame, width=70)
        self.command_entry.pack(side=tk.LEFT, padx=5)
        self.command_entry.bind("<Return>", self.run_command)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.result_label = tk.Label(self.result_frame, text="Results:")
        self.result_label.pack(anchor="w")

        self.result_text = scrolledtext.ScrolledText(self.result_frame, width=100, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.result_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.pack_forget()

    def run_command(self, event):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.handle_command(command)

    def handle_command(self, command):
        self.result_text.delete(1.0, tk.END)
        self.clear_table()
        self.tree.pack_forget()  # Oculta la tabla
        self.result_text.pack(fill=tk.BOTH, expand=True)  # Muestra el área de texto

        parts = command.split()
        if not parts:
            self.result_text.insert(tk.END, "No command entered.\n")
            return
        cmd = parts[0].lower()
        args = parts[1:]

        try:
            if cmd == "create" and len(args) == 2:
                table_name, column_families = args
                column_families = column_families.split(',')
                self.simulator.create_table(table_name, column_families)
                self.result_text.insert(tk.END, f"Table '{table_name}' created with column families {column_families}.\n")
            elif cmd == "help":
                self.print_help()
            elif cmd == "list":
                tables = self.simulator.list_tables()
                self.result_text.insert(tk.END, f"Tables: {tables}\n")
            elif cmd == "put" and len(args) == 6:
                table_name, row_key, column_family, column, value, timestamp = args
                self.simulator.put(table_name, row_key, column_family, column, value, timestamp)
                self.result_text.insert(tk.END, f"Inserted/Updated row '{row_key}' in table '{table_name}'.\n")
            elif cmd == "get" and len(args) == 4:
                value, timestamp = self.simulator.get(*args)
                if value is not None:
                    self.result_text.insert(tk.END, f"Value: {value}, Timestamp: {timestamp}\n")
                else:
                    self.result_text.insert(tk.END, "No data found.\n")
            elif cmd == "scan" and len(args) == 1:
                table_name = args[0]
                data = self.simulator.scan(table_name)
                if data:
                    columns = ["Row Key","Column Family" ,"Column", "Value", "Timestamp"]
                    rows = []
                    for family in data:
                        for row_key, columns_data in sorted(data[family].items()):
                            for column, (value, timestamp) in columns_data.items():
                                rows.append((row_key, family, column, value, timestamp))
                    self.result_text.pack_forget()  # Oculta el área de texto
                    self.display_table(columns, rows)
                else:
                    self.result_text.insert(tk.END, "No data found.\n")
            elif cmd == "disable" and len(args) == 1:
                self.simulator.disable_table(args[0])
                self.result_text.insert(tk.END, f"Table '{args[0]}' has been disabled.\n")
            elif cmd == "enable" and len(args) == 1:
                self.simulator.enable_table(args[0])
                self.result_text.insert(tk.END, f"Table '{args[0]}' has been enabled.\n")
            elif cmd == "is_enabled" and len(args) == 1:
                enabled = self.simulator.is_enabled(args[0])
                state = "enabled" if enabled else "disabled"
                self.result_text.insert(tk.END, f"Table '{args[0]}' is {state}.\n")
            elif cmd == "truncate" and len(args) == 1:
                self.simulator.truncate_table(args[0])
                self.result_text.insert(tk.END, f"Table '{args[0]}' has been truncated and recreated.\n")
            elif cmd == "drop" and len(args) == 1:
                self.simulator.drop_table(args[0])
                self.result_text.insert(tk.END, f"Table '{args[0]}' has been dropped.\n")
            elif cmd == "alter" and len(args) == 3:
                table_name, operation, column_family = args
                self.simulator.alter_table(table_name, operation, column_family)
                self.result_text.insert(tk.END, f"Table '{table_name}' altered: {operation} column family '{column_family}'.\n")
            elif cmd == "drop_all":
                self.simulator.drop_all_tables()
                self.result_text.insert(tk.END, "All tables have been dropped.\n")
            elif cmd == "describe" and len(args) == 1:
                self.simulator.describe_table(args[0])
            elif cmd == "delete" and len(args) == 4:
                self.simulator.delete(*args)
                self.result_text.insert(tk.END, f"Deleted column '{args[3]}' from row '{args[1]}' in table '{args[0]}'.\n")
            elif cmd == "deleteall" and len(args) == 2:
                self.simulator.delete_all(args[0], args[1])
                self.result_text.insert(tk.END, f"Deleted all columns from row '{args[1]}' in table '{args[0]}'.\n")
            elif cmd == "count" and len(args) == 1:
                count = self.simulator.count_rows(args[0])
                self.result_text.insert(tk.END, f"Table '{args[0]}' has {count} rows.\n")
            else:
                self.result_text.insert(tk.END, "Unknown command or incorrect number of arguments. Type 'help' for a list of commands.\n")
        except ValueError as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def display_table(self, columns, rows):
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        for row in rows:
            self.tree.insert("", tk.END, values=row)
        self.tree.pack(fill=tk.BOTH, expand=True)  # Muestra la tabla

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def print_help(self):
        help_text = """
        Available commands:
        - create [table_name] [column_family1,column_family2,...]: Create a new table.
        - list: List all tables.
        - put [table_name] [row_key] [column_family] [column] [value] [timestamp]: Insert or update a value.
        - get [table_name] [row_key] [column_family] [column]: Retrieve a value.
        - scan [table_name]: Scan a table.
        - disable [table_name]: Disable a table.
        - enable [table_name]: Enable a table.
        - is_enabled [table_name]: Check if a table is enabled.
        - alter [table_name] [add/remove] [column_family]: Alter a table.
        - drop [table_name]: Drop a table.
        - drop_all: Drop all tables.
        - describe [table_name]: Describe a table.
        - delete [table_name] [row_key] [column_family] [column]: Delete a specific column.
        - deleteall [table_name] [row_key]: Delete all columns in a specific row.
        - count [table_name]: Count the number of rows in a table.
        - exit: Exit the CLI.
        """
        self.result_text.insert(tk.END, help_text)

def main():
    root = tk.Tk()
    simulator = HBaseSimulator()
    load_initial_data(simulator, "../data/initial_data.json")
    app = HBaseGUI(root, simulator)
    root.mainloop()

if __name__ == "__main__":
    main()
