import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models.file import File
from app.models.result import Result
from app.config import settings
from app.services.extract import extract_text

router = APIRouter()


@router.post("/files")
async def upload_file(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    # Fayl turi tekshirish
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     "image/png", "image/jpeg"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Fayl turi qo'llab-quvvatlanmaydi")
    
    # Fayl hajmi tekshirish
    content = await file.read()
    size = len(content)
    max_size = settings.MAX_UPLOAD_MB * 1024 * 1024  # MB to bytes
    
    if size > max_size:
        raise HTTPException(status_code=413, detail=f"Fayl hajmi {settings.MAX_UPLOAD_MB}MB dan oshmasligi kerak")
    
    # UUID nom bilan saqlash
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    stored_path = settings.UPLOAD_DIR / unique_filename
    
    # Papka yaratish
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Faylni saqlash
    with open(stored_path, "wb") as f:
        f.write(content)
    
    # Database ga yozish
    db_file = File(
        filename=file.filename,
        stored_path=str(stored_path),
        content_type=file.content_type,
        size=size
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {
        "id": db_file.id,
        "filename": db_file.filename,
        "size": db_file.size,
        "content_type": db_file.content_type,
        "created_at": db_file.created_at
    }


@router.post("/files/{file_id}/extract")
async def extract_file_text(
    file_id: int,
    db: Session = Depends(get_db)
):
    # Faylni bazadan topish
    db_file = db.query(File).filter(File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    
    # Fayl yo'li tekshirish
    file_path = Path(db_file.stored_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fayl diskda topilmadi")
    
    # Matn ajratish
    try:
        text = extract_text(str(file_path), db_file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Result yaratish/yangilash
    existing_result = db.query(Result).filter(Result.file_id == file_id).first()
    if existing_result:
        existing_result.text = text
        db.commit()
        db.refresh(existing_result)
        result = existing_result
    else:
        result = Result(file_id=file_id, text=text)
        db.add(result)
        db.commit()
        db.refresh(result)
    
    return {
        "id": result.id,
        "file_id": result.file_id,
        "text": result.text,
        "created_at": result.created_at
    }


@router.get("/files")
async def get_files(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Fayllar ro'yxati (pagination bilan)
    """
    offset = (page - 1) * size
    files = db.query(File).order_by(File.created_at.desc()).offset(offset).limit(size).all()
    total = db.query(File).count()
    
    return {
        "files": [
            {
                "id": f.id,
                "filename": f.filename,
                "size": f.size,
                "content_type": f.content_type,
                "created_at": f.created_at
            }
            for f in files
        ],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }


@router.get("/files/{file_id}")
async def get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Bitta fayl ma'lumotlari (natija bilan)
    """
    db_file = db.query(File).filter(File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    
    # Result ni olish
    result = db.query(Result).filter(Result.file_id == file_id).first()
    
    return {
        "id": db_file.id,
        "filename": db_file.filename,
        "size": db_file.size,
        "content_type": db_file.content_type,
        "created_at": db_file.created_at,
        "result": {
            "id": result.id,
            "text": result.text,
            "summary": result.summary,
            "data": result.data,
            "created_at": result.created_at
        } if result else None
    }


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Faylni diskdan va bazadan o'chirish
    """
    db_file = db.query(File).filter(File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    
    # Diskdan o'chirish
    file_path = Path(db_file.stored_path)
    if file_path.exists():
        file_path.unlink()
    
    # Bazadan o'chirish (Result CASCADE bilan o'chadi)
    db.delete(db_file)
    db.commit()
    
    return {"message": "Fayl muvaffaqiyatli o'chirildi"}
