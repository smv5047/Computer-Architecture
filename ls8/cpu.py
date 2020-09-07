"""CPU functionality."""
# TODO Why are my instructions not being interpretted correctly
import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.is_running = True
        # 256 bit memory
        self.ram = [0] * 256
        # temporary memory, read and write to
        self.register = [0] * 8
        # program counter
        self.pc = 0
        # ops codes
        # set of instruction codes
        self.ops = {
            'HLT': 0b00000001,  # Halt
            'LDI': 0b10000010,
            'PRN': 0b01000111  # Print
        }

    def load(self):
        """Load a program into memory."""
        # open a file
        # get file name from command line arguments
        # argv gives us an array of arguments passed in via the command line
        # check if not enough or too many arguments were past
        address = 0
        if len(sys.argv) != 2:
            print("Usage: failed to pass correct number of arguments")
            sys.exit(1)
        try:
            # LOAD FILE FROM SYS.ARGV[1]
            with open(sys.argv[1]) as f:
                for line in f:
                    # split the current lin on # symbol
                    split_line = line.split('#')
                    # removes whitespace and \n character
                    code_value = split_line[0].strip()
                    # make sure value before # is nto empty
                    if code_value == '':
                        continue

                    num = int(code_value)
                    self.ram[address] = num
                    address += 1
                    # print(bin(int(line)))

        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()
    # Inside the CPU, there are two internal registers used for memory operations:
    # the Memory Address Register (MAR) and the Memory Data Register (MDR).
    # The MAR contains the address that is being read or written to.
    # The MDR contains the data that was read or the data to write.
    # You dont need to add the MAR or MDR to your CPU class,
    # but they would make handy parameter names for ram_read() and ram_write()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        while self.is_running:
            instruction = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if instruction == self.ops['LDI']:

                self.register[operand_a] = operand_b
                self.pc += 3

            elif instruction == self.ops['PRN']:

                print(self.register[operand_a])
                self.pc += 2

            elif instruction == self.ops['HLT']:
                self.running = False
                self.pc += 1

            else:
                print(f"Unknown instruction {instruction}")
                # program did not end cleanly
                sys.exit(1)
