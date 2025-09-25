from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.database import get_async_session
from src.auth.users import current_active_user
from src.links.models import links
from src.links.schemas import *
from src.links.aux_for_handlers import *


router = APIRouter(
    prefix="/links",
    tags=["links"]
)


@router.post("/short")
async def create_short_link(
        new_link: LinkCreateUserInput,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
):
    """
    * FOR GENERATE code by API input strings like 'Null', 'NULL'
    * Short code expiration date sets here (automatically, 14 days)
    """
    try:
        new_link = new_link.dict()
        if new_link['short_code'].lower() == 'null':
            new_link['short_code'] = gen_short_code()
        new_link = fill_fields_initially(new_link)
        new_link['user_id'] = user.id

        statement = insert(links).values(**new_link)
        await session.execute(statement)
        await session.commit()

        return {
            "status": f"Success. Your short core for this link: '{new_link['short_code']}'",
            "data" : new_link['short_code'],
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": "smth went wrong",
        })


@router.get("/{short_code}")
async def get_orig_link(
        short_code: str,
        session: AsyncSession = Depends(get_async_session)
):
    """By short code returns original long link"""
    try:
        query = select(links.c.orig_url).where(links.c.short_code == short_code)
        result = await session.execute(query)
        row = result.scalars().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "data": None,})
    if row is None:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": f"Не найдено {short_code}",
})
    orig_url = row

    # ++stats
    update_stmt = links.update().where(
        links.c.short_code == short_code
    ).values(
        usage_cnt=links.c.usage_cnt + 1
    )
    await session.execute(update_stmt)
    await session.commit()

    return {"status": "success", "data": orig_url}


@router.delete("/{short_code}")
async def delete_link(
        short_code: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)
):
    """Удалить существующую ссылку этого юзера"""
    # Чекаем что такая ссылка есть
    query = select(links).where(links.c.short_code == short_code)
    result = await session.execute(query)
    result = result.scalars().first()
    print(result)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Не найдено"
        )

    # Чекаем что это ссылка пользователя, который удаляет
    query = select(links.c.user_id).where(links.c.short_code == short_code)
    owner_link = await session.execute(query)
    owner_link = owner_link.scalars().first()
    if user.id != owner_link:
        raise HTTPException(
            status_code=403,
            detail="Нет прав на удаление"
        )

    await session.execute(delete(links).where(links.c.short_code == short_code))
    await session.commit()
    return {"message": "Ссылка успешно удалена"}


@router.get("/{short_code}/stats")
async def get_stats(
        short_code: str,
        session: AsyncSession = Depends(get_async_session),
):
    """Get stats on short_code"""
    query = select(
        links.c.orig_url,
        links.c.created_time,
        links.c.usage_cnt,
        links.c.last_usage_time,
    ).where(links.c.short_code == short_code)
    result = await session.execute(query)
    stats = result.first()

    return {
        "status" : "success",
        "data" : {
            "orig_url": stats.orig_url,
            "created_time": stats.created_time,
            "usage_cnt": stats.usage_cnt,
            "last_usage_time":stats.last_usage_time,
        },
    }


@router.get("/search")
async def search_by_orig_link(
        orig_url: str,
        session: AsyncSession = Depends(get_async_session),
):
    """Search short code by long original link"""
    print(type(orig_url))
    query = select(links.c.short_code).where(links.c.orig_url == orig_url)
    result = await session.execute(query)
    result = result.scalars().first()
    return {
        "status" : "success",
        "data" : result
    }


@router.get("/get_all_my_links")
async def get_all_my_links(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
):
    """
    Additional Endpoint
    Get all links of auth user"""
    curr_user_id = user.id

    query = select(
        links.c.short_code,
        links.c.orig_url,
        links.c.expiered_time,
    ).where(links.c.user_id == curr_user_id)
    result = await session.execute(query)
    user_links = result

    return {
        'status':'susses',
        'data': user_links
    }