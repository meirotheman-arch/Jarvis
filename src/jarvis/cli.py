"""Commande `jarvis-ai` : `jarvis-ai demande "..."` ou `jarvis-ai discute`."""

from __future__ import annotations

import argparse
from pathlib import Path

import jarvis.tools  # noqa: F401  (enregistre les outils personnalisés)
from openjarvis import Jarvis

CONFIG_PAR_DEFAUT = Path(__file__).resolve().parents[2] / "config" / "config.toml"
MOTS_DE_SORTIE = {"exit", "quit", "quitter", "sortir", "au revoir"}


def _liste_outils(j: Jarvis) -> list[str]:
    return [t.strip() for t in j.config.agent.tools.split(",") if t.strip()]


def _demander(j: Jarvis, question: str) -> str:
    return j.ask(question, agent=j.config.agent.default_agent, tools=_liste_outils(j))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="jarvis-ai", description="Jarvis, assistant personnel", add_help=False)
    parser.add_argument("-h", "--help", action="help", help="afficher cette aide et quitter")
    parser.add_argument("--config", default=str(CONFIG_PAR_DEFAUT), help="chemin vers config.toml")
    parser.add_argument("--model", default=None, help="utiliser un autre modèle")
    sous = parser.add_subparsers(dest="commande", required=True, metavar="{demande,discute}")
    p_demande = sous.add_parser("demande", aliases=["ask"], help="poser une seule question")
    p_demande.add_argument("question", nargs="+")
    sous.add_parser("discute", aliases=["chat"], help="conversation (Ctrl-D ou « quitter » pour sortir)")
    args = parser.parse_args(argv)

    chemin_config = args.config if Path(args.config).exists() else None
    j = Jarvis(config_path=chemin_config, model=args.model)
    try:
        if args.commande in {"demande", "ask"}:
            print(_demander(j, " ".join(args.question)))
            return
        print("Jarvis est prêt. Tapez « quitter » pour sortir.")
        while True:
            try:
                ligne = input("vous> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if ligne.lower() in MOTS_DE_SORTIE:
                break
            if ligne:
                print(f"jarvis> {_demander(j, ligne)}\n")
    finally:
        j.close()


if __name__ == "__main__":
    main()
