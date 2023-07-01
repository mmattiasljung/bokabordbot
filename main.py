import bokabordapi
import restaurants
import time


def main():
    restaurant = restaurants.lilla_ego
    first_name = "Mattias"
    last_name = "Ljung"
    email = "malju_95@hotmail.com"
    phone = "0702190353"
    date = "2023-08-26"
    num_people = 2

    while not book_table_between(restaurant, "18:30", "19:30", date, num_people,
                                 email, phone, first_name, last_name):
        time.sleep(0.1)


def book_table_between(restaurant, time_earliest, time_latest, date, num_people, email, phone, first_name, last_name):
    times = bokabordapi.get_times(restaurant, date, num_people)

    for time in times:
        if is_before(time, time_earliest) or is_after(time, time_latest):
            continue

        response = bokabordapi.save_booking(
            restaurant, date, num_people, email, phone, first_name, last_name, time)

        if response["success"]:
            print("Successfully booked",
                  restaurant["name"], "on", date, "at", time)
            return True

    print("Failed to book", restaurant["name"])
    return False


def is_before(time, reference_time):
    time_stripped = time.replace(":", "")
    reference_time_stripped = reference_time.replace(":", "")

    return time_stripped < reference_time_stripped


def is_after(time, reference_time):
    time_stripped = time.replace(":", "")
    reference_time_stripped = reference_time.replace(":", "")

    return time_stripped > reference_time_stripped


if __name__ == '__main__':
    main()
