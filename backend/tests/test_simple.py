"""Simple tests without external dependencies."""

def test_addition():
    """Test basic addition."""
    result = 1 + 1
    if result != 2:
        raise AssertionError(f"1 + 1 = {result}, expected 2")

def test_string():
    """Test string operations."""
    result = "hello" + " world"
    if result != "hello world":
        raise AssertionError(f"String concatenation failed, got: {result}")

def test_list():
    """Test list operations."""
    result = [1, 2] + [3, 4]
    if result != [1, 2, 3, 4]:
        raise AssertionError(f"List concatenation failed, got: {result}")

# Add a main function to allow running this file directly
if __name__ == "__main__":
    print("Running simple tests...")
    test_addition()
    test_string()
    test_list()
    print("All tests passed!")