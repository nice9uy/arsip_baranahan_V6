def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "nip": str(user["nip"]),
        "nama": str(user["nama"]),
        "password": str(user["password"]),
        "is_active": bool(user["is_active"]),
        "join_date": int(user["join_date"]),
    }


def all_user(users) -> dict:
    return [user_serializer(user) for user in users]
