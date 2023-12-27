from intcode import IntCode, read_program_for_puzzle, read_program_string

program5 = read_program_for_puzzle(5)

ans1 = IntCode(program5).run_test(1)
print(f"{ans1=}")

# 5.2 ex
inp = """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""

program = read_program_string(inp)
assert IntCode(program).run(8) == 1000
assert IntCode(program).run(7) == 999
assert IntCode(program).run(99) == 1001

# 5.2
ans2 = IntCode(program5).run(5)
print(f"{ans2=}")
