from openjarvis.core.registry import ToolRegistry

from myjarvis.tools import CurrentTimeTool


def test_registered():
    assert ToolRegistry.contains("current_time")


def test_local_time():
    result = CurrentTimeTool().execute()
    assert result.success
    assert result.content


def test_named_zone():
    result = CurrentTimeTool().execute(timezone="Asia/Tokyo")
    assert result.success
    assert "JST" in result.content


def test_bad_zone():
    result = CurrentTimeTool().execute(timezone="Not/AZone")
    assert not result.success
