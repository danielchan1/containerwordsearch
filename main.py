from lettertree import LetterTree
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, PreTrainedTokenizer, PreTrainedTokenizerFast

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

def check_and_add(word: str, words: list[str], verbose: bool=True) -> int:
    word = word.strip().upper()
    word = ''.join([i for i in word if not i.isdigit()])
    if word in words:
        return 0
    else:
        if not verbose or input(f"{word} is not in the list. Add it? Y/N: ").upper() == 'Y':
            import bisect
            bisect.insort(words, word)
            if verbose:
                print(f"{word} was added.")
            return 1
        else:
            if verbose:
                print(f"{word} not added.")
            return 0

# use "containerwordsearch/english.txt" for prod and "english.txt" for dev
def save_all_words(num_new_words: int, all_words: list[str]):
    if num_new_words > 0:
        with open('english.txt', 'w') as f:
            for word in all_words:
                f.write(f"{word}\n")
        print(f"{num_new_words} new word{'' if num_new_words == 1 else 's'} added.")
    else:
        print("No new words added.")

""" def setup_ai(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return (tokenizer, model)
 
def ai_define_word(tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast, model, word: str) -> str:
    input_text = f"What is the definition of {word}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_new_tokens=70)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# uses AI to define word
def get_definition(word: str):
    model_id = "ltg/flan-t5-definition-en-large"
    (tokenizer, model) = setup_ai(model_id) 
    return ai_define_word(tokenizer, model, word) """

# use "containerwordsearch/english.txt" for prod and "english.txt" for dev
def create_letter_tree(filename: str="english.txt") -> LetterTree:
    lt: LetterTree = LetterTree()
    with open(filename) as file:
        for line in file:
            word = line.strip()
            all_words.append(word)
            if len(word) < lt.prompt_length:
                lt.insert(word, word) # short_root
            else:
                for prompt in extract_prompts(word):
                    lt.insert(word, prompt)
    return lt

all_words: list[str] = []
count = 0
try:
    # lt = create_letter_tree()
    # for printing mass solves to file
    """ with open('mostly_everything.txt', 'w') as f:
            print(repr(lt), file=f) """

    # for checking mass words from file
    """ with open('words_alpha.txt') as file:
        for line in file:
            word = line.strip()
            count += check_and_add(word, all_words, verbose=False)
    """
    
    # for checking words and their ai-generated definitions via console
    """ while True:
        word = input(f"Enter a word to check or '-save' ({count} added so far): ")
        if word == "-save":
            save_all_words(count, all_words)
            count = 0
        else:
            # print(get_definition(word))
            count += check_and_add(word, all_words) """
    
    # for getting solves via console
    num_solves = 20 # default max num solves
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

except KeyboardInterrupt:
    # save_all_words(count, all_words)
    pass
