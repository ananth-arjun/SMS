from fastapi import FastAPI
from controller.profile import ProfileController
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
def create_profile():
    return {"message": "Profile created!"}