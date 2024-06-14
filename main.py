from lettertree import LetterTree
# import os

def extract_prompts(word: str, prompt_length: int=3) -> list[str]:
    substrings: list[str] = []
    word = word.upper()
    for i in range(len(word)-prompt_length+1):
        substring = word[i:i+prompt_length]
        if substring.isalpha() and substring not in substrings:
            substrings.append(substring) # add unique, alphabetic substrings
    return substrings

def get_desired_solves(solves: list[str], num_solves: int=1) -> list[str]:
    from random import sample
    # num solves: number WANTED
    # len(solves): number CURRENTLY HAVE
    if num_solves <= 0 or num_solves > len(solves):
        num_solves = len(solves)

    # return solves[num_solves * -1:] # x shortest solves
    # return solves[:num_solves] # x longest solves

    if num_solves > 2: # x-2 random solves + longest + shortest
        middle_solves = solves[1:-1]
        all_solves = sample(middle_solves, num_solves - 2)
        all_solves.extend([solves[0], solves[-1]])
        return LetterTree.format_list(all_solves)
    else:
        return LetterTree.format_list(sample(solves, num_solves)) # x random solves

# https://stackoverflow.com/a/434328
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# os.system('cls') # clear screen windows
# print("Loading...")

def create_letter_tree(filename: str="english.txt") -> LetterTree:
    lt: LetterTree = LetterTree()
    with open(filename) as file:
        for line in file:
            word = line.strip()
            if len(word) < lt.prompt_length:
                lt.insert(word, word) # short_root
            else:
                for prompt in extract_prompts(word):
                    lt.insert(word, prompt)
    return lt

# lt = create_letter_tree()

# for printing mass solves to file
""" with open('mostly_everything.txt', 'w') as f:
    print(repr(lt), file=f) """

# os.system('cls') # clear screen windows
# print(lt)

# try:
#     num_solves = 20 # default max num solves
#     """ while True:
#         try:
#             str_solves = input("Number of solves, 0 for all: ").strip()
#             if str_solves == "":
#                 break
#             num_solves = int(str_solves)
#             break
#         except ValueError:
#             print("Please enter a number.") """

#     while True:
#         prompt = input("Enter prompt, CTRL+C to exit: ").strip().upper()
#         solves = lt.get_solves(prompt)
#         print(f"{len(solves)} {'word' if len(solves) == 1 else 'words'} found")
#         if len(solves) > 0:
#             desired_solves = get_desired_solves(solves, num_solves)
#             for group in chunker(desired_solves, 5):
#                 print(f"{', '.join(group)}")
#         print("")
# except KeyboardInterrupt:
#     print("\n\nGoodbye.")
