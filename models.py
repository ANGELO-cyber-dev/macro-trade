from datetime import datetime
import enum
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
from database import Base

class QualityStatus(enum.Enum):
    GOOD = "GOOD"
    STALE = "STALE"
    MISSING = "MISSING"
    INVALID = "INVALID"
    DELAYED = "DELAYED"
    REVISED = "REVISED"

class AssetClass(enum.Enum):
    FX = "FX"
    COMMODITIES = "COMMODITIES"
    CRYPTO = "CRYPTO"
    INDICES = "INDICES"
    RATES = "RATES"

class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True)
    ticker = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    asset_class = Column(Enum(AssetClass), nullable=False)
    base_currency = Column(String(8), nullable=True)
    quote_currency = Column(String(8), nullable=True)

    quotes = relationship("MarketQuote", back_populates="instrument")
    history = relationship("MarketHistory", back_populates="instrument")

class MarketQuote(Base):
    __tablename__ = "market_quotes"

    id = Column(Integer, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False, index=True)
    price = Column(Numeric(18, 6), nullable=False)
    change_24h = Column(Float, nullable=True)
    source = Column(String(64), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    instrument = relationship("Instrument", back_populates="quotes")

class MarketHistory(Base):
    __tablename__ = "market_history"

    id = Column(Integer, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open = Column(Numeric(18, 6), nullable=True)
    high = Column(Numeric(18, 6), nullable=True)
    low = Column(Numeric(18, 6), nullable=True)
    close = Column(Numeric(18, 6), nullable=False)
    volume = Column(Float, nullable=True)

    instrument = relationship("Instrument", back_populates="history")

class MacroIndicator(Base):
    __tablename__ = "macro_indicators"

    id = Column(Integer, primary_key=True)
    series_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False)
    frequency = Column(String(16), nullable=False)
    source = Column(String(64), default="FRED")

    observations = relationship("MacroObservation", back_populates="macro_indicator")

class MacroObservation(Base):
    __tablename__ = "macro_observations"

    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey("macro_indicators.id"), nullable=False, index=True)
    observation_date = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=True)
    quality_status = Column(Enum(QualityStatus), default=QualityStatus.GOOD, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    macro_indicator = relationship("MacroIndicator", back_populates="observations")

    __table_args__ = (
        Index("ix_indicator_date", "indicator_id", "observation_date"),
    )
