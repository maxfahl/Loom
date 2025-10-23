def test_session_scope_one(session_scope_fixture):
    assert session_scope_fixture == "session_resource"

def test_session_scope_two(session_scope_fixture):
    assert session_scope_fixture == "session_resource"
