from app.database import supabase

def sign_up(email: str, password: str, full_name: str, user_type: str, phone: str = None):

    auth_response = supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "full_name": full_name,
                "user_type": user_type
            }
        }
    })

    if auth_response.user is None:
        raise Exception("Error al registrar usuario")

    if phone:
        supabase.table("profiles").update({
            "phone": phone
        }).eq("id", auth_response.user.id).execute()

    return auth_response


def sign_in(email: str, password: str):

    auth_response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    return auth_response