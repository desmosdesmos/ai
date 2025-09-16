from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..db import Base


class RuleStatusEnum(Enum):
	PENDING = "pending"
	APPROVED = "approved"
	REJECTED = "rejected"


class Rule(Base):
	__tablename__ = "rules"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	article: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
	part: Mapped[Optional[str]] = mapped_column(String(16), index=True, nullable=True)
	point: Mapped[Optional[str]] = mapped_column(String(16), index=True, nullable=True)
	rekvizit: Mapped[str] = mapped_column(String(64), nullable=False)
	min_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
	max_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
	source_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	source_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
	status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessingJob(Base):
	__tablename__ = "processing_jobs"

	id: Mapped[str] = mapped_column(String(64), primary_key=True)
	status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
	input_path: Mapped[str] = mapped_column(Text, nullable=False)
	output_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Source(Base):
	__tablename__ = "sources"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(64), unique=True)
	base_url: Mapped[str] = mapped_column(Text)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RuleVersion(Base):
	__tablename__ = "rule_versions"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	rule_id: Mapped[int] = mapped_column(Integer, ForeignKey("rules.id"), index=True)
	version: Mapped[str] = mapped_column(String(32))
	content_json: Mapped[str] = mapped_column(Text)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

