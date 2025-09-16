from backend.app.utils.normalization import normalize_amount, map_rekvizit_code


def test_normalize_amount():
	assert normalize_amount("250 000") == 250000.0
	assert normalize_amount("1,5") == 1.5
	assert normalize_amount(None) is None


def test_map_rekvizit_code():
	assert map_rekvizit_code(1) == "крупный размер"
	assert map_rekvizit_code("2") == "особо крупный размер"
	assert map_rekvizit_code("x") is None

