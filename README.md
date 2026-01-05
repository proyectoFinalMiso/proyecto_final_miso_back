# ERP Backend

This is a graduation project for Master's of Engineering in Software. The scope of this project is limited to backend for an ERP designed previously by a team of 4. You can check more about the design and modules to understand the backend better in this [repository](https://github.com/diegonaranjo94/proyecto_final_miso_arquitectura/tree/main). The most important aspects of this projects are:

## Python Version
- **Python 3.12** (see Pipfile and Dockerfile for each microservice)

## Frameworks & Libraries
- **Flask** (main web framework)
- **Flask-SQLAlchemy** (ORM)
- **Marshmallow** (serialization/validation)
- **Waitress** (production WSGI server)
- **pytest** (testing)
- **pipenv** (dependency management)

## Folder Structure

```
proyecto_final_miso_back/
│
├── gestorClientes/
│   ├── app.py
│   ├── Dockerfile
│   ├── Pipfile
│   ├── src/
│   │   ├── blueprints/
│   │   ├── commands/
│   │   ├── constants/
│   │   └── models/
│   └── tests/
│
├── productos/
│   ├── app.py
│   ├── Dockerfile
│   ├── Pipfile
│   ├── src/
│   └── tests/
│
├── bodega/
│   ├── app.py
│   ├── Dockerfile
│   ├── Pipfile
│   ├── src/
│   └── tests/
│
├── vendedores/
│   ├── app.py
│   ├── Dockerfile
│   ├── Pipfile
│   ├── src/
│   └── tests/
│
├── bffClientes/
├── bffWeb/
├── gestorPedidos/
│
└── .github/
	 └── workflows/
		  └── pipeline_ci.yml
```

## Testing

- All microservices use **pytest** for unit and integration tests.
- Example: [gestorClientes/tests/](gestorClientes/tests/)
- To run tests for a microservice:
  ```bash
  cd gestorClientes
  pipenv install --dev
  pipenv run pytest
  ```

## GitHub Actions

- CI pipeline defined in [.github/workflows/pipeline_ci.yml](.github/workflows/pipeline_ci.yml)
- Runs tests on push/pull request to `main` and `develop` branches.
- Example job for `productos`:
  - Installs dependencies with pipenv
  - Runs pytest with coverage

## How to Run

### Local Development

1. **Install pipenv** (if not installed):
	```bash
	pip install pipenv
	```

2. **Install dependencies**:
	```bash
	cd gestorClientes
	pipenv install
	```

3. **Run the app**:
	```bash
	pipenv run python app.py dev
	```
	- For production, use:
	  ```bash
	  pipenv run python app.py production
	  ```

4. **Run with Docker**:
	```bash
	docker build -t gestor-clientes .
	docker run -p 3007:3007 gestor-clientes
	```

### API Endpoints

To see detailed information about each enpoint in this project please check the [Postman collection file](https://github.com/proyectoFinalMiso/proyecto_final_miso_back/blob/main/proyecto_final.postman_collection.json) with all the details.

---

You can contact me and get more information through:

<div>
  <p align="center">
  <a href="https://www.linkedin.com/in/diegonaranjo94/" target="blank">
    <img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="imorange" height="30" width="40" />
    </a>
  <a href="https://www.instagram.com/diegonaranjo.94/" target="blank">
    <img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="imorange" height="30" width="40" />
    </a>
  <a href="https://github.com/diegonaranjo94" target="blank">
    <img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg" alt="imorange" height="30" width="40" />
    </a>
  </p>
</div>
