from royalnet.commands import *


class EatCommand(Command):
    name: str = "eat"

    description: str = "Mangia qualcosa!"

    syntax: str = "{cibo}"

    _FOODS = {
        "_default": "🍗 Hai mangiato {food}!\n[i]Ma non è successo nulla.[/i]",
        "tonnuooooooro": "👻 Il {food} che hai mangiato era posseduto.\n[i]Spooky![/i]",
        "uranio": "☢️ L'{food} che hai mangiato era radioattivo.\n[i]Stai brillando di verde![/i]",
        "pollo": '🍗 Il {food} che hai appena mangiato proveniva dallo spazio.\n[i]Coccodè?[/i]',
        "ragno": "🕸 Hai mangiato un {food}.\n[i]Ewww![/i]",
        "curry": "🔥 BRUCIAAAAAAAAAA! Il {food} era piccantissimo!\n[i]Stai sputando fiamme![/i]",
        "torta": "⬜️ Non hai mangiato niente.\n[i]La {food} è una menzogna![/i]",
        "cake": "⬜️ Non hai mangiato niente.\n[i]The {food} is a lie![/i]",
        "biscotto": "🍪 Hai mangiato un {food} di contrabbando.\n[i]L'Inquisizione non lo saprà mai![/i]",
        "biscotti": "🍪 Hai mangiato tanti {food} di contrabbando.\n[i]Attento! L'Inquisizione è sulle tue tracce![/i]",
        "tango": "🌳 Hai mangiato un {food}, e un albero insieme ad esso.\n[i]Senti le tue ferite curarsi...[/i]",
        "giaroun": "🥌 Il {food} che hai mangiato era duro come un {food}.\n[i]Stai soffrendo di indigestione![/i]",
        "giarone": "🥌 Il {food} che hai mangiato era duro come un {food}.\n[i]Stai soffrendo di indigestione![/i]",
        "sasso": "🥌 Il {food} che hai mangiato era duro come un {food}.\n[i]Stai soffrendo di indigestione![/i]",
        "gnocchetti": "🥘 Ullà, sono duri 'sti {food}!\n[i]Fai fatica a digerirli.[/i]",
        "tide pod": "☣️ I {food} che hai mangiato erano buonissimi.\n[i]Stai sbiancando![/i]",
        "tide pods": "☣️ I {food} che hai mangiato erano buonissimi.\n[i]Stai sbiancando![/i]",
        "gelato": "🍨 Mangiando del {food}, hai invocato Steffo.\n[i]Cedigli ora il tuo gelato.[/i]",
        "tua mamma": "⚠️ Non sei riuscito a mangiare {food}.\n[i]Era troppo grande e non ci stava nella tua bocca![/i]",
        "mango": "🥭 Hai mangiato un {food}.\n[i]Ti sembra di avere più mana, adesso.[/i]",
        "mango incantato": "🥭 Hai mangiato un {food}.\n[i]Ti sembra di avere più mana, adesso.[/i]",
        "enchanted mango": "🥭 Hai mangiato un {food}.\n[i]Ti sembra di avere più mana, adesso.[/i]",
    }

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        food = args.joined(require_at_least=0)
        food_string = self._FOODS.get(food.lower(), self._FOODS["_default"])
        await data.reply(food_string.format(food=food.capitalize()))
