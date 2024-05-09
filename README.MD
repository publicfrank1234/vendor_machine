# Project Name

This project is using Makefile targets and an in-memory ORM with FastAPI.

## Makefile Targets

### make help

Display help for available Makefile targets.


```bash
make help
make setup
make docker-build
make docker-test
make run-local 
```


### JWT Simplification 

```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    # For simplicity, assume the token is the user_id
    # Skipped jwt token validation
    user_id = token  # Simplification for example purposes
    return int(user_id)
```


### Tests
Most cases are covered under pytest 