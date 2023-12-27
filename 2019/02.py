from intcode import IntCode, read_program_for_puzzle

def run2(program,inputs=None):
    vm = IntCode(program)
    try:
        vm.next_output(inputs)
    except GeneratorExit:
        return vm.memory[0]

program2 = read_program_for_puzzle(2)

def run_with_edits(noun,verb):
    program2[1] = noun
    program2[2] = verb
    return run2(program2)

ans1=run_with_edits(12,2)
print(f"{ans1=}")

def solve2():
    for noun in range(100):
        for verb in range(100):
            if run_with_edits(noun,verb)==19690720:
                return 100*noun+verb

ans2 = solve2()
print(f"{ans2=}")
