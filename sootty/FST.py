import subprocess

class VerilatorConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert_to_vcd(self):
        verilator_command = f"fst2vcd {self.input_file} > output.vcd"
        result = subprocess.run(verilator_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "output.vcd"

# Usage
file_name = "ABC.fst"  # Provide your file name here
verilator_converter = VerilatorConverter(file_name)
verilator_converter.convert_to_vcd()
