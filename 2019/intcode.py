"""IntCode VM created in exercise 2/5/7/9 and used on other days"""
from collections.abc import Iterator
from aocd.models import Puzzle

def read_program_string(values_str):
    """read the program from the input"""
    return [int(v) for v in values_str.strip().split(',')]

def read_program_for_puzzle(puzzle_no):
    """read the program from the input"""
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

def _clean_inputs(inputs):
    if inputs is None:
        inputs = []
    elif isinstance(inputs,int):
        inputs = [inputs]
    if not isinstance(inputs,Iterator):
        inputs = iter(inputs)
    return inputs

class IntCode:
    """IntCode VM"""

    def __init__(self,program,name=None):
        self.memory = list(program).copy()
        self.pointer = 0
        self.relative_base = 0
        if name is not None:
            self.name = name

    def __str__(self):
        if hasattr(self,"name"):
            return f"IntCode({self.name})"
        else:
            return super().__str__()

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

    def run_test(self,input_val):
        """test returns 0 outputs until a final exit code
        we could use self.run() but then it won't stop at the first error
        """
        inputs = [input_val]
        while True:
            output = self.next_output(inputs)
            if output:
                assert self.memory[self.pointer]==99
                return output


    def run(self,inputs=None):
        """run the program until it halts"""
        inputs= _clean_inputs(inputs)
        outputs = []
        while True:
            try:
                output = self.next_output(inputs)
                outputs.append(output)
            except StopIteration:
                return outputs

    def run_simple(self,inputs=None):
        """often a program only has one output"""
        outputs = self.run(inputs)
        assert len(outputs)==1
        return outputs[0]

    def output_gen(self,inputs=None):
        """generator to get outputs"""
        while True:
            try:
                output = self.next_output(inputs)
                yield output
            except StopIteration:
                return


    def next_output(self,inputs_it=None):
        # run the program. 
        # inputs_it should be iterator or iterable
        inputs=_clean_inputs(inputs_it)
        while True:
            inp=self._read(self.pointer)
            opcode = inp%100
            if opcode == 99:
                raise StopIteration

            instr_size,var_size = instruction_sizes[opcode]
            write_res = instr_size-var_size==2

            parameters = [self._read(p) for p in range(self.pointer+1,self.pointer+instr_size)]

            # 0: position mode
            # 1: immediate mode
            # 2: relative mode
            parameter_modes = [(inp//10**d)%10 for d in range(2,instr_size+1)]
            assert set(parameter_modes)<={0,1,2},parameter_modes

            if var_size:
                variables = [self._read_var(val,pmode) for val,pmode in zip(parameters[:var_size],parameter_modes)]

            self.pointer += instr_size

            match opcode:
                case 1:
                    v1, v2 = variables
                    res = v1 + v2
                case 2:
                    v1, v2 = variables
                    res = v1 * v2
                case 3:
                    res = next(inputs)
                case 4:
                    output = variables[0]
                    return output
                case 5|6:
                    v1, v2 = variables
                    if bool(v1) == (opcode==5):
                        self.pointer=v2
                case 7:
                    v1, v2 = variables
                    res = int(v1 < v2)
                case 8:
                    v1, v2 = variables
                    res = int(v1 == v2)
                case 9:
                    v1 = variables[0]
                    self.relative_base += v1
                case 99:
                    raise StopIteration
                case _:
                    raise ValueError(f"Unknown opcode {opcode}")

            if write_res:
                res_addr = self._get_loc(parameters[-1],parameter_modes[-1])
                self._write(res_addr,res)
