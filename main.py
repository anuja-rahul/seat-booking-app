from handler import BookingHandler

test = BookingHandler(name="TestUser", password="TestPassword", row="A", column="1")
test.book_seat()
print(dir(test))
