from mailcleaner_db.models import User, Commtouch, WWLists

commtouch = Commtouch()
c = commtouch.all()
print(c)
newton = User.find_by_username_and_domain("newton", "toto.local")
print("Hello")
print(newton)
newton.username = "newton3"
newton.save()
print(newton)

wwlists = WWLists()
lists = wwlists.all()
print(lists)