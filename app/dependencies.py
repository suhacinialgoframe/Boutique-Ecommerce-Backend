from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.security import SECRET_KEY, ALGORITHM


security = HTTPBearer()


# Verify JWT Token
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id = payload.get("user_id")


        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


        # Return complete token data
        return payload


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )



# Verify Admin Role
def verify_admin(
    user: dict = Depends(verify_token)
):

    if user.get("role") != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


    return user