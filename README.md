[Advent of code](https://adventofcode.com/)


Uses [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data) to get the inputs and submit results.

It needs to know your session ID. I'm using [python-dotenv] to read them from `\.env`, which looks like this:
```sh
AOC_SESSION=your_session_id
```
Altenatively, just permanently set the env variable or store the session id in `Path.home() / ".config/aocd/token"`.
See [here](https://github.com/wimglenn/advent-of-code-wim/issues/1) how to get the token.


Run `python utils/create_file.py` to create a file for the next exercise