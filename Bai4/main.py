from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from middleware import authorization_middleware
from security import Role, create_access_token


app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://online-exam.example.com"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PATCH"
    ],
    allow_headers=[
        "Authorization",
        "Content-Type"
    ]
)




app.middleware("http")(authorization_middleware)



USERS = {
    "student01": {
        "user_id": "student01",
        "role": Role.USER
    },
    "student02": {
        "user_id": "student02",
        "role": Role.USER
    },
    "admin01": {
        "user_id": "admin01",
        "role": Role.ADMIN
    }
}



RESULTS = {
    "student01": [
        {
            "exam_id": 1,
            "score": 8.5
        }
    ],
    "student02": [
        {
            "exam_id": 1,
            "score": 7.5
        }
    ]
}




@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/exams")
def get_exams():
    return {
        "message": "Exam list"
    }


@app.post("/admin/exams")
def create_exam():
    return {
        "message": "Exam created"
    }


@app.patch("/admin/exams/{exam_id}/lock")
def lock_exam(exam_id: int):
    return {
        "message": f"Exam {exam_id} locked"
    }

@app.get("/users/me/results")
def get_my_results(request: Request):

    current_user = request.state.user

    user_id = current_user["user_id"]

    return {
        "user_id": user_id,
        "results": RESULTS.get(user_id, [])
    }


@app.get("/admin/results")
def get_all_results():

    return {
        "results": RESULTS
    }


@app.post("/demo-login/{user_id}")
def demo_login(user_id: str):

    user = USERS.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }

    token = create_access_token(
        user_id=user["user_id"],
        role=user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }