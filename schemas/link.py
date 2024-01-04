from typing import Optional
from pydantic import BaseModel





class LinkBase(BaseModel):
    endpoint_url: str



class LinkCreate(LinkBase):
    endpoint_url: str


class Link(LinkBase):
    id: int
    endpoint_url: str
    xs_url: str
    owner_id: int
    link_visits: Optional[list] = []

    class Config:
        orm_mode = True


class LinkVisitBase(BaseModel):
    pass


class LinkVisitCreate(LinkVisitBase):
    link_id: int
    ip_address: str
    user_agent: str


class LinkVisit(LinkVisitBase):
    id: int
    visited_at: str

    class Config:
        orm_mode = True
