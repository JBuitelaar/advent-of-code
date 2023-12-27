# Solution of Intcode problems (2/5/7)
# Try to find a nice solution, but the yields make it pretty ugly.
# probaby better just to return the state of the program and the pointer
# especially because we need to be able to provide new inputs anyway.
import itertools
from aocd.models import Puzzle

def read_data(values_str):
    return [int(v) for v in values_str.strip().split(',')]

def read_program(puzzle_no):
    puzzle = Puzzle(2019,puzzle_no)
    data = puzzle.input_data
    # data = "1,9,10,3,2,3,11,0,99,30,40,50"
    return read_data(data)

instruction_sizes = {  # instruction sizes and #variables
    1: (4,2),
    2: (4,2),
    3: (2,0),
    4: (2,1),
    5: (3,2),
    6: (3,2),
    7: (4,2),
    8: (4,2),
    99: (1,0)
}
class IntCode:
    """IntCode VM"""

    def __init__(self,program):
        self.memory = list(program).copy()
        self.pointer = 0

    def run_test(self,input_val):
        """test returns 0 outputs until a final exit code"""
        while True:
            output = self.run(input_val)
            if output:
                assert self.memory[self.pointer]==99
                return output


    def run(self,inputs=None):
        # run the program. Stops at and retuns the next output, or raises a GeneratorExit
        memory = self.memory

        if inputs is not None:
            if isinstance(inputs,int):
                inputs = [inputs]
            input_pointer = 0

        while True:
            inp=memory[self.pointer]
            opcode = inp%100
            if opcode == 99:
                raise GeneratorExit

            instr_size,var_size = instruction_sizes[opcode]
            parameters = memory[self.pointer+1:self.pointer+instr_size]

            # 0: position mode
            # 1: immediate mode
            parameter_modes = [(inp//10**d)%10 for d in range(2,instr_size+1)]
            assert set(parameter_modes)<={0,1},parameter_modes

            if var_size:
                vars = [ix if pmode==1 else memory[ix] for pmode,ix in zip(parameter_modes,parameters[:var_size])]

            self.pointer += instr_size

            if opcode==4:
                output = vars[0]
                return output
            
            if instr_size-var_size==2:
                assert parameter_modes[-1]==0
                res_addr = parameters[-1]

            if opcode == 1:
                v1,v2 = vars
                res  = v1+v2
                memory[res_addr] = res
            elif opcode == 2:
                v1,v2 = vars
                res  = v1*v2

                memory[res_addr] = res
            elif opcode==3:
                input_val = inputs[input_pointer]
                input_pointer+=1
                memory[res_addr]=input_val
            elif opcode in (5,6):
                v1,v2=vars
                if bool(v1)== (opcode==5):
                    self.pointer=v2
            elif opcode==7:
                v1,v2=vars
                memory[res_addr] = int(v1<v2)
            elif opcode==8:
                v1,v2=vars
                memory[res_addr] = int(v1==v2)
            else:
                raise(ValueError(f"Unknown opcode {opcode}"))


print("2019.2")
def run2(program,inputs=None):
    vm = IntCode(program)
    try:
        vm.run(inputs)
    except GeneratorExit:
        return vm.memory[0]

program2 = read_program(2)

def solve(noun,verb):
    program2[1] = noun
    program2[2] = verb
    return run2(program2)

ans1=solve(12,2)

assert ans1==4462686,ans1
print(f"{ans1=}")

def solve2():
    for noun in range(100):
        for verb in range(100):
            if solve(noun,verb)==19690720:
                return 100*noun+verb

ans2 = solve2()
print(f"{ans2=}")
assert ans2==5936,ans2

print("2019.5")
program5 = read_program(5)

ans1 = IntCode(program5).run_test(1)
print(f"{ans1=}")
assert ans1==13210611,ans1

# 5.2 ex
inp = """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""

program = read_data(inp)
assert IntCode(program).run(8) == 1000
assert IntCode(program).run(7) == 999
assert IntCode(program).run(99) == 1001

# 5.2
ans2 = IntCode(program5).run(5)
print(f"{ans2=}")
assert ans2 == 584126, ans2

print("2019.7")
# 7.1 example:
program = read_data("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")

seq= [1,0,4,3,2]
input = 0
for phase in seq:
    input = IntCode(program).run([phase,input])
assert input == 65210,input

# # 7.1:
program7 = read_program(7)

ans1 = 0
for seq in itertools.permutations(range(5)):
    input = 0
    for phase in seq:
        input = IntCode(program7).run([phase,input])
    if input>ans1:
        ans1 = input

print(f"{ans1=}")
assert 22012==ans1


# 7.2 ex 1

def run72(program,seq):
    vms = []
    val = 0
    for phase in seq:
        p = IntCode(program)
        vms.append(p)
        val = p.run([phase,val])

    def run_until_done(vms,input):
        while True:
            for vm in vms:
                try:
                    input = vm.run(input)
                except GeneratorExit:
                    return input

    return run_until_done(vms,val)

program = read_data("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
seq = [9,8,7,6,5]
res = run72(program,seq)
assert res == 139629729,input

input_str = """3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"""
program=read_data(input_str)
seq = [9,7,8,5,6]
res = run72(program,seq)
assert res == 18216,input


list(range(5,10))
ans2 = 0
for seq in itertools.permutations(range(5,10)):
    res = run72(program7,seq)
    if res>ans2:
        ans2 = res

print(f"{ans2=}")
assert ans2==4039164,ans2
