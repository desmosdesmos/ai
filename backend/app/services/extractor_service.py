from typing import List, Dict, Any


PROMPT_TEMPLATE = (
	"Выдели из текста УК РФ пороги сумм и реквизиты (значительный/крупный/особо крупный). "
	"Верни JSON массив объектов с полями article, part, point, rekvizit, min, max, source_excerpt."
)


def extract_rules_from_text(text: str, article_hint: str | None = None) -> List[Dict[str, Any]]:
	# Stub: return empty list for now; LLM integration can be added later.
	return []

