# API - Chamadas Telefônicas
![Built with](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Built with](https://img.shields.io/pypi/pyversions/Django) 


Este projeto é uma aplicação web para gerenciamento de chamadas eletrônicas, desenvolvida utilizando Django para o backend e Docker com Docker Compose para orquestração de containers. O banco de dados utilizado é o PostgreSQL.

![](https://reactiongifs.me/cdn-cgi/imagedelivery/S36QsAbHn6yI9seDZ7V8aA/18f67a6f-c8fa-4903-1589-afde824de800/w=400)


# Pré-requisitos

- [Docker e docker-compose](https://docs.docker.com/engine/install/)

# Execução com docker-compose

```sh
git clone https://github.com/AfonsoDglan/TesteTecnico.git
```

```sh
cd TesteTecnico
```

```sh
mv .env-dev .env
```

```sh
docker-compose up -d --build
```

- Acesse a API em [http://localhost/](http://localhost/)

# Desenvolvimento

Para executar o servidor de desenvolvimento da API, você pode executar os seguintes comandos:

API - backend (Django):

```sh
pip install -r requirements.txt # (apenas na primeira execução ou se houverem novas dependências)
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```
# ambiente de trabalho
Neste projeto ultilizei as seguintes ferramentas:
- Notebook asus vivobook X513EAN
- Sistema operacional debian
- VS code
- Miniconda
- Docker
- Django
- Django rest framework
# Contribuindo

Contribuições são bem-vindas! Se você encontrou algum problema, tem uma ideia para uma nova funcionalidade ou simplesmente quer melhorar o projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.

# Licença

Este projeto está licenciado sob a Licença MIT.
