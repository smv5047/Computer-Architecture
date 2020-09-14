"""CPU functionality."""
# TODO
# TODO - use number of operands +1  to increment PC
import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.is_running = True
        # 256 bit memory
        self.ram = [0] * 256
        # temporary memory, read and write to
        self.register = [0, 0, 0, 0, 0, 0, 0, 255]
        # program counter
        self.pc = 0
        # Stack Pointer
        self.sp = 7
        # Flags register
        # set 5 to 1 if less than
        # set 6 to 1 if greater than
        # set 7 to 1 if equal
        # self.fl = [0] * 8
        self.fl = {
            "E": 0,
            "L": 0,
            "G": 0
        }
        # ops codes
        # set of instruction codes
        self.ops = {
            'HLT': 0b00000001,  # Halt
            'LDI': 0b10000010,
            'PRN': 0b01000111,  # Print
            'MUL': 0b10100010,  # multiply
            'POP': 0b01000110,
            'PUSH': 0b01000101,
            'CALL': 0b01010000,
            'RET': 0b00010001,
            'ADD': 0b10100000,
            'NOP': 0b00000000,
            'CMP': 0b10100111,
            'JMP': 0b01010100,
            'JEQ': 0b01010101,
            'JNE': 0b01010110
        }

    # def stack_pointer(self):
    #     print(self.register[7])
    #     self.register[self.sp] = len(self.ram)
    #     print(self.register[7])

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

                    num = int(code_value, 2)
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
        elif op == "CMP":

            if reg_a == reg_b:
                # self.fl["L"] = 0
                # self.fl["G"] = 0
                self.fl["E"] = 1
            elif reg_a < reg_b:
                self.fl["L"] = 1
                # self.fl["G"] = 0
                # self.fl["E"] = 0
            elif reg_a > reg_b:
                # self.fl["L"] = 0
                self.fl["G"] = 1
                # self.fl["E"] = 0

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
            if instruction == self.ops['ADD']:

                self.alu("ADD", operand_a, operand_b)

                self.pc += 3

            elif instruction == self.ops['LDI']:

                self.register[operand_a] = operand_b
                self.pc += 3

            elif instruction == self.ops['PRN']:
                print(self.register[operand_a])
                self.pc += 2

            elif instruction == self.ops['MUL']:
                self.register[operand_a] = self.register[operand_a] * \
                    self.register[operand_b]
                self.pc += 3

            elif instruction == self.ops['POP']:
                # get register
                given_register = self.ram[self.pc+1]
                # write the value in memory at the top of stack to the given register
                # get value from memory
                value_from_memory = self.ram[self.register[self.sp]]
                self.register[given_register] = value_from_memory
                # increment the stack pointer
                # if self.register[self.sp] < len(self.ram)-1:
                self.register[self.sp] += 1
                self.pc += 2

            elif instruction == self.ops['PUSH']:
                # get register we will be working with
                given_register = self.ram[self.pc+1]
                # get  value in that register
                # stack pointer, we want to decress it
                value_in_register = self.register[given_register]
                # decrement the Stack Pointer
                # since the 8th spot in register is reserved for stack pointer
                self.register[self.sp] -= 1
                # write the value of the given register
                self.ram[self.register[self.sp]] = value_in_register
                # increment pc by 2
                self.pc += 2

            elif instruction == self.ops['CALL']:
                # get the given register in the operand
                given_register = self.ram[self.pc+1]
                # Store the return address [PC +2) onto the stack
                # decrement the Stack Pointer
                self.register[self.sp] -= 1
                # write return address
                self.ram[self.register[self.sp]] = self.pc+2
                # SET PC TO value inside givne register
                self.pc = self.register[given_register]

            elif instruction == self.ops['RET']:
                # set PC to the value at the top of the stack
                self.pc = self.ram[self.register[self.sp]]
                # POP from stack
                self.register[self.sp] += 1

            elif instruction == self.ops['HLT']:
                self.running = False
                sys.exit(0)

            elif instruction == self.ops['NOP']:
                print('nop')

            elif instruction == self.ops['CMP']:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif instruction == self.ops['JMP']:
                # jump to the address stored in the given register
                given_register = operand_a
                # set the pc to the address stored in the given register
                self.pc = self.register[given_register]

            elif instruction == self.ops['JEQ']:
                # if equal flag is set to true,
                if self.fl["E"] == 1:
                    # jump to the address stored in the given register
                    given_register = operand_a
                    # set the pc to the address stored in the given register
                    self.pc = self.register[given_register]
                else:
                    self.pc += 2

            elif instruction == self.ops['JNE']:
                # If equal flag is not set to 1
                if self.fl["E"] == 0:
                    # jump to the address stored in the given register
                    given_register = operand_a
                    # set the pc to the address stored in the given register
                    self.pc = self.register[given_register]
                else:
                    self.pc += 2

            else:
                self.trace()
                print(f"Unknown instruction {instruction}")
                # program did not end cleanly
                sys.exit(1)
