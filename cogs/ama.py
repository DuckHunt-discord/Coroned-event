import time

import discord
from discord.ext import commands

from utils.cog_class import Cog
from utils.ctx_class import MyContext


class AMA(Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.questions = []

    @commands.command()
    async def ask(self, ctx: MyContext, *, your_question:str):
        """
        Ask a question about the bot. They will get answered at the end of the event.
        """
        self.questions.append((ctx, your_question))
        await ctx.send("👌 Question recorded.")

    @commands.command()
    async def questions(self, ctx: MyContext):
        """
        List the questions asked.
        """

        if len(self.questions) == 0:
            await ctx.send(content="No questions :)")
            return

        i = 0
        message = []
        for q_ctx, q_str in self.questions:
            message.append(f"{i}: {q_str}")
            i += 1
        await ctx.send(content="\n".join(message))

    @commands.command()
    @commands.is_owner()
    async def answer(self, ctx: MyContext, question_id:int, *, a_str:str):
        """
        Answer a question and post it in the specified channel
        """
        q_ctx, q_str = self.questions.pop(question_id)

        await (ctx.guild.get_channel(self.config()['ama_channel_id']).send(f"Q: **{q_str}** (By {q_ctx.author.mention})\nA: {a_str}"))

        await ctx.send(content="👌", delete_after=15)




setup = AMA.setup
