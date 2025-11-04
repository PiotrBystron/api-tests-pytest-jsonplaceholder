# API Tests with Pytest

A simple project demonstrating API testing using **pytest**, **requests**, and **pytest-html**  
on the public [JSONPlaceholder](https://jsonplaceholder.typicode.com) REST API.

---

## How to run

### 1. Clone repository

```bash
git clone https://github.com/PiotrBystron/api-tests-pytest-jsonplaceholder.git
```

```bash
cd api-tests-pytest-jsonplaceholder
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the tests

```bash
pytest --html=report.html --self-contained-html
```

A detailed report will be generated as report.html in the project folder.