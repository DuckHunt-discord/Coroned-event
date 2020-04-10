import asyncio
import random

import discord
from tortoise import Tortoise

from .models import Player, Achievements, Inventory, Statistics, AlignementGood, AlignementLaw


class Database:
    def __init__(self, bot):
        self.bot = bot

    async def init(self, url):
        await Tortoise.init(
            db_url=url,
            modules={'models': ['utils.models']}
        )
        # Generate the schema
        await Tortoise.generate_schemas()

    async def get_player(self, user: discord.User) -> Player:
        player = await Player.filter(discord_id=user.id).first()

        if not player:
            player = Player(discord_id=user.id,
                            discord_name=user.name,
                            immunodeficient=random.randint(0, 100) <= 15,
                            doctor=random.randint(0, 100) <= 2,
                            good=random.choice(list(AlignementGood)),
                            law=random.choice(list(AlignementLaw)),
                            charisma=random.randint(0, 10)
            )
            await player.save()
            inventory = Inventory(player=player)
            await inventory.save()
            achievements = Achievements(player=player)
            await achievements.save()
            statistics = Statistics(player=player)
            await statistics.save()

        await player.fetch_related('inventory', 'statistics', 'achievements')
        return player

    async def save_player(self, player: Player) -> None:
        await player.save()
        await player.inventory.save()
        await player.achievements.save()
        await player.statistics.save()


