import pytest


def pytest_bdd_apply_tag(tag, function):
    # strict: once a gap is fixed the scenario fails, so its row gets moved to the right table
    if tag == "known_gap":
        pytest.mark.xfail(reason="known grader gap", strict=True)(function)
        return True
    return None
