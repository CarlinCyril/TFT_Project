from bisect import insort
from itertools import combinations
from multiprocessing.pool import Pool
from typing import List, Dict, Iterable
from argparse import ArgumentParser

from Champion_Data import Champion, Composition
from Trait import Trait, SetTrait
from Parser import ParserTFT


class Main:
    def __init__(self, champions: List[Champion], traits: Dict[str, Trait]):
        self.champions = champions
        self.traits = traits

    def custom_combinations(self, r: int) -> List[Composition]:
        first_compo = Composition(next(combinations(self.champions, r)), self.traits)
        list_combinations = [first_compo]
        for tuple_champions in combinations(self.champions, r):
            new_compo = Composition(tuple_champions, self.traits)
            if new_compo.score > list_combinations[-1].score:
                if len(list_combinations) >= 10:
                    _ = list_combinations.pop(-1)
                insort(list_combinations, new_compo)
        return list_combinations

    def run(self):
        compositions_by_level = dict()
        print("Computing all combinations of all {} champions".format(len(self.champions)))
        # print("Compositions of 7 champions")
        pool = Pool(processes=3)
        combinations_of_7, combinations_of_8, combinations_of_9 = \
            pool.map(self.custom_combinations, (7, 8, 9))

        compositions_by_level[7] = combinations_of_7
        compositions_by_level[8] = combinations_of_8
        compositions_by_level[9] = combinations_of_9

        compositions_by_level[7] = self.custom_combinations(7)
        compositions_by_level[8] = self.custom_combinations(8)
        compositions_by_level[9] = self.custom_combinations(9)

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
