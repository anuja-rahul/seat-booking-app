from handler import BookingHandler
import pprint

test = BookingHandler(name="TestUser1", password="TestPassword1", row="A", column="1")
# test.add_user()
print(test.check_credentials())
# pprint.pprint(dir(test))
