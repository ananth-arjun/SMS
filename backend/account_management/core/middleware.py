from datetime import datetime, timezone
from typing import Annotated, Iterable, Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt  # PyJWT
import dotenv
dotenv.load_dotenv()
from pydantic import BaseModel
import os

# === Settings ===
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable must be set")

JWT_ALG = os.getenv("JWT_HS512_ALGORITHM")
JWT_AUDIENCE = "account-mgmt"
JWT_ISSUER = "account-mgmt-auth"

# === Models ===
class User(BaseModel):
    id: str
    email: str
    roles: list[str]

# === Bearer auth scheme ===
bearer = HTTPBearer(auto_error=False)

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALG],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
            options={"require": ["exp", "iat"]}
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# === Base dependency: must authenticate ===
async def current_user(
    request: Request,
    creds: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer)]
) -> User:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing bearer token")

    payload = decode_jwt(creds.credentials)

    # minimal claims → adapt to your IdP
    sub = payload.get("sub")
    email = payload.get("email")
    roles = payload.get("roles", [])
    if not sub or not email:
        raise HTTPException(status_code=401, detail="Malformed token")

    # (optional) additional checks
    now = datetime.now(timezone.utc).timestamp()
    if payload.get("nbf") and now < payload["nbf"]:
        raise HTTPException(status_code=401, detail="Token not yet valid")

    user = User(id=sub, email=email, roles=roles)
    request.state.user = user  # make available to handlers/middleware
    return user

# === Role check wrapper ===
def require_roles(*allowed: str):
    """
    Usage: Depends(require_roles("admin", "manager"))
    Pass no roles to just enforce auth.
    """
    async def checker(
        user: Annotated[User, Depends(current_user)]
    ) -> User:
        if not allowed:  # only auth required
            return user
        if not any(r in set(user.roles) for r in allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(allowed)}"
            )
        return user
    return checker
