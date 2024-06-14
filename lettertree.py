from random import sample

class LetterTreeNode:
    def __init__(self, contents: str):
        self.contents: str = contents
        self.children: dict[str, LetterTreeNode] = {}
    
    def __repr__(self):
        return f"{self.contents} ({', '.join(self.children.keys())})"

class LetterTree:
    def __init__(self, prompt_length: int=3):
        self.root: LetterTreeNode = LetterTreeNode("")
        self.prompt_length: int = prompt_length
        self.short_root: LetterTreeNode = LetterTreeNode("")

    def __repr__(self):
        lines = []
        self._repr_helper(self.root, False, level=0, prompt="", lines=lines, limit=0) # can change limit
        lines.sort()
        return "\n".join(lines) # can replace with ", " for csv

    """ Set node->short_root and short to True to print short words
        Limit: max number of solutions to display per prompt. -1 = all """
    def _repr_helper(self, node: LetterTreeNode, short: bool, level: int, prompt: str, lines: list[str], limit: int=-1):
        if level == self.prompt_length - 1 if short else self.prompt_length:
            solutions = [node.contents for node in node.children.values()]
            line = f"{prompt.upper()} ({len(solutions)})"
            limited = False
            if limit > 0 and limit < len(solutions):
                solutions = sample(solutions, limit) # randomly select limit # of solves
                limited = True
            if limit != 0:
                solutions_str = ", ".join(self.format_list(solutions))
                line += f": {solutions_str}"
                if limited:
                    line += ", ..."
            lines.append(line)
        for char, child in node.children.items():
            if len(char) == 1:
                self._repr_helper(child, short, level + 1, prompt + char, lines, limit)

    """ Inserts a word into the letter tree for a given prompt.
        If len(prompt) < self.prompt_length, inserts word into short_root tree"""
    def insert(self, word: str, prompt: str):
        node: LetterTreeNode = self.root if len(word) >= self.prompt_length else self.short_root

        for i in range(min(len(prompt), self.prompt_length)):
            char = prompt[i]
            if char not in node.children:
                node.children[char] = LetterTreeNode(char)
            node = node.children[char]
        if word not in node.children:
            node.children[word] = LetterTreeNode(word)

    """ Finds solves for the given prompt.
        If prompt length does not match lettertrie's prompt length,
         uses get_solves_short_prompt (see below) """
    def get_solves(self, prompt: str) -> list[str]:
        if len(prompt) != self.prompt_length:
            return self.get_solves_short_prompt(prompt)
        
        node: LetterTreeNode = self.root

        for i in range(self.prompt_length):
            char = prompt[i]
            if char not in node.children:
                return []
            node = node.children[char]

        return self.format_list(sorted(node.children))
    
    def get_solves_short_prompt(self, prompt: str) -> list[str]:
        if len(prompt) > self.prompt_length or len(prompt) == 0:
            return []
        solutions = []
        self._get_solves_short_prompt_helper(prompt, self.root, False, all_solutions=solutions)
        short_solutions = []
        self._get_solves_short_prompt_helper(prompt, self.short_root, True, all_solutions=short_solutions)
        solutions.extend(short_solutions)
        return self.format_list(solutions)

    def _get_solves_short_prompt_helper(self, search_prompt: str, node: LetterTreeNode, short: bool, all_solutions: list[str], level: int=0, tree_prompt: str=""):
        # if (level == self.prompt_length - 1 if short else self.prompt_length): # bottom level
        if node.children and len([sn for sn in node.children.values()][0].contents) > 1:
            if search_prompt in tree_prompt: # subprompt match
                solutions = [node.contents for node in node.children.values()]
                all_solutions.extend(solutions)
        for char, child in node.children.items():
            if len(char) == 1:
                self._get_solves_short_prompt_helper(search_prompt, child, short, all_solutions, level + 1, tree_prompt + char)
    
    @staticmethod
    def format_list(l: list) -> list:
        l = list(set(l))
        l.sort(key=len, reverse=True)
        return l
    