from datetime import datetime
from zoneinfo import ZoneInfo

from openjarvis.core.registry import ToolRegistry

from jarvis.tools import OutilHeureActuelle, formater_date


def test_outil_enregistre():
    assert ToolRegistry.contains("current_time")


def test_heure_locale():
    resultat = OutilHeureActuelle().execute()
    assert resultat.success
    assert resultat.content


def test_fuseau_nomme():
    resultat = OutilHeureActuelle().execute(timezone="Asia/Tokyo")
    assert resultat.success
    assert "JST" in resultat.content


def test_fuseau_inconnu():
    resultat = OutilHeureActuelle().execute(timezone="Pas/UnFuseau")
    assert not resultat.success
    assert "inconnu" in resultat.content


def test_format_francais():
    moment = datetime(2026, 11, 24, 9, 5, 3, tzinfo=ZoneInfo("Europe/Paris"))
    assert formater_date(moment) == "mardi 24 novembre 2026, 09:05:03 CET (UTC+01:00)"
