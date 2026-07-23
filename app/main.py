from fastapi import FastAPI

from app.database.connection import database

from app.routes.product_routes import router as product_router
from app.routes.category_routes import router as category_router
from app.routes.customer_routes import router as customer_router
from app.routes.cart_routes import router as cart_router
from app.routes.order_routes import router as order_router
from app.routes.payment_routes import router as payment_router
from app.routes.auth_routes import router as auth_router
from app.routes.aggregation_routes import router as aggregation_router
from app.routes.lookup_routes import router as lookup_router
from app.routes.advanced_lookup_routes import router as advanced_lookup_router
from app.routes.report_routes import router as report_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.order_management_routes import router as order_management_router
from app.routes.statistics_routes import router as statistics_router
from app.routes.search_routes import router as search_router
from app.routes.pagination_routes import router as pagination_router

app = FastAPI(
    title="Boutique E-Commerce Backend",
    description="Backend API for Boutique E-Commerce Store",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(customer_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(aggregation_router)
app.include_router(lookup_router)
app.include_router(advanced_lookup_router)
app.include_router(report_router)
app.include_router(dashboard_router)
app.include_router(order_management_router)
app.include_router(statistics_router)
app.include_router(search_router)
app.include_router(pagination_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Boutique Backend"
    }


@app.get("/database")
def check_database():

    collections = database.list_collection_names()

    return {
        "collections": collections
    }