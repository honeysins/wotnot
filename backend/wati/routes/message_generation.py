from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import database
from ..Schemas.message_generation import MessageGenerationRequest, MessageGenerationResponse
from ..services.message_generation import message_generation_service
from ..oauth2 import get_current_user
from ..Schemas import user

router = APIRouter(tags=['Message Generation'])

@router.post("/generate-message", response_model=MessageGenerationResponse)
async def generate_message(
    request: MessageGenerationRequest,
    db: AsyncSession = Depends(database.get_db),
    current_user: user.newuser = Depends(get_current_user)
):
    """
    Generate a message based on user's prompt using Gemini API
    
    Args:
        request: Contains prompt
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        MessageGenerationResponse: Generated message or error
    """
    try:
        # Generate the message using the service
        result = await message_generation_service.generate_message(
            prompt=request.prompt
        )
        
        return MessageGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
