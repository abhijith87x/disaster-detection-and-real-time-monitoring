from fastapi import FastAPI
from predict import router as predict_router
import time
from fastapi import Request
from fastapi.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

app = FastAPI()

# @app.middleware("http")
# async def timing_middleware(request: Request, call_next):
#     start = time.perf_counter()

#     print("MIDDLEWARE START")

#     response = await call_next(request)
#     t_after_call_next = time.perf_counter()
#     print(
#         f"CALL_NEXT RETURNED: "
#         f"{t_after_call_next - start:.4f}s"
#     )

#     print("MIDDLEWARE END")

#     return response



app.include_router(predict_router)