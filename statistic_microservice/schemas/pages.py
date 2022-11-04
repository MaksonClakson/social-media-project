from pydantic import BaseModel


class Page(BaseModel):
    page_id: int
    user_id: int
    name: str
    likes: int
    followers: int
    follower_requests: int
