from enum import Enum
from fastapi import Body, FastAPI, HTTPException, Request, status, Form
from pydantic import BaseModel
import settings
from fastapi.responses import JSONResponse

import services
from schemas.pages import Page


app = FastAPI()

class POST_PARAMETERS(str, Enum):
    PAGE_ID = "page_id"
    USER_ID = "user_id"
    NAME = "page_name"

@app.get('/get_statistic/', response_model=Page)
def get_statistic(page_id: int = Body(), user_id: int = Body()):
    """
    Returns statistic of the page
    Request body:
        :page_id - id of the page
        :user_id - id of the current authenticated user
    """
    content, _status = services.get_statistic(page_id, user_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/create_page/', response_model=Page)
def create_page(page_id: int = Body(), user_id: int = Body(), page_name: str = Body()):
    """
    Perfroms creating page at the 'Pages' table
    Request body:
        :page_id - id of the page
        :user_id - id of user (owner) of the page
    """
    content, _status = services.create_page(page_id, user_id, page_name)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/update_page/', response_model=Page)
def update_page(page_id: int = Body(), user_id: int = Body(), page_name: str = Body()):
    """
    Perfroms updating page name of the page at the 'Pages' table
    :page_id - id of the page
    :user_id - id of the current authenticated user
    :page_name - new name of the page
    """
    content, _status = services.update_page(page_id, user_id, page_name)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.delete('/delete_page/')
def delete_page(page_id: int = Body(), user_id: int = Body()):
    """
    Perfroms removing page from the 'Pages' table
    Request body:
        :page_id - id of the page
        :user_id - id of the current authenticated user
    """
    content, _status = services.delete_page(page_id, user_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/new_like/', response_model=Page)
def new_like(page_id: int = Body(embed=True)):
    """
    Perfroms adding like to page statistic
    Request body:
        :page_id - id of the page
    """
    content, _status = services.new_like(page_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/undo_like/', response_model=Page)
def undo_like(page_id: int = Body(embed=True)):
    """
    Perfroms removing like from page statistic
    Request body:
        :page_id - id of the page
    """
    content, _status = services.undo_like(page_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/new_follow_request/', response_model=Page)
def new_follow_request(page_id: int = Body(embed=True)):
    """
    Perfroms adding new follow request to page statistic
    Request body:
        :page_id - id of the page
    """
    content, _status = services.new_follow_request(page_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/undo_follow_request/', response_model=Page)
def undo_follow_request(page_id: int = Body(embed=True)):
    """
    Perfroms removing follow request from page statistic
    Request body:
        :page_id - id of the page
    """
    content, _status = services.undo_follow_request(page_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/new_follower/', response_model=Page)
def new_follower(page_id: int = Body(embed=True)):
    """
    Perfroms adding new follower to page statistic
    Request body:
        :page_id - id of the page
    """
    content, _status = services.new_follower(page_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content


@app.post('/undo_follower/', response_model=Page)
def undo_follower(page_id: int = Body(embed=True)):
    """
    Perfroms removing follower from page statistic
    """
    content, _status = services.undo_follower(page_id)
    if _status != status.HTTP_200_OK:
        raise HTTPException(status_code=_status, detail=content)
    return content
