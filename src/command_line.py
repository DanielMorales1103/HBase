class CommandLineInterface:
    def __init__(self, simulator):
        self.simulator = simulator

    def run(self):
        print("Welcome to the HBase Simulator CLI.")
        print("Type 'help' for a list of commands.")
        while True:
            command = input("Enter command: ")
            if command.lower() == "exit":
                print("Exiting HBase Simulator CLI.")
                break
            self.handle_command(command)

    def handle_command(self, command):
        parts = command.split()
        if not parts:
            print("No command entered.")
            return
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "create" and len(args) == 2:
            table_name, column_families = args
            column_families = column_families.split(',')
            try:
                self.simulator.create_table(table_name, column_families)
                print(f"Table '{table_name}' created with column families {column_families}.")
            except ValueError as e:
                print(e)
        elif cmd == "help":
            self.print_help()
        elif cmd == "list":
            tables = self.simulator.list_tables()
            print("Tables:", tables)
        elif cmd == "put" and len(args) == 6:
            table_name, row_key, column_family, column, value, timestamp = args
            try:
                self.simulator.put(table_name, row_key, column_family, column, value, timestamp)
                print(f"Inserted value '{value}' at {table_name}.{row_key}.{column_family}.{column} with timestamp {timestamp}.")
            except ValueError as e:
                print(e)
        elif cmd == "get" and len(args) == 4:
            table_name, row_key, column_family, column = args
            result = self.simulator.get(table_name, row_key, column_family, column)
            if result:
                value, timestamp = result
                print(f"Value: {value}, Timestamp: {timestamp}")
            else:
                print("No data found.")
        elif cmd == "scan":
            if len(args) != 1:
                print("Usage: scan [table_name]")
            else:
                try:
                    data = self.simulator.scan(args[0])
                    for column_family, rows in data.items():
                        print(f"Column Family: {column_family}")
                        for row_key, columns in rows.items():
                            print(f"  Row Key: {row_key}")
                            for column, (value, timestamp) in columns.items():
                                print(f"    Column: {column}, Value: {value}, Timestamp: {timestamp}")
                except ValueError as e:
                    print(e)
        elif cmd == "disable":
            if len(args) != 1:
                print("Usage: disable [table_name]")
            else:
                try:
                    self.simulator.disable_table(args[0])
                except ValueError as e:
                    print(e)
        elif cmd == "enable":
            if len(args) != 1:
                print("Usage: enable [table_name]")
            else:
                try:
                    self.simulator.enable_table(args[0])
                except ValueError as e:
                    print(e)
        elif cmd == "is_enabled":
            if len(args) != 1:
                print("Usage: is_enabled [table_name]")
            else:
                try:
                    enabled = self.simulator.is_enabled(args[0])
                    state = "enabled" if enabled else "disabled"
                    print(f"Table '{args[0]}' is {state}.")
                except ValueError as e:
                    print(e)
        elif cmd == "truncate":
            if len(args) != 1:
                print("Usage: truncate [table_name]")
            else:
                try:
                    self.simulator.truncate_table(args[0])
                except ValueError as e:
                    print(e)
        elif cmd == "drop":
            if len(args) != 1:
                print("Usage: drop [table_name]")
            else:
                try:
                    table_name = args[0]
                    self.simulator.drop_table(table_name)
                    print(f"Table '{table_name}' has been successfully dropped.")
                except ValueError as e:
                    print(e)
        elif cmd == "alter":
            if len(args) != 3:
                print("Usage: alter [table_name] [add/remove] [column_family]")
            else:
                table_name, operation, column_family = args
                try:
                    self.simulator.alter_table(table_name, operation, column_family)
                except ValueError as e:
                    print(e)
        elif cmd == "drop_all":
            try:
                self.simulator.drop_all_tables()
            except Exception as e:
                print(e)
        elif cmd == "describe":
            if len(args) != 1:
                print("Usage: describe [table_name]")
            else:
                try:
                    self.simulator.describe_table(args[0])
                except ValueError as e:
                    print(e)
        else:
            print("Unknown command or incorrect number of arguments. Type 'help' for a list of commands.")

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
        - exit: Exit the CLI.
        """
        print(help_text)
