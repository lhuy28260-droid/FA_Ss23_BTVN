import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger("secure_learning_portal")


# ==========================================
# REQUEST MIDDLEWARE
# ==========================================

class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        # --------------------------------------
        # 1. Sinh Request ID
        # --------------------------------------

        request_id = str(uuid.uuid4())

        # Lưu Request ID vào request
        request.state.request_id = request_id

        # --------------------------------------
        # 2. Ghi nhận thời gian bắt đầu
        # --------------------------------------

        start_time = time.perf_counter()

        # --------------------------------------
        # 3. Cho Request đi tiếp
        # --------------------------------------

        response = await call_next(request)

        # --------------------------------------
        # 4. Tính thời gian xử lý
        # --------------------------------------

        process_time = (
            time.perf_counter() - start_time
        )

        # --------------------------------------
        # 5. Gắn Request ID vào Response
        # --------------------------------------

        response.headers["X-Request-ID"] = request_id

        # --------------------------------------
        # 6. Log thông tin Request
        # --------------------------------------

        logger.info(
            "%s %s - %s - %.4fs - request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
            request_id
        )

        return response