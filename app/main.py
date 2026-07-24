from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, optional

app = FastAPI(
    title="AgroVest API",
    description="API for AgroVest project",
    version="1.0.0",
)

def get_current_time() -> datetime:
    return datetime.now(timezone.utc)

#Enum for user roles

class UserRole(str, Enum):
    INVESTOR = "investor"
    FARMER = "farmer"
    ADMIN = "admin"

class UnitType(str, Enum):
    KILOGRAM = "kg"
    TON = "ton"
    BAG = "bag"
    CRAATE = "crate"
    LITER = "liter"
    UNIT = "unit"

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class IvestmentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    ACTIVE = "active"
    DEFAULTED = "defaulted"

class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    MOBILEMONEY = "mobilemoney"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    INTEREST = "interest"

class MarketBase(str, Enum):
    product_name: str = Field(..., min_length=1, max_length=100)
    product_description: str = Field(..., min_length=1, max_length=500)
    product_price: float = Field(..., gt=0)
    product_quantity: float = Field(..., gt=0)
    unit_type: UnitType
    market_id: UUID = Field(default_factory=uuid4, alias="id")
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

class ProductCategory(str, Enum):
    FRUITS = "fruits"
    VEGETABLES = "vegetables"
    GRAINS = "grains"
    DAIRY = "dairy"
    MEAT = "meat"
    POULTRY = "poultry"
    SEAFOOD = "seafood"
    BEVERAGES = "beverages"



# FARMER MODEL
class FarmerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    location: str = Field(..., min_length=1, max_length=100)
    farm_size: float = Field(..., gt=0)
    farm_type: str = Field(..., min_length=1, max_length=100)
    farmer_id: UUID = Field(default_factory=uuid4, alias="id")
    farm_name: str = Field(..., min_length=1, max_length=100)
    primary_crop: str = Field(..., min_length=1, max_length=100)

class FarmerCreate(FarmerBase):
    pass 

class FarmerUpdate(BaseModel):
    name : optional[str] = None
    email : optional[EmailStr] = None
    phone_number : optional[str] = None
    location : optional[str] = None
    farm_size : optional[float] = None
    farm_type : optional[str] = None
    farm_name : optional[str] = None
    primary_crop : optional[str] = None

class Farmer(FarmerBase):
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

# INVESTOR MODEL
class InvestorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    location: str = Field(..., min_length=1, max_length=100)
    investor_id: UUID = Field(default_factory=uuid4, alias="id")
    occupation: str = Field(..., min_length=1, max_length=100)
    investment_amount: float = Field(..., gt=0)

class InvestorCreate(InvestorBase):
    pass

class InvestorUpdate(BaseModel):
    name : optional[str] = None
    email : optional[EmailStr] = None
    phone_number : optional[str] = None
    location : optional[str] = None
    occupation : optional[str] = None
    investment_amount : optional[float] = None

class Investor(InvestorBase):
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

class InvestmentBase(BaseModel):
    investment_id: UUID = Field(default_factory=uuid4, alias="id")
    investor_id: UUID
    farmer_id: UUID
    amount: float = Field(..., gt=0)
    status: IvestmentStatus = Field(default=IvestmentStatus.PENDING)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
    note: str = Field(..., min_length=1, max_length=500)

class InvestmentCreate(BaseModel):
    investor_id: UUID
    farmer_id: UUID
    amount: float = Field(..., gt=0)
    expected_return: float = Field(..., gt=0)
    note: str = Field(..., min_length=1, max_length=500)

class InvestmentUpdate(BaseModel):
    status: optional[IvestmentStatus] = None

# Market And Order  Model
class MarketBaseModel(BaseModel):
    market_id: UUID = Field(default_factory=uuid4, alias="id")
    product_name: str = Field(..., min_length=1, max_length=100)
    product_description: str = Field(..., min_length=1, max_length=500)
    product_price: float = Field(..., gt=0)
    product_quantity: float = Field(..., gt=0)
    unit_type: UnitType
    category: ProductCategory
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

class MarketCreate(MarketBaseModel):
    pass

class MarketUpdate(BaseModel):
    product_name: optional[str] = None
    product_description: optional[str] = None
    product_price: optional[float] = None
    product_quantity: optional[float] = None
    unit_type: optional[UnitType] = None
    category: optional[ProductCategory] = None

class Market(MarketBaseModel):
    pass

class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100)
    product_description: str = Field(..., min_length=1, max_length=500)
    product_price: float = Field(..., gt=0)
    product_quantity: float = Field(..., gt=0)
    unit_type: UnitType
    category: ProductCategory
    farmer_id: UUID

class ProductUpdate(BaseModel):
    product_name: optional[str] = None
    product_description: optional[str] = None
    product_price: optional[float] = None
    product_quantity: optional[float] = None
    unit_type: optional[UnitType] = None
    category: optional[ProductCategory] = None

class Product(BaseModel):
    product_id: UUID = Field(default_factory=uuid4, alias="id")
    product_name: str = Field(..., min_length=1, max_length=100)
    product_description: str = Field(..., min_length=1, max_length=500)
    product_price: float = Field(..., gt=0)
    product_quantity: float = Field(..., gt=0)
    unit_type: UnitType
    category: ProductCategory
    farmer_id: UUID
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

class OrderBase(BaseModel):
    order_id: UUID = Field(default_factory=uuid4, alias="id")
    product_id: UUID
    investor_id: UUID
    quantity: float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    @field_validator("total_price")
    @field_validator("quantity")
    @classmethod
    def validate_total_price(cls, v, values):
        if "product_id" in values and "quantity" in values:
            product = get_product_by_id(values["product_id"])
            if product:
                expected_total_price = product.product_price * values["quantity"]
                if v != expected_total_price:
                    raise ValueError(f"Total price should be {expected_total_price} for the given quantity.")
        return v
    
class OrderCreate(BaseModel):
    product_id: UUID
    investor_id: UUID
    quantity: float = Field(..., gt=0)
    buyer_id = UUID
    quantity: float = Field(..., gt=0)
    unit_price = float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default_factory=get_current_time)

class OrderUpdate(BaseModel):
    status: optional[OrderStatus] = None

# In-memory storage for demonstration purposes
farmer_db: dict[UUID, Farmer] = {}
investor_db: dict[UUID, Investor] = {}
product_db: dict[UUID, Product] = {}
order_db: dict[UUID, OrderBase] = {}
investment_db: dict[UUID, InvestmentBase] = {}

#Helper functions 
def get_or_404(store: dict[UUID, BaseModel], key: UUID, label: str) -> BaseModel:
    item = store.get(key)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{label} not found.")
    return item

def ower_exists(owner_id: UUID) -> bool:
    return owner_id in farmer_db or owner_id in investor_db

#Root / Health
@app.get("/", tags=["roots"])
def root():
    return{
        "message" : "Welcome TO AgroVest API",
        "docs" : "/docs",
        "modules" : ["farmers", "investors", "products", "orders", "investments", "market"]
    }

@app.get("/health", tags=["roots"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": get_current_time().isoformat().utcnow()
    }

#Farmer Endpoints
@app.post("/farmers", response_model=Farmer, status_code=status.HTTP_201_CREATED, tags=["farmers"])
def create_farmer(farmer: FarmerCreate):
    new_farmer = Farmer(**farmer.dict())
    farmer_db[new_farmer.farmer_id] = new_farmer
    return new_farmer
@app.get("/farmers", response_model=List[Farmer], tags=["farmers"])
def get_farmers(location: optional[str] = Query(None, description="Filter farmers by location" )):
    result = list(farmer_db.values())
    if location:
        result = [farmer for farmer in result if farmer.location.lower() == location.lower()]
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No farmers found.")
    if verified_only:
        result = [farmer for farmer in result if farmer.verified]
    return result
