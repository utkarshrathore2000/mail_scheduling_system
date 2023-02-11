def get_parcel_shipped_data(parcel):
    response_data = {"shipping_status": False, "shipping_cost": None}
    if parcel and parcel.cost:
        response_data = {"shipping_status": True, "shipping_cost": parcel.cost}
    return response_data
