from fastapi import APIRouter, Body, HTTPException, status, Depends
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(tags=["Events"])

events = []

""" Retrieve Endpoints """
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session = Depends(get_session)):
    statement = select(Event)
    events = session.exec(statement).all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session = Depends(get_session)):
    event = session.get(Event, id)
    if event:
            return event 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} does not exist  ")

""" Posting Endpoints """
@event_router.post("/new")
async def create_event(new_event: Event, session = Depends(get_session) ):
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Event created successfully"}


""" Delete Endpoints """

# Delete single data
@event_router.delete("/{id}")
async def delete_event(id:int, session = Depends(get_session)):
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        
        return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with supplied ID {id} doesn't exist")

# Delete all data
@event_router.delete("/")
async def delete_all_events():
    events.clear()
    return {"message": "Events deleted successfully"}


""" Update Endpoints """
@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session = Depends(get_session)):
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with supplied ID {id} doesn't exist")
    
        