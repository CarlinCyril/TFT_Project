from typing import List, Dict

from Trait import Trait


class Champion:
    def __init__(self, name: str, traits: List[str], cost: int, champion_id: str) -> None:
        self.name = name
        self.traits = traits
        self.cost = cost
        self.champion_id = champion_id

    def __eq__(self, other) -> bool:
        return isinstance(other, Champion) and self.champion_id == other.champion_id

    def __repr__(self):
        representation = """Name : {}
                            Cost : {}
                            Classes : {}""".format(self.name, self.cost, self.traits)
        return representation


class Composition:
    def __init__(self, champions: List[Champion], traits_model: Dict[str, Trait]):
        self.champions = champions
        self.synergies = dict()
        self.traits_model = traits_model
        self.score = 0
        self.compute_synergies()

    def __repr__(self):
        result = "~~~~~~~~~~~~~~~~ COMPOSITION ~~~~~~~~~~~~~~~~\n"
        result += "Score = {}\n".format(self.score)
        result += "----------- Synergies -----------\n"
        for trait, number in self.synergies.items():
            result += "{} --> {}\n".format(trait.__repr__(), number)

        result += "----------- Champions -----------\n"
        for champion in self.champions:
            result += champion.__repr__() + "\n"

        return result

    def compute_synergies(self):
        for champion in self.champions:
            for champ_trait in champion.traits:
                self.synergies[champ_trait] = self.synergies.get(champ_trait, 0) + 1

    def _score_milestone(self, trait_name) -> int:
        trait_number = self.synergies[trait_name]
        for milestone in self.traits_model[trait_name].milestones:
            if milestone.min_level < trait_number <= milestone.max_level:
                if milestone.style == "bronze":
                    return 10
                elif milestone.style == "silver":
                    return 20
                else:
                    return 30
            elif milestone.min_level == trait_number:
                if milestone.style == "bronze":
                    return 70
                elif milestone.style == "silver":
                    return 80
                else:
                    return 200
        return -100

    def scoring(self):
        self.score = 0
        for trait_name in self.synergies.keys():
            self.score += self._score_milestone(trait_name)
        return self.score
