import json
from argparse import ArgumentParser
from itertools import combinations
from multiprocessing.pool import Pool
from typing import List, Dict

from Champion_Data import Champion, Composition
from Trait import Trait, SetTrait


class ParsingException(Exception):
    def __init__(self, message):
        super(ParsingException, self).__init__()
        self.message = message


class ParserTFT:

    def __init__(self, file_traits: str, file_champions: str):
        # list_traits, list_champions = None, None
        with open(file_traits) as traits:
            list_traits = json.load(traits)
        with open(file_champions) as champions:
            list_champions = json.load(champions)

        self.list_traits = list_traits
        self.list_champions = list_champions

    def trait_parser(self) -> Dict[str, Trait]:
        try:
            found_traits = dict()

            for trait in self.list_traits:
                milestones = list()

                for set_trait in trait.get("sets", []):
                    milestones.append(
                        SetTrait(
                            style=set_trait.get("style", "gold"),
                            min_level=set_trait.get("min", 0),
                            max_level=set_trait.get("max", 10)
                        )
                    )

                found_traits[trait["name"]] = Trait(
                    name=trait["name"],
                    description=trait.get("description", str()),
                    trait_id=trait.get("key", trait["name"]),
                    milestones=milestones
                )
            return found_traits
        except KeyError:
            raise ParsingException("Failed to parse Trait file.")

    def champion_parser(self) -> List[Champion]:
        try:
            found_champions = [
                Champion(
                    name=champ["name"],
                    champion_id=champ["championId"],
                    cost=champ["cost"],
                    traits=champ["traits"]
                )
                for champ in self.list_champions
            ]

            return found_champions
        except KeyError:
            raise ParsingException("Failed to parse Champion file.")


class Main:
    def __init__(self, champions: List[Champion], traits: Dict[str, Trait]):
        self.champions = champions
        self.traits = traits

    def run(self):
        compositions_by_level = dict()
        print("Computing all combinations of all {} champions".format(len(self.champions)))
        # print("Compositions of 7 champions")
        pool = Pool(processes=3)
        combinations_of_7, combinations_of_8, combinations_of_9 = \
            pool.starmap(combinations, [(self.champions, 7), (self.champions, 8), (self.champions, 9)])

        compos_of_7 = [Composition(champions_pool, self.traits) for champions_pool in combinations_of_7]
        # print("Compositions of 8 champions")
        compos_of_8 = [Composition(champions_pool, self.traits) for champions_pool in combinations_of_8]
        # print("Compositions of 9 champions")
        compos_of_9 = [Composition(champions_pool, self.traits) for champions_pool in combinations_of_9]

        print("Scoring each composition found")
        compositions_by_level[7] = sorted(compos_of_7, key=Composition.scoring, reverse=True)
        compositions_by_level[8] = sorted(compos_of_8, key=Composition.scoring, reverse=True)
        compositions_by_level[9] = sorted(compos_of_9, key=Composition.scoring, reverse=True)

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
