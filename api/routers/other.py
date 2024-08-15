from fastapi import APIRouter

from api import deps
router = APIRouter(prefix='/example', tags=["example"])


@router.get('/')
def get_protected(user: deps.user_dependency):
    return user