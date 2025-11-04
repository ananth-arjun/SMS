""" This controller handles the profile related operations """
import uuid
from model import db, users
from core.security import hash_password
from datetime import datetime

class ProfileController:
    def __init__(self):
        pass
    def get_profile(self,user_id: str):
        """ This function retrieves the user profile from the database. 
        Args:
            user_id (str): The ID of the user whose profile is to be retrieved.
        Returns:
            dict: A dictionary containing user profile information.

        """
        db_session = db.SessionLocal()
        try:
            user_id = uuid.UUID(user_id)
            profile = db_session.query(users.User).filter(users.id == user_id).first()
            return profile
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid UUID string: {user_id}") from e
        finally:
            db_session.close()

    def get_profiles(self):
        """ This function retrieves all user profiles from the database.
        Returns:
            list: A list of dictionaries containing user profile information.

        """
        db_session = db.SessionLocal()
        try:
            profiles = db_session.query(users.User).all()
            # Convert to dicts OR use Pydantic in the route
            return [
            {
                "id": str(p.id),
                "first_name": p.first_name,
                "middle_name": p.middle_name,
                "last_name": p.last_name,
                "email": p.email,
                "is_active": p.is_active,
                "phone": p.phone,
                "address": p.address,
                "city": p.city,
                "state": p.state,
                "country": p.country,
            }
            for p in profiles
            ]
        finally:
            db_session.close()

    def create_profile(self, profile_data: dict):
        """ This function creates a new user profile in the database.
        Args:
            profile_data (dict): A dictionary containing user profile information.
        Returns:
            dict: A dictionary containing the created user profile information.

        """
         # Check email exists
        response = {}
        db_session = db.SessionLocal()
        existing = db_session.query(users.User).filter(users.User.email == profile_data.email).first()
        if existing:
            response["status"] = "error"
            response["message"] = "Email already exists"
            return response

        user = users(
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            email=profile_data.email,
            password=hash_password(profile_data.password),   # ✅ hash here before inserting
            phone=profile_data.phone,
            address=profile_data.address,
            country=profile_data.country,
            created_by=profile_data.created_by,
            created_on=datetime.now(),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user