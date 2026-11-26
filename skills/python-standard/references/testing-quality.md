# Python Testing And Quality

Use this reference for pytest, unittest, mocks, fixtures, coverage, type checking, linting, and formatting.

## Test Selection

Use the narrowest test that proves the behavior:

- Pure functions: unit tests with direct inputs/outputs.
- Services/adapters: tests with mocked external boundary or local fake.
- Database behavior: integration tests against the repo's test database setup.
- Web APIs: request/client tests through the framework test client.
- CLIs: invoke through Click/Typer/argparse test helpers or subprocess when shell behavior matters.

## Pytest Patterns

Prefer fixtures for reusable setup and `parametrize` for data variations.

```python
@pytest.mark.parametrize("raw,expected", [("1", 1), (" 2 ", 2)])
def test_parse_count(raw: str, expected: int) -> None:
    assert parse_count(raw) == expected
```

Mock at the boundary you own, not the implementation detail under test. Avoid mocking the function whose behavior you are trying to prove.

## Async Tests

Use the project's async test plugin/style (`pytest.mark.asyncio`, AnyIO, framework helpers). Await the behavior under test and assert cleanup/cancellation when relevant.

## Quality Commands

Run the repo's scripts when present. Common commands:

```bash
pytest
pytest path/to/test_file.py::test_name
ruff check .
ruff format --check .
black --check .
mypy .
pyright
python -m build
```

Do not run broad destructive database reset commands unless the repo clearly marks them as test-only.

## Coverage

Add focused assertions for changed behavior, not coverage theater. Cover success, validation failure, edge cases, and important error paths.

Mention residual risk when verification cannot run locally.
