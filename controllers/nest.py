from models.models import Nest, User
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from controllers.auth import get_current_user
import secrets
import string


class NestCreateRequest(BaseModel):
    name: str


class NestResponse(BaseModel):
    join_code: str
    name: str
    members: list[str]


class GetNestsResponse(BaseModel):
    nests: list[NestResponse]


async def generate_unique_join_code(length: int = 6) -> str:
    while True:
        # Generate random alphanumeric code
        code = "".join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for _ in range(length)
        )

        # Check if it already exists
        exists = await Nest.filter(join_code=code).exists()
        if not exists:
            return code


async def createNest(request_data: NestCreateRequest, user=Depends(get_current_user)):
    try:
        db_user = await User.get(id=user.id)

        nest = await Nest.create(
            name=request_data.name,
            join_code=await generate_unique_join_code(),
            created_by=db_user,
        )

        await nest.users.add(db_user)

        return NestResponse(
            join_code=nest.join_code, name=nest.name, members=[db_user.display_name]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def getNestsByUser(user=Depends(get_current_user)):
    try:
        db_user = await User.get(id=user.id)

        nests = await db_user.joined_nests.all().prefetch_related("users")

        response = GetNestsResponse(
            nests=[
                NestResponse(
                    join_code=n.join_code,
                    name=n.name,
                    members=[m.display_name for m in n.users],
                )
                for n in nests
            ]
        )
        
        print(response.model_dump_json(indent=2))
        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
