from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import AIHistory
from schemas import PromptRequest
from services.ai_service import generate_ai_reply
from routers.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/ask", response_model=AIHistory)
def ask_ai(
    data: PromptRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    try:
        reply = generate_ai_reply(data.prompt)
        record = AIHistory(username=current_user, prompt=data.prompt, response=reply)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list[AIHistory])
def get_history(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    return session.exec(select(AIHistory).where(AIHistory.username == current_user)).all()

@router.delete("/history/{record_id}")
def delete_history(
    record_id:int, 
    session: Session = Depends(get_session), 
    current_user: str = Depends(get_current_user)
):

    record = session.get(AIHistory, record_id)
    if not record or record.username != current_user:
        raise HTTPException(status_code=404, detail="Record not found")
    session.delete(record)
    session.commit()
    return {"message": "Record deleted"}
@router.put("/history/{record_id}", response_model=AIHistory)
def update_history(
    record_id: int,
    data: PromptRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    record = session.get(AIHistory, record_id)
    if not record or record.username != current_user:
        raise HTTPException(status_code=404, detail="Record not found")
    
    # Update the prompt and generate a new response
    record.prompt = data.prompt
    try:
        record.response = generate_ai_reply(data.prompt)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))