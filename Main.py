import sys
from bisect import insort

from itertools import combinations
from math import factorial
from multiprocessing.pool import Pool
from typing import List, Dict
from argparse import ArgumentParser

from Champion_Data import Champion, Composition
from Trait import Trait
from Parser import ParserTFT


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end, file=sys.stderr)
    # Print New Line on Complete
    if iteration == total:
        print()


class Main:
    def __init__(self, champions: List[Champion], traits: Dict[str, Trait]):
        self.champions = champions
        self.traits = traits

    def custom_combinations(self, r: int) -> List[Composition]:
        print("Computing combinations of {} champions".format(r), file=sys.stderr)
        first_compo = Composition(next(combinations(self.champions, r)), self.traits)
        list_combinations = [first_compo]

        n = len(self.champions)
        it = 1
        complexity = factorial(n)/(factorial(r) * factorial(n - r))

        if r == 9:
            print_progress_bar(it, complexity, prefix='Progress:', suffix='Complete', length=100)

        for tuple_champions in combinations(self.champions, r):
            it += 1
            new_compo = Composition(tuple_champions, self.traits)
            if new_compo.score > list_combinations[-1].score and len(list_combinations) > 11:
                _ = list_combinations.pop(-1)
                insort(list_combinations, new_compo)
            elif len(list_combinations) < 11:
                insort(list_combinations, new_compo)

            if r == 9:
                print_progress_bar(it, complexity, prefix='Progress:', suffix='Complete', length=100)
        print(file=sys.stderr)
        return list_combinations

    def run(self):
        compositions_by_level = dict()
        print("Computing all combinations of all {} champions".format(len(self.champions)), file=sys.stderr)
        # print("Compositions of 7 champions")
        pool = Pool(processes=3)
        combinations_of_7, combinations_of_8, combinations_of_9 = \
            pool.map(self.custom_combinations, (7, 8, 9))  # type: List[Composition]

        combinations_of_7.reverse()
        combinations_of_8.reverse()
        combinations_of_9.reverse()

        compositions_by_level[7] = combinations_of_7
        compositions_by_level[8] = combinations_of_8
        compositions_by_level[9] = combinations_of_9

        # compositions_by_level[7] = self.custom_combinations(7)
        # compositions_by_level[8] = self.custom_combinations(8)
        # compositions_by_level[9] = self.custom_combinations(9)

        for level, composition in compositions_by_level.items():
            print("########################################")
            print("############### LEVEL {} ###############".format(level))
            print("########################################")
            print(composition.__repr__())


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--trait", help="Path to the Trait file you want to parse")
    parser.add_argument("-c", "--champ", help="Path to the Champion file you want to parse")
    args = parser.parse_args()
    tft_parser = ParserTFT(file_traits=args.trait, file_champions=args.champ)
    parsed_champions = tft_parser.champion_parser()
    parsed_traits = tft_parser.trait_parser()
    main = Main(parsed_champions, parsed_traits)
    
    main.run()
