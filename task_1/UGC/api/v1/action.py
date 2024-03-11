from uuid import UUID
from fastapi import APIRouter, Depends
from services.producer import get_producer_service, ProducerService
from core.handlers import JwtHandler, require_access_token

router = APIRouter()


@router.post('/')
async def create_action(
    action: str,
    film_id: UUID,
    service: ProducerService = Depends(get_producer_service),
    jwt_handler: JwtHandler = Depends(require_access_token),
):
    user = await jwt_handler.get_current_user()
    return service.produce(action=action, film_id=film_id, user=user)
