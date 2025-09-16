from typing import Optional
from pydantic import BaseModel, Field


class RuleBase(BaseModel):
	article: str
	part: Optional[str] = None
	point: Optional[str] = None
	rekvizit: str
	# For input, accept keys "min"/"max"; internally we use min_amount/max_amount
	min_amount: Optional[float] = Field(default=None, validation_alias="min", serialization_alias="min")
	max_amount: Optional[float] = Field(default=None, validation_alias="max", serialization_alias="max")
	source_url: Optional[str] = None
	source_excerpt: Optional[str] = None
	confidence: Optional[float] = None
	status: Optional[str] = "pending"

	model_config = dict(populate_by_name=True, from_attributes=True)


class RuleCreate(RuleBase):
	pass


class RuleOut(RuleBase):
	id: int

