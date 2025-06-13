# from fastapi import FastAPI
# from fastapi.openapi.utils import get_openapi
# from routes.auth import auth_router
# from routes import actorRoute, directorRoute, priceRoute, seatRoute, ticketRoute, playRoute, customerRoute, showtimeRoute
# from fastapi.middleware.cors import CORSMiddleware
#
#
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[""],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# app.include_router(auth_router)
# app.include_router(actorRoute.actor_router)
# app.include_router(directorRoute.director_router)
# app.include_router(playRoute.play_router)
# app.include_router(customerRoute.customer_router)
# app.include_router(showtimeRoute.showtime_router)
# app.include_router(seatRoute.seat_router)
# app.include_router(ticketRoute.ticket_router)
# app.include_router(priceRoute.price_router)
#
# @app.get("/")
# def root():
#     return {"message":"🎭welcome to Sierra Leone Theatre"}
#
#
# # Custom OpenAPI to add OAuth2 scheme in docs for padlock
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Sierra Leone Music Api",
#         version="1.0.0",
#         description="API with OAuth2 authentication",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "OAuth2PasswordBearer": {
#             "type": "oauth2",
#             "flows": {
#                 "password": {
#                     "tokenUrl": "/auth/login",
#                     "scopes": {}
#                 }
#             },
#         }
#     }
#     # Apply globally so padlock shows for all endpoints that require it
#     openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
#
# app.openapi = custom_openapi
#
#
#
#
#
