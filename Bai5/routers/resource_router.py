from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies.authentication import get_current_user
from dependencies.authorization import require_admin
from models.models import User
from schemas.schemas import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from services.resource_service import (
    create_resource,
    delete_resource,
    get_all_resources,
    get_my_resources,
    get_resource_by_id,
    update_resource,
)


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


# ==========================================
# GET ALL RESOURCES
# ==========================================

@router.get(
    "",
    response_model=list[ResourceResponse]
)
def read_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_resources(db)


# ==========================================
# GET MY RESOURCES
# ==========================================

@router.get(
    "/me",
    response_model=list[ResourceResponse]
)
def read_my_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_resources(
        db,
        current_user
    )


# ==========================================
# GET RESOURCE BY ID
# ==========================================

@router.get(
    "/{resource_id}",
    response_model=ResourceResponse
)
def read_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_resource_by_id(
        db,
        resource_id
    )


# ==========================================
# CREATE RESOURCE - ADMIN ONLY
# ==========================================

@router.post(
    "",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return create_resource(
        db,
        resource_data,
        current_user
    )


# ==========================================
# UPDATE RESOURCE - OWNER ONLY
# ==========================================

@router.patch(
    "/{resource_id}",
    response_model=ResourceResponse
)
def update_existing_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_resource(
        db,
        resource_id,
        resource_data,
        current_user
    )


# ==========================================
# DELETE RESOURCE - OWNER ONLY
# ==========================================

@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_resource(
        db,
        resource_id,
        current_user
    )

    return None