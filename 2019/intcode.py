"""IntCode VM created in exercise 2/5/7/9 and used on other days"""
from aocd.models import Puzzle

def read_program_string(values_str):
    """read the program from the input"""
    return [int(v) for v in values_str.strip().split(',')]

def read_program_for_puzzle(puzzle_no):
    puzzle = Puzzle(2019,puzzle_no)
    data = puzzle.input_data
    # data = "1,9,10,3,2,3,11,0,99,30,40,50"
    return read_program_string(data)

instruction_sizes = {  # instruction sizes and #variables
    1: (4,2),
    2: (4,2),
    3: (2,0),
    4: (2,1),
    5: (3,2),
    6: (3,2),
    7: (4,2),
    8: (4,2),
    9: (2,1),  # adjust relative base
    99: (1,0)
}
class IntCode:
    """IntCode VM"""

    def __init__(self,program):
        self.memory = list(program).copy()
        self.pointer = 0
        self.relative_base = 0

    def run_test(self,input_val):
        """test returns 0 outputs until a final exit code"""
        while True:
            output = self.run(input_val)
            if output:
                assert self.memory[self.pointer]==99
                return output

    def _write(self,addr,val):
        if addr>=len(self.memory):
            self.memory.extend([0]*(addr-len(self.memory)+1))
        self.memory[addr]=val

    def _read(self,addr):
        if addr>=len(self.memory):
            return 0
        return self.memory[addr]

    def _get_loc(self,addr,mode):
        if mode == 0:
            return addr
        elif mode == 2:
            return self.relative_base+addr
        else:
            raise ValueError(f"Unknown mode {mode}")

    def _read_var(self,val,mode):
        if mode==1:
            return val
        else:
            return self._read(self._get_loc(val,mode))

    def run_all(self,inputs=None):
        """run the program until it halts"""
        outputs = []
        while True:
            try:
                output = self.run(inputs)
                outputs.append(output)
            except GeneratorExit:
                return outputs

    def run(self,inputs=None):
        # run the program. Stops at and retuns the next output, or raises a GeneratorExit
        if inputs is not None:
            if isinstance(inputs,int):
                inputs = [inputs]
            input_pointer = 0

        while True:
            inp=self._read(self.pointer)
            opcode = inp%100
            if opcode == 99:
                raise GeneratorExit

            instr_size,var_size = instruction_sizes[opcode]
            write_res = instr_size-var_size==2

            parameters = [self._read(p) for p in range(self.pointer+1,self.pointer+instr_size)]

            # 0: position mode
            # 1: immediate mode
            # 2: relative mode
            parameter_modes = [(inp//10**d)%10 for d in range(2,instr_size+1)]
            assert set(parameter_modes)<={0,1,2},parameter_modes

            if var_size:
                variables = [self._read_var(ix,pmode) for pmode,ix in zip(parameter_modes,parameters[:var_size])]

            self.pointer += instr_size

            if opcode==4:
                output = variables[0]
                return output

            if opcode == 1:
                v1,v2 = variables
                res  = v1+v2
                # self._write(res_addr,res)
            elif opcode == 2:
                v1,v2 = variables
                res  = v1*v2
            elif opcode==3:
                res = inputs[input_pointer]
                input_pointer+=1
            elif opcode in (5,6):
                v1,v2=variables
                if bool(v1)== (opcode==5):
                    self.pointer=v2
            elif opcode==7:
                v1,v2=variables
                res = int(v1<v2)
            elif opcode==8:
                v1,v2=variables
                res = int(v1==v2)
            elif opcode==9:
                v1 = variables[0]
                self.relative_base += v1
            else:
                raise(ValueError(f"Unknown opcode {opcode}"))

            if write_res:
                res_addr = self._get_loc(parameters[-1],parameter_modes[-1])
                self._write(res_addr,res)

