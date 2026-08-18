import re

from fastapi import Request
from fastapi.responses import JSONResponse

from security import decode_access_token


PROTECTED_ROUTES = {
    ("GET", "/exams"): ["user", "admin"],
    ("GET", "/users/me/results"): ["user", "admin"],
    ("POST", "/admin/exams"): ["admin"],
    ("PATCH", "/admin/exams/{exam_id}/lock"): ["admin"],
    ("GET", "/admin/results"): ["admin"],
}


PUBLIC_ROUTES = {
    ("GET", "/health")
}


def path_matches(request_path: str, route_path: str):
    if "{" not in route_path:
        return request_path == route_path

    pattern = re.sub(
        r"\{[^/]+\}",
        r"[^/]+",
        route_path
    )

    pattern = "^" + pattern + "$"

    return re.match(pattern, request_path) is not None


def find_permission(method: str, path: str):
    for (allowed_method, route_path), allowed_roles in PROTECTED_ROUTES.items():

        if method != allowed_method:
            continue

        if path_matches(path, route_path):
            return allowed_roles

    return None


async def authorization_middleware(request: Request, call_next):

    # Bẫy 2:
    # OPTIONS phải được CORS xử lý,
    # không yêu cầu JWT.
    if request.method == "OPTIONS":
        return await call_next(request)

    method = request.method
    path = request.url.path

    # API public
    if (method, path) in PUBLIC_ROUTES:
        return await call_next(request)

    # Kiểm tra API có cần Authorization không
    allowed_roles = find_permission(method, path)

    # Không nằm trong Permission Matrix
    if allowed_roles is None:
        return await call_next(request)

    # Lấy Authorization Header
    authorization = request.headers.get("Authorization")

    if not authorization:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Missing token"
            }
        )

    if not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid authorization header"
            }
        )

    token = authorization.replace("Bearer ", "", 1)

    # Authentication
    try:
        current_user = decode_access_token(token)
    except Exception as e:

        status_code = getattr(e, "status_code", 401)

        detail = getattr(
            e,
            "detail",
            "Invalid token"
        )

        return JSONResponse(
            status_code=status_code,
            content={
                "error": detail
            }
        )

    # Authorization - Role Check
    user_role = current_user["role"]

    if user_role not in allowed_roles:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Permission Denied"
            }
        )

    request.state.user = current_user

    return await call_next(request)