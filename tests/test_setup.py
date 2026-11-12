from app import get_app_title


def test_app_title_mentions_project_name() -> None:
    title = get_app_title()
    assert "SocraticCode" in title
    assert "AI Tutor" in title
