import datetime
import random

from tortoise.models import Model
from tortoise import fields
from enum import Enum, IntEnum


class AlignementLaw(IntEnum):
    lawful = 1
    neutral = 2
    chaotic = 3


class AlignementGood(IntEnum):
    good = 1
    neutral = 2
    evil = 3


class Isolation(IntEnum):
    """The closer to 0 the most isolated they become"""
    lives_in_bunker = 1
    stays_at_home_country = 10
    stays_at_home_city = 15
    works_from_home = 20
    essential_worker = 20
    normal_life = 25
    construction_worker = 30
    medical_personnel = 35
    goes_to_parties = 40


class Player(Model):
    discord_id = fields.BigIntField(pk=True)
    discord_name = fields.CharField(max_length=200)

    percent_infected = fields.IntField(default=0)

    cured = fields.BooleanField(default=False)
    doctor = fields.BooleanField(default=False)
    immunodeficient = fields.BooleanField(default=False)

    total_infected_points = fields.IntField(default=0)
    total_cured_points = fields.IntField(default=0)
    maximum_infected_points = fields.IntField(default=0)

    isolation = fields.IntEnumField(Isolation, default=Isolation.normal_life)

    touched_last = fields.DatetimeField(auto_now_add=True)

    good = fields.IntEnumField(AlignementGood)
    law = fields.IntEnumField(AlignementLaw)
    charisma = fields.IntField()

    inventory: fields.ReverseRelation["Inventory"]
    achievements: fields.ReverseRelation["Achievements"]
    statistics: fields.ReverseRelation["Statistics"]

    def is_dead(self) -> bool:
        return self.percent_infected >= 100

    def is_infected(self) -> bool:
        return self.percent_infected > 0

    def can_be_touched(self) -> bool:
        if not self.is_dead():
            return self.touched_last + datetime.timedelta(hours=3) < datetime.datetime.utcnow()
        else:
            return self.touched_last + datetime.timedelta(hours=1) < datetime.datetime.utcnow()

    def infect(self, add_infected: int = None) -> None:
        if add_infected is None:
            add_infected = random.randint(1, 8)

        if self.achievements.vaccined:
            add_infected = min(0, add_infected)

        self.total_infected_points += max(0, add_infected)
        self.total_cured_points -= min(0, add_infected)
        self.percent_infected += add_infected
        self.percent_infected = max(self.percent_infected, 0)
        self.maximum_infected_points = max(self.maximum_infected_points, self.percent_infected)

        if self.total_infected_points >= 50 and self.percent_infected == 0:
            self.cured = True

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.discord_name


class Inventory(Model):
    player: fields.OneToOneRelation[Player] = fields.OneToOneField(
        "models.Player", on_delete=fields.CASCADE, related_name="inventory", pk=True
    )

    education = fields.BigIntField(default=1)
    knowledge_points = fields.BigIntField(default=0)
    working_points = fields.BigIntField(default=0)
    research_points = fields.BigIntField(default=0)
    money = fields.BigIntField(default=0)  # Comes from work
    soap = fields.IntField(default=1)  # Can be bought
    food = fields.IntField(default=2)  # Can be bought
    airplane_ticket = fields.IntField(default=0)  # Can be bought
    lottery_ticket = fields.IntField(default=0)  # Can be bought
    herb = fields.IntField(default=0)  # Can be found
    music_cd = fields.IntField(default=0)  # Can be found
    pill = fields.IntField(default=0)  # Can be given to by doctors
    vaccine = fields.IntField(default=0)  # Can be given to by doctors
    mask = fields.IntField(default=0)  # Can be given to by doctors
    toilet_paper = fields.IntField(default=6)  # Can be used only
    gun = fields.IntField(default=0)  # Can be used only
    dagger = fields.IntField(default=1)  # Can be used only
    virus_test = fields.IntField(default=0)  # Can be given to by doctors


class ItemsEmojis(Enum):
    education = "🧠"
    knowledge_points = "🔬"
    working_points = "🛠"
    money = "💰"
    soap = "🧼"
    food = "🥔"
    herb = "🌿"
    music_cd = "💿"
    pill = "💊"
    vaccine = "💉"
    mask = "😷"
    airplane_ticket = "✈"
    lottery_ticket = "🎫"
    toilet_paper = "🧻"
    gun = "🔫"
    dagger = "🔪"
    virus_test = "📊"


class Achievements(Model):
    player: fields.OneToOneRelation[Player] = fields.OneToOneField(
        "models.Player", on_delete=fields.CASCADE, related_name="achievements", pk=True
    )
    hospital_stay = fields.BooleanField(default=False)
    it_was_just_a_cold = fields.BooleanField(default=False)
    symptoms = fields.BooleanField(default=False)
    bad_symptoms = fields.BooleanField(default=False)
    tested_positive = fields.BooleanField(default=False)
    vaccined = fields.BooleanField(default=False)
    suicided = fields.BooleanField(default=False)
    murderer = fields.BooleanField(default=False)
    victim = fields.BooleanField(default=False)
    died = fields.BooleanField(default=False)
    cured = fields.BooleanField(default=False)
    traveler = fields.BooleanField(default=False)
    back_from_the_dead = fields.BooleanField(default=False)


class AchievementsEmojis(Enum):
    hospital_stay = "🏥"
    it_was_just_a_cold = "🤧"
    symptoms = "🤢"
    bad_symptoms = "🤮"
    tested_positive = "🦠"
    vaccined = "💉"
    suicided = "💀"
    murderer = "🔫"
    victim = "☮"
    died = "☣"
    cured = "🕶️"
    traveler = "✈️"
    back_from_the_dead = "⛪️"


class Statistics(Model):
    player: fields.OneToOneRelation[Player] = fields.OneToOneField(
        "models.Player", on_delete=fields.CASCADE, related_name="statistics", pk=True
    )
    worked_times = fields.BigIntField(default=0)
    researched_times = fields.BigIntField(default=0)
    hugs_given = fields.BigIntField(default=0)
    hugs_recived = fields.BigIntField(default=0)
    made_vaccines = fields.BigIntField(default=0)
    heals = fields.BigIntField(default=0)
    been_eaten_times = fields.BigIntField(default=0)
    eaten_brains = fields.BigIntField(default=0)
