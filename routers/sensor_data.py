from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import datetime

from database import get_db, SensorReading

router = APIRouter()

@router.get("/")
def get_sensor_readings(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    topic: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
):
    query = db.query(SensorReading)
    
    if topic != None:
        query = query.filter(SensorReading.topic == topic)
    
    if start_time != None:
        query = query.filter(SensorReading.received_at >= start_time)
        
    if end_time != None:
        query = query.filter(SensorReading.received_at <= end_time)
    
    count_data = query.count()
    
    # Calculating the skip number
    skip_num = (page - 1) * page_size
    
    data_from_db = query.order_by(desc(SensorReading.received_at)).offset(skip_num).limit(page_size).all()
    
    # Putting everything in a list one by one
    readings_list = []
    for r in data_from_db:
        # Create a dictionary for the row
        row_dict = {}
        row_dict["id"] = r.id
        row_dict["topic"] = r.topic
        row_dict["temperature"] = r.temperature
        row_dict["humidity"] = r.humidity
        row_dict["voltage"] = r.voltage
        row_dict["current"] = r.current
        row_dict["pressure"] = r.pressure
        
        if r.received_at != None:
            row_dict["received_at"] = r.received_at.isoformat()
        else:
            row_dict["received_at"] = None
            
        readings_list.append(row_dict)
    
    # Math for pages
    total_p = (count_data + page_size - 1) // page_size
    
    return {
        "data": readings_list,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": count_data,
            "total_pages": total_p
        }
    }

@router.get("/latest")
def get_latest_readings(db: Session = Depends(get_db)):
    # First get the topics
    all_topics_data = db.query(SensorReading.topic).distinct().all()
    
    latest_results = []
    for t_tuple in all_topics_data:
        current_topic = t_tuple[0]
        
        # Now find the latest one for this specific topic
        res = db.query(SensorReading).filter(SensorReading.topic == current_topic).order_by(desc(SensorReading.received_at)).first()
        
        if res != None:
            # Build the item manually
            item = {}
            item["id"] = res.id
            item["topic"] = res.topic
            item["temperature"] = res.temperature
            item["humidity"] = res.humidity
            item["voltage"] = res.voltage
            item["current"] = res.current
            item["pressure"] = res.pressure
            
            if res.received_at != None:
                item["received_at"] = res.received_at.isoformat()
            else:
                item["received_at"] = None
                
            latest_results.append(item)
    
    return {"data": latest_results}

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    # Getting counts separately
    total1 = db.query(SensorReading).count()
    total2 = db.query(SensorReading.topic).distinct().count()
    
    return {
        "total_readings": total1,
        "total_topics": total2,
    }

@router.get("/topics")
def get_all_topics(db: Session = Depends(get_db)):
    topic_rows = db.query(SensorReading.topic).distinct().all()
    
    # No list comprehension, just a basic loop
    final_topic_list = []
    for row in topic_rows:
        name = row[0]
        final_topic_list.append(name)
        
    return {"topics": final_topic_list}