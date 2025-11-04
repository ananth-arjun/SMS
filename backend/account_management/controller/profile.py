""" This controller handles the profile related operations """
import uuid
from model import db, users, user_schema
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
            return profiles
        finally:
            db_session.close()

    def create_profile(self, profile_data: user_schema.UserCreate):
        """ This function creates a new user profile in the database.
        Args:
            profile_data (dict): A dictionary containing user profile information.
        Returns:
            dict: A dictionary containing the created user profile information.

        """
         # Check email exists
        db_session = db.SessionLocal()
        response = {}
        try:
            existing = db_session.query(users.User).filter(users.User.email == profile_data.email).first()
            if existing:
                response["status"] = "error"
                response["message"] = "Email already exists"
                return response
            else:
                response["status"] = "success"
                response["message"] = "User Created!"
                user = users.User(
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
                db_session.add(user)
                db_session.flush()        # ✅ forces INSERT so user.id is generated
                db_session.refresh(user)  # ✅ makes sure user.id is populated
                userRoles = users.UserRole(
                    user_id=user.id,
                    role_id=profile_data.role_id,
                    assigned_on=datetime.now()
                )
                db_session.add(userRoles)
                db_session.commit()
                db_session.refresh(user)
                db_session.refresh(userRoles)
                print("Created User:", user.id)
                return response
        except Exception as e:
            db_session.rollback()
            response["status"] = "error"
            response["message"] = str(e)
            return response
        finally:
            db_session.close()
            

    def get_roles(self):
        """ This function retrieves all roles from the database.
        Returns:
            list: A list of dictionaries containing role information.

        """
        db_session = db.SessionLocal()
        try:
            roles = db_session.query(users.Role).all()
            # Convert to dicts OR use Pydantic in the route
            return roles
        except Exception as e:
            raise e
        finally:
            db_session.close()
        
        

       