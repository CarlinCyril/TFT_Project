import json
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

