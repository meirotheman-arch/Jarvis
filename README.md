# Jarvis

Mon assistant personnel, construit sur [OpenJarvis](https://github.com/open-jarvis/OpenJarvis)
(licence Apache-2.0). Il fonctionne en local avec Ollama et répond en français.
Aucune donnée d'utilisation n'est envoyée.

## Installation

Prérequis : Python 3.11 à 3.13, [uv](https://docs.astral.sh/uv/) et [Ollama](https://ollama.com).

```bash
ollama pull qwen3.5:4b
uv sync --extra dev
```

## Utilisation

```bash
uv run jarvis-ai demande "Quelle heure est-il à Montréal ?"
uv run jarvis-ai discute
uv run jarvis-ai --model qwen3.5:9b discute
```

La commande s'appelle `jarvis-ai` et non `jarvis`, car OpenJarvis installe déjà sa
propre commande `jarvis` (toujours disponible à côté).

## Organisation

| Chemin | Contenu |
|--------|---------|
| `config/config.toml` | Moteur, modèle, agent, outils activés, consignes de Jarvis |
| `src/jarvis/tools.py` | Outils personnalisés (enregistrés dans le `ToolRegistry` d'OpenJarvis) |
| `src/jarvis/cli.py` | La commande `jarvis-ai` |
| `tests/` | Tests (`uv run pytest`) |

## Ajouter un outil

1. Dans `src/jarvis/tools.py`, ajoutez une sous-classe de `BaseTool` décorée par
   `@ToolRegistry.register("nom")`.
2. Ajoutez `nom` à `agent.tools` dans `config/config.toml`.

L'outil `web_search` accède à Internet : retirez-le de `agent.tools` pour un Jarvis entièrement hors ligne.

OpenJarvis est épinglé sur un commit précis dans `pyproject.toml` ; changez le hash pour le mettre à jour.
