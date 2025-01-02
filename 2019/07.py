import itertools
from intcode import IntCode, read_program_for_puzzle, read_program_string

# 7.1 example:
program = read_program_string("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")

seq= [1,0,4,3,2]
val = 0
for phase in seq:
    val = IntCode(program).run_simple([phase,val])
assert val == 65210,val

# # 7.1:
program7 = read_program_for_puzzle(7)

ans1 = 0
for seq in itertools.permutations(range(5)):
    val = 0
    for phase in seq:
        val = IntCode(program7).run_simple([phase,val])
    if val>ans1:
        ans1 = val

print(f"{ans1=}")
assert 22012==ans1


# 7.2 ex 1

def run72(program,seq):
    vms = []
    val = 0
    for phase in seq:
        p = IntCode(program)
        vms.append(p)
        val = p.next_output([phase,val])

    def run_until_done(vms,val):
        while True:
            for vm in vms:
                try:
                    val = vm.next_output(val)
                except StopIteration:
                    return val

    return run_until_done(vms,val)

# 7.2 examples:
program = read_program_string("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
seq = [9,8,7,6,5]
res = run72(program,seq)
assert res == 139629729,val

input_str = """3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"""
program=read_program_string(input_str)
seq = [9,7,8,5,6]
res = run72(program,seq)
assert res == 18216,val

# 7.2:
ans2 = 0
for seq in itertools.permutations(range(5,10)):
    res = run72(program7,seq)
    if res>ans2:
        ans2 = res

print(f"{ans2=}")
assert ans2==4039164,ans2
