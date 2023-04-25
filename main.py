from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from db.crud import get_user_by_username, get_user_by_email, create_user, get_user_links, get_link_by_short_url
from db.models import User as UserModel, Link as LinkModel, LinkVisit as LinkVisitModel
from schemas.link import LinkCreate, Link
from schemas.user import User, UserCreate
from schemas.token import Token
from security.password import authenticate_user, get_password_hash
from security.token import create_access_token, get_current_active_user, get_current_active_user_links
import secrets
import string



def create_random_string(lenght: int = 6):
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(lenght))


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, request: Request):
    ip_address = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    existing_email = await get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    existing_username = await get_user_by_username(user.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")

    hashed_password = get_password_hash(user.password)
    new_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password,
                         user_ip=ip_address, user_agent=user_agent)
    await new_user.save()
    return {"message": "User created successfully"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/me/links/")
async def read_user_links(current_user: Annotated[User, Depends(get_current_active_user_links)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    if not current_user.user_links:
        return [current_user, {"message": "No links found"}]
    return current_user


@app.post("/users/me/links/")
async def create_user_link(link: LinkCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    i = None
    while i is None:
        random_string = create_random_string()
        link_exists = await LinkModel.get_or_none(xs_url=random_string)
        if not link_exists:
            i = random_string
    new_link = LinkModel(endpoint_url=link.endpoint_url, xs_url=i, owner_id=current_user.id)
    user = await UserModel.get(id=current_user.id)
    user_links = await user.fetch_related("links")
    if user_links:
        user.user_links.append(new_link)
    await user.save()
    await new_link.save()
    return Link.from_orm(new_link)


@app.post("/users/me/links/{link_id}")
async def edit_user_link(link_id: int, new_endpoint: str,
                         current_user: Annotated[User, Depends(get_current_active_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_links = await get_user_links(current_user.id)
    if not user_links:
        raise HTTPException(status_code=400, detail="No links found")
    for user_link in user_links:
        if user_link.id == link_id:
            user_link.endpoint_url = new_endpoint
            await user_link.save()
            return Link.from_orm(user_link)
    raise HTTPException(status_code=400, detail="Link not found")






@app.get('/s/{xs_url}')
async def redirect_to_endpoint(xs_url: str, request: Request):
    ip_address = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    link = await get_link_by_short_url(xs_url)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    new_visitor = LinkVisitModel(link=link, ip_address=ip_address,
                                 user_agent=user_agent)

    await new_visitor.save()
    await link.save()
    return {"id": link.id, "endpoint_url": link.endpoint_url}







register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/postgres5",
    modules={"models": ["db.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
