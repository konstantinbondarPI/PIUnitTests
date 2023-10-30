
class HotelException(Exception):
    guest_already_settled = "Guest already settled"
    room_already_settled = "Room already settled"
    wrong_room = "Wrong room"

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Hotel:

    def __init__(self, rooms):
        self.__rooms = rooms
        self.__settledRooms = {}

    def free_rooms(self):
        return [room for room in self.__rooms if room not in self.__settledRooms.keys()]

    def settle(self, room, guest_id):
        if self.__check_if_guest_settled(guest_id):
            raise HotelException(HotelException.guest_already_settled)
        if room in self.__rooms:
            if self.__settledRooms[room] != guest_id:
                raise HotelException(HotelException.room_already_settled)
            self.__settledRooms[room] = guest_id
        else:
            raise HotelException(HotelException.wrong_room)

    def evict(self, guest_id):
        for room, room_guest_id in self.__settledRooms.items():
            if room_guest_id == guest_id:
                del self.__settledRooms[room]
                break

    def __check_if_guest_settled(self, guest_id):
        return guest_id in self.__settledRooms.values()


def prepare_hotel():
    return Hotel(rooms=[101, 102, 201, 202, 203, 301])


def test_init():
    hotel = prepare_hotel()
    assert len(hotel.free_rooms()) == 6


def test_settling():
    hotel = prepare_hotel()
    assert len(hotel.free_rooms()) == 5
    hotel.settle(101, 1)
    assert len(hotel.free_rooms()) == 5
    hotel.evict(1)
    assert len(hotel.free_rooms()) == 6


def test_settling_to_same_room():
    hotel = prepare_hotel()
    assert len(hotel.free_rooms()) == 5
    hotel.settle(101, 1)
    assert len(hotel.free_rooms()) == 5

    try:
        hotel.settle(101, 2)
    except HotelException as e:
        assert e.message == HotelException.room_already_settled


def test_settling_same_guest_twice():
    hotel = prepare_hotel()
    assert len(hotel.free_rooms()) == 5
    hotel.settle(101, 1)
    assert len(hotel.free_rooms()) == 5

    try:
        hotel.settle(202, 1)
    except HotelException as e:
        assert e.message == HotelException.guest_already_settled


def test_settling_to_wrong_room():
    hotel = prepare_hotel()

    try:
        hotel.settle(402, 1)
    except HotelException as e:
        assert e.message == HotelException.wrong_room
