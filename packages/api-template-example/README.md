# API Template Example

Example API client template.

## 📦 Installation

```bash
# From GitHub
pip install git+https://github.com/yourname/api-template-example.git

# For development
git clone https://github.com/yourname/api-template-example.git
cd api-template-example
pip install -e ".[dev]"
pre-commit install
```

## 🚀 Usage

```python
from api_template_example import APIClient

async with APIClient("https://api.example.com") as client:
    response = await client.get("/endpoint")
    print(response.data)
```

## 🛠️ Development

```bash
ruff check .      # Linting
ruff format .     # Formatting
mypy src          # Type checking
pytest            # Tests
```
