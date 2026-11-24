"""Outils personnalisés de Jarvis.

Importer ce module enregistre chaque outil dans le ToolRegistry d'OpenJarvis,
pour que les agents puissent l'utiliser par son nom (voir ``agent.tools``
dans config/config.toml). Ajoutez vos nouveaux outils ici sur le même modèle.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def formater_date(moment: datetime) -> str:
    """Formate une date en français, sans dépendre de la locale du système."""
    decalage = moment.strftime("%z")
    decalage = f"{decalage[:3]}:{decalage[3:]}" if decalage else ""
    fuseau = moment.tzname() or ""
    return (
        f"{JOURS[moment.weekday()]} {moment.day} {MOIS[moment.month - 1]} {moment.year}, "
        f"{moment:%H:%M:%S} {fuseau} (UTC{decalage})"
    ).strip()


@ToolRegistry.register("current_time")
class OutilHeureActuelle(BaseTool):
    """Donne la date et l'heure actuelles, éventuellement dans un fuseau horaire donné."""

    tool_id = "current_time"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="current_time",
            description=(
                "Donne la date et l'heure actuelles. Accepte en option un fuseau "
                "horaire IANA, par exemple 'Europe/Paris' ou 'America/Montreal'."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Nom du fuseau horaire IANA (par défaut : heure locale)",
                    },
                },
                "required": [],
            },
            category="utilitaire",
        )

    def execute(self, **params: Any) -> ToolResult:
        fuseau = (params.get("timezone") or "").strip()
        try:
            maintenant = datetime.now(ZoneInfo(fuseau)) if fuseau else datetime.now().astimezone()
        except (ZoneInfoNotFoundError, ValueError):
            return ToolResult(
                tool_name="current_time",
                content=f"Fuseau horaire inconnu : {fuseau!r}",
                success=False,
            )
        return ToolResult(tool_name="current_time", content=formater_date(maintenant), success=True)


__all__ = ["OutilHeureActuelle", "formater_date"]
