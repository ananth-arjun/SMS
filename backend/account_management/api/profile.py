from fastapi import FastAPI, HTTPException
from controller.profile import ProfileController
from model import user_schema
app = FastAPI()

@app.get("/my-profile")
def profile(id: str):
    """Get Request - My Profile

    Returns:
        _type_: _description_
    """
    my_profile = ProfileController().get_profile(id)
    return my_profile
@app.get("/profiles")
def profile_list():
    """
    Get Request - Profile List
    Returns:
        _type_: _description_
    """
    profile_list = ProfileController().get_profiles()
    
    return profile_list

@app.post("/create-profile")
def create_profile(profile_data: user_schema.UserCreate):
    try:
        response =  ProfileController().create_profile(profile_data)   # only pass the data
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating profile: {str(e)}")
    
@app.get("/roles")
def get_roles():
    """
    Get Request - Roles List
    Returns:
        _type_: _description_
    """
    roles = ProfileController().get_roles()
    return roles