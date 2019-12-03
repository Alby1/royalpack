from typing import *
from royalnet.commands import *
from royalnet.utils import *
from royalnet.backpack.tables import User
from sqlalchemy import func
import royalspells as rs


class SpellCommand(Command):
    name: str = "spell"

    description: str = "Genera casualmente una spell!"

    syntax = "{nome_spell}"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        spell_name = args.joined(require_at_least=1)
        spell = rs.Spell(spell_name)

        rows: List[str] = [f"✨ [b]{spell.name}[/b]"]

        if spell.damage_component:
            dmg: rs.DamageComponent = spell.damage_component
            constant_str: str = f"{dmg.constant:+d}" if dmg.constant != 0 else ""
            rows.append(f"Danni: [b]{dmg.dice_number}d{dmg.dice_type}{constant_str}[/b]"
                        f" {andformat(dmg.damage_types, final=' e ')}")
            rows.append(f"Precisione: [b]{dmg.miss_chance}%[/b]")
            if dmg.repeat > 1:
                rows.append(f"Multiattacco: [b]×{dmg.repeat}[/b]")
            rows.append("")

        if spell.healing_component:
            heal: rs.HealingComponent = spell.healing_component
            constant_str: str = f"{heal.constant:+d}" if heal.constant != 0 else ""
            rows.append(f"Cura: [b]{heal.dice_number}d{heal.dice_type}{constant_str}[/b] HP")
            rows.append("")

        if spell.stats_component:
            stats: rs.StatsComponent = spell.stats_component
            rows.append("Il caster riceve: ")
            for stat_name in stats.stat_changes:
                rows.append(f"[b]{stats.stat_changes[stat_name]}{stat_name}[/b]")
            rows.append("")

        if spell.status_effect_component:
            se: rs.StatusEffectComponent = spell.status_effect_component
            rows.append("Infligge al bersaglio: ")
            rows.append(f"[b]{se.effect}[/b] ({se.chance}%)")
            rows.append("")

        await data.reply("\n".join(rows))
