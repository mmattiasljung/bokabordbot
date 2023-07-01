import requests
import json

get_times_url = "https://app.waiteraid.com/booking-widget/api/getTimes"
save_booking_url = "https://app.waiteraid.com/reservation/api/booking/saveBooking"

get_times_request = {
    "date_code": "",
    "hd_meal": "",
    "int_test": "N",
    "lang": "",
    "mc_code": "",
    "mealid": "7098",
    "testmode": 0
}

save_booking_request = {
    "ap_label": "",
    "bookingid": 0,
    "children_amount": None,
    "city": "",
    "comment": "",
    "country_code": "+46",
    "date_code": "",
    "dial_code": "+46",
    "from_url": "bokabord",
    "hd_meal": "",
    "length": 120,
    "linked_meal": False,
    "mc_code": "",
    "offer_ID": 0,
    "products": [],
    "saveinfo": 1,
    "segment": "",
    "temp_sid": "",
    "terms": {
        "general": True,
        "restaurant": False,
        "bokabord": False
    },
    "testmode": 0,
    "waitb": "",
    "waitlist": False,
    "waitlist_end": None,
    "widget_lang": "",
}


def get_times(restaurant, date, num_people):
    get_times_request["date"] = date
    get_times_request["amount"] = num_people
    get_times_request[restaurant["secret_key"]] = restaurant["secret_value"]
    get_times_request["hash"] = restaurant["hash"]
    get_times_request["mealid"] = restaurant["meal_id"]

    response = requests.post(get_times_url, json=get_times_request)

    times = clean_times(json.loads(response.content)["times"])
    lengths = clean_lengths(json.loads(response.content)["lengths"])

    return free_times_with_lengths(times, lengths)


def save_booking(restaurant, date, num_people, email, phone, first_name, last_name, time):
    save_booking_request["date"] = date
    save_booking_request["amount"] = num_people
    save_booking_request[restaurant["secret_key"]] = restaurant["secret_value"]
    save_booking_request["hash"] = restaurant["hash"]
    save_booking_request["mealid"] = restaurant["meal_id"]
    save_booking_request["email"] = email
    save_booking_request["phone"] = phone
    save_booking_request["firstname"] = first_name
    save_booking_request["lastname"] = last_name
    save_booking_request["time"] = time

    response = requests.post(save_booking_url, json=save_booking_request)
    return json.loads(response.content)


def clean_times(times):
    times_clean = []

    for key in times:
        times_clean.append(times[key][0])

    return times_clean


def clean_lengths(lengths):
    lengths_clean = {}

    for key in lengths:
        lengths_clean.update(lengths[key])

    return lengths_clean


def free_times_with_lengths(free_times, lengths):
    free_times_lengths = {}

    for time in free_times:
        free_times_lengths[time] = lengths[time]

    return free_times_lengths
