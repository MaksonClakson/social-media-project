from enum import Enum

CONTAINER_MESSAGES_IP = 'statistic_service_innotter:8000'


class CommandTypes(str, Enum):
    CREATE_PAGE = "create_page"
    UPDATE_PAGE = "update_page"
    DELETE_PAGE = "delete_page"
    GET_ALL_STAT = "get_stat"
    NEW_PAGE_LIKE = "new_like"
    NEW_PAGE_FOLLOWER = "new_follower"
    NEW_PAGE_FOLLOW_REQUEST = "new_follow_request"
    UNDO_PAGE_LIKE = "undo_like"
    UNDO_PAGE_FOLLOWER = "undo_follower"
    UNDO_FOLLOW_REQUEST = "undo_follow_request"
