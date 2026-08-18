from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.models import Resource, User
from schemas.schemas import ResourceCreate, ResourceUpdate


# ==========================================
# GET ALL RESOURCES
# ==========================================

def get_all_resources(
    db: Session
) -> list[Resource]:

    return (
        db.query(Resource)
        .all()
    )


# ==========================================
# GET RESOURCE BY ID
# ==========================================

def get_resource_by_id(
    db: Session,
    resource_id: int
) -> Resource:

    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    return resource


# ==========================================
# GET MY RESOURCES
# ==========================================

def get_my_resources(
    db: Session,
    current_user: User
) -> list[Resource]:

    return (
        db.query(Resource)
        .filter(
            Resource.owner_id == current_user.id
        )
        .all()
    )


# ==========================================
# CREATE RESOURCE
# ==========================================

def create_resource(
    db: Session,
    resource_data: ResourceCreate,
    current_user: User
) -> Resource:

    resource = Resource(
        title=resource_data.title,
        description=resource_data.description,
        owner_id=current_user.id
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


# ==========================================
# UPDATE RESOURCE
# ==========================================

def update_resource(
    db: Session,
    resource_id: int,
    resource_data: ResourceUpdate,
    current_user: User
) -> Resource:

    # 1. Tìm Resource
    resource = get_resource_by_id(
        db,
        resource_id
    )

    # 2. Kiểm tra Ownership
    if resource.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource"
        )

    # 3. Lấy dữ liệu cần update
    update_data = resource_data.model_dump(
        exclude_unset=True
    )

    # 4. Cập nhật từng field
    for field, value in update_data.items():
        setattr(
            resource,
            field,
            value
        )

    # 5. Lưu Database
    db.commit()
    db.refresh(resource)

    return resource


# ==========================================
# DELETE RESOURCE
# ==========================================

def delete_resource(
    db: Session,
    resource_id: int,
    current_user: User
) -> None:

    # 1. Tìm Resource
    resource = get_resource_by_id(
        db,
        resource_id
    )

    # 2. Kiểm tra Ownership
    if resource.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource"
        )

    # 3. Xóa
    db.delete(resource)
    db.commit()