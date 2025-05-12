from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from src.models.campground import Campground
from datetime import datetime

Base = declarative_base()

class CampgroundDB(Base):
    __tablename__ = "campgrounds"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    region_name = Column(String)
    administrative_area = Column(String, nullable=True)
    nearest_city_name = Column(String, nullable=True)

    accommodation_type_names = Column(ARRAY(String))
    bookable = Column(Boolean)
    camper_types = Column(ARRAY(String))

    operator = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    photo_urls = Column(ARRAY(String))

    photos_count = Column(Integer)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer)

    slug = Column(String, nullable=True)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)

    availability_updated_at = Column(DateTime, nullable=True)


def remove_tz(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None) if dt and dt.tzinfo else dt


def campground_to_db(c: Campground) -> CampgroundDB:
    return CampgroundDB(
        id=c.id,
        type=c.type,
        name=c.name,
        latitude=c.latitude,
        longitude=c.longitude,
        region_name=c.region_name,
        administrative_area=c.administrative_area,
        nearest_city_name=c.nearest_city_name,
        accommodation_type_names=c.accommodation_type_names,
        bookable=c.bookable,
        camper_types=c.camper_types,
        operator=c.operator,
        photo_url=str(c.photo_url) if c.photo_url else None,  
        photo_urls=[str(url) for url in c.photo_urls] if c.photo_urls else [],  
        photos_count=c.photos_count,
        rating=c.rating,
        reviews_count=c.reviews_count,
        slug=c.slug,
        price_low=float(c.price_low) if c.price_low else None,
        price_high=float(c.price_high) if c.price_high else None,
        availability_updated_at=remove_tz(c.availability_updated_at)
    )

