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
        "peperoncino": "🔥 BRUCIAAAAAAAAAA! Il {food} era piccantissimo!\n[i]Stai sputando fiamme![/i]",
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
        "musica": "🎶 Hai mangiato un po' di {food} mentre ascoltavi un buon pranzo.\n[i]Tutto ciò ha perfettamente"
                  " senso.[\i]",
        "fungo": "🍄 Hai mangiato un {food}.\n[i]Presto riuscirai a salvare Peach![/i]",
        "zucca": "🎃 Hai mangiato una {food}. Solo che era una lanterna di Halloween.\n[i]Inizi a fare luce al"
                 " buio.[/i]",
        "granchio": "🦀 Hai mangiato un {food}. {food} is gone!\n[i]Senti il tuo stomaco ballare.[/i]",
        "crab": "🦀 Hai mangiato un {food}. {food} is gone!\n[i]Senti il tuo stomaco ballare.[/i]",
        "veleno": "☠️ Hai mangiato del {food}. Perché lo hai fatto?\n[i]Adesso stai male, contento?[/i]",
        "polvere": "☁️ Hai mangiato la {food}.\n[i]Ti hanno proprio battuto![/i]",
        "diavolo": "👿 Hai mangiato un {food}. Non l'ha presa bene...\n[i]Hai terribili bruciori di stomaco.[/i]",
        "demone": "👿 Hai mangiato un {food}. Non l'ha presa bene...\n[i]Hai terribili bruciori di stomaco.[/i]",
        "niente": "⬜️ Non hai mangiato {food}.\n[i]Hai ancora più fame.[/i]",
        "nulla": "⬜️ Non hai mangiato {food}.\n[i]Hai ancora più fame.[/i]",
        "tutto": "👵🏻 Hai mangiato {food}. Si vede che hai gradito il pasto!\n[i]Tua nonna ti serve un'altra"
                 " porzione.[/i]",
        "caffè": "☕️ Oh, no! Questo era il {food} della Peppina!\n[i]Ha provato col tritolo, salti in aria col"
                 " caffè.[/i]",
        "caffé": "☕️ Oh, no! Questo era il {food} della Peppina!\n[i]Ha provato col tritolo, salti in aria col"
                 " caffè.[/i]",
    }

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        food = args.joined(require_at_least=1)
        food_string = self._FOODS.get(food.lower(), self._FOODS["_default"])
        await data.reply(food_string.format(food=food.capitalize()))
