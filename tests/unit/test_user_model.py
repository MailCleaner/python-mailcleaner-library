from mailcleaner import User

from mailcleaner.db.models.User import UserFactory


def test_create_user(session):
    user = UserFactory.create()
    assert User.find_by_username(user.username) is not None
