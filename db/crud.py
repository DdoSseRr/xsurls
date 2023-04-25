from .models import User as UserModel, Link as LinkModel
from fast.schemas.user import User


async def get_user_by_dict(user_info: dict):
    user = await UserModel.get_or_none(**user_info)
    return user


async def get_user_by_email(email: str):
    user = await UserModel.get_or_none(email=email)
    if user:
        return user



async def get_user_by_username(username: str):
    user = await UserModel.get_or_none(username=username)
    return user



async def get_user_full(username: str):
    user = await UserModel.filter(username=username).first()
    await user.fetch_related("links")
    user_links = list(user.links)
    user.user_links = user_links
    if user:
        if not user.user_links:
            user.user_links = []
        return User.from_orm(user)


async def create_user(user: UserModel):
    await user.save()
    return User.from_orm(user)


async def get_user_links(user_id: int):
    links = await LinkModel.filter(owner_id=user_id).all()
    if links:
        return links


async def get_link_by_short_url(xs_url: str):
    link = await LinkModel.filter(xs_url=xs_url).first()
    if link:
        await link.fetch_related("visits")
        link_visits = list(link.visits)
        link.link_visits = link_visits
        return link
