from mailcleaner.db.models import Administrator
from mailcleaner.db.models.Administrator import AdministratorFactory


def test_create_administrator(session):
    admin = AdministratorFactory.create()
    print("Admin: {}".format(admin))
    print("Admin2: {}".format(Administrator.find_by_id(admin.id)))
    assert Administrator.find_by_username(admin.id) is not None
