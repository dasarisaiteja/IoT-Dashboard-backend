from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import json

from database import get_db, Alert

router = APIRouter()

@router.get("/")
def get_alerts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: str = Query(None),   
    topic: str = Query(None),      
):
    query = db.query(Alert)
    
    if severity != None:
        severity_upper = severity.upper()
        query = query.filter(Alert.severity == severity_upper)
        
    if topic != None:
        query = query.filter(Alert.topic == topic)
    
    count_all = query.count()
    
    # Manual pagination math
    number_to_skip = (page - 1) * page_size
    alerts_data = query.order_by(desc(Alert.created_at)).offset(number_to_skip).limit(page_size).all()
    
    results = []
    for item in alerts_data:
        # Handling JSON strings manually for each one
        try:
            val_actual = json.loads(item.actual_values)
        except:
            val_actual = {}
        
        try:
            val_threshold = json.loads(item.threshold_values)
        except:
            val_threshold = {}
        
        # Building the dictionary key by key
        d = {}
        d["id"] = item.id
        d["topic"] = item.topic
        d["violated_keys"] = item.violated_keys.split(", ")
        d["actual_values"] = val_actual
        d["threshold_values"] = val_threshold
        d["severity"] = item.severity
        
        if item.created_at != None:
            d["created_at"] = item.created_at.isoformat()
        else:
            d["created_at"] = None
            
        results.append(d)
    
    total_pages_count = (count_all + page_size - 1) // page_size
    
    return {
        "data": results,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": count_all,
            "total_pages": total_pages_count
        }
    }

@router.get("/recent")
def get_recent_alerts(
    db: Session = Depends(get_db),
    limit: int = Query(5, ge=1, le=20)
):
    recent_db_data = db.query(Alert).order_by(desc(Alert.created_at)).limit(limit).all()
    
    list_to_return = []
    for a in recent_db_data:
        try:
            parsed_json = json.loads(a.actual_values)
        except:
            parsed_json = {}
        
        # New coders often re-type the whole dictionary structure
        new_item = {
            "id": a.id,
            "topic": a.topic,
            "violated_keys": a.violated_keys.split(", "),
            "actual_values": parsed_json,
            "severity": a.severity,
            "created_at": a.created_at.isoformat() if a.created_at != None else None
        }
        list_to_return.append(new_item)
    
    return {"data": list_to_return}

@router.get("/stats")
def get_alert_stats(db: Session = Depends(get_db)):
    # Running separate queries instead of an aggregate/group_by
    v1 = db.query(Alert).count()
    v2 = db.query(Alert).filter(Alert.severity == "CRITICAL").count()
    v3 = db.query(Alert).filter(Alert.severity == "WARNING").count()
    
    return {
        "total_alerts": v1,
        "critical_alerts": v2,
        "warning_alerts": v3
    }