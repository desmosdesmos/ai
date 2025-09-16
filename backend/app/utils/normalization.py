from typing import Optional, Tuple


REKVIZIT_CODE_TO_NAME = {
	1: "крупный размер",
	2: "особо крупный размер",
	3: "значительный ущерб",
	4: "крупный ущерб",
	5: "особо крупный ущерб",
	6: "значительный размер",
}


def normalize_article(value: str) -> str:
	return str(value).strip()


def normalize_part(value: Optional[str]) -> Optional[str]:
	if value is None:
		return None
	s = str(value).strip()
	return s or None


def normalize_point(value: Optional[str]) -> Optional[str]:
	if value is None:
		return None
	s = str(value).strip()
	return s or None


def normalize_amount(value) -> Optional[float]:
	if value is None or value == "":
		return None
	try:
		return float(str(value).replace(" ", "").replace(",", "."))
	except Exception:
		return None


def map_rekvizit_code(code_value) -> Optional[str]:
	try:
		code_int = int(code_value)
		return REKVIZIT_CODE_TO_NAME.get(code_int)
	except Exception:
		return None

