from intcode import IntCode, read_program_for_puzzle, read_program_string

# examples:
program = read_program_string("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
vm = IntCode(program)
assert vm.run() == program
res = IntCode(read_program_string("1102,34915192,34915192,7,4,7,99,0")).next_output()
assert len(str(res))==16

program9 = read_program_for_puzzle(9)
ans1 = IntCode(program9).run_test(1)
print(f"{ans1=}")
assert ans1 == 2870072642, ans1

ans2=IntCode(program9).run_simple(2)
print(f"{ans2=}")
assert ans2==58534,ans2
