from fastapi import APIRouter, HTTPException
from app.models.subscription import SubscriptionCreate, SubscriptionVerify
from app.utils.database import Database
from typing import Dict, Any

router = APIRouter(prefix="/api/subscription", tags=["subscription"])
db = Database()


@router.post("/create")
async def create_subscription(subscription: SubscriptionCreate) -> Dict[str, Any]:
    try:
        result = db.create_subscription(
            email=subscription.email,
            duration_days=subscription.duration_days
        )
        return {
            "success": True,
            "message": "تم إنشاء الاشتراك بنجاح / Subscription created successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify")
async def verify_subscription(verify: SubscriptionVerify) -> Dict[str, Any]:
    try:
        result = db.verify_subscription(
            code=verify.code,
            device_id=verify.device_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/renew/{code}")
async def renew_subscription(code: str, additional_days: int = 30) -> Dict[str, Any]:
    try:
        result = db.renew_subscription(code, additional_days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_subscriptions() -> Dict[str, Any]:
    try:
        subscriptions = db.get_all_subscriptions()
        return {
            "success": True,
            "count": len(subscriptions),
            "subscriptions": subscriptions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
