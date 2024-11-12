from mirascope.core.azure._utils._convert_common_params import convert_common_params
from mirascope.core.base.call_params import CommonCallParams


def test_anthropic_conversion_full():
    """Test full parameter conversion for Anthropic."""
    params: CommonCallParams = {
        "temperature": 0.7,
        "max_tokens": 100,
        "top_p": 0.9,
        "stop": ["STOP", "END"],
    }
    result = convert_common_params(params)
    assert result == {
        "temperature": 0.7,
        "max_tokens": 100,
        "top_p": 0.9,
        "stop_sequences": ["STOP", "END"],
    }


def test_anthropic_conversion_single_stop():
    """Test single stop sequence conversion for Anthropic."""
    params: CommonCallParams = {
        "temperature": 0.7,
        "stop": "STOP",
    }
    result = convert_common_params(params)
    assert result == {
        "temperature": 0.7,
        "stop_sequences": ["STOP"],
    }


def test_anthropic_conversion_empty():
    """Test empty parameters conversion for Anthropic."""
    result = convert_common_params({})
    assert result == {}


def test_anthropic_conversion_none_values():
    """Test None values conversion for Anthropic."""
    params: CommonCallParams = {
        "temperature": None,
        "max_tokens": None,
    }
    result = convert_common_params(params)
    assert result == {}
