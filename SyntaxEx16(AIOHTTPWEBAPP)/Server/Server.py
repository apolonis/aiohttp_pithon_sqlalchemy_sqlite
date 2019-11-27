from aiohttp import web
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Model import Person
routes = web.RouteTableDef()


engine = Person.dbCreate()
session = sessionmaker(bind=engine)()
Base = declarative_base()

@routes.get('/')
async def handler(request):
    return web.Response(text="<h1 style=color:red>Web server is running</h1>",
                        content_type='text/html')

@routes.get('/home')
async def handler(request):
    return web.Response(text="<h1 style=color:blue>Home page </h1>",
                        content_type='text/html')

@routes.post("/path/{name}/{lastname}")
async def greet_user(request: web.Request) -> web.Response:

    # PATH VARIABLE
    person = Person.Person((request.match_info.get("name","")),(request.match_info.get("lastname","")))

    person1 = Person.Person("Some1","Other1")

    my_data = {"name": person.name, "lastname": person.lastname}
    my_data1 = {"name": person1.name, "lastname": person1.lastname}

    list = []
    list.append(my_data)
    list.append(my_data1)

    session.add(person)
    session.add(person1)
    session.commit()

    return web.json_response(list)

@routes.post("/postReq")
async def postReq(request):

    # REQUEST BODY
    data =await request.json()

    name = data["name"]
    lastname = data["lastname"]

    person = Person.Person(name,lastname)

    my_data = {"name": person.name, "lastname": person.lastname}

    list_ = []
    list_.append(my_data)

    session.add(person)
    session.commit()

    return web.json_response(list_)

@routes.get("/getAll")
async def getAll(request):

    result = [r for r in session.query(Person.Person).all()]

    list_ = []
    for r in result:
        my_data = {"name":r.name, "lastname":r.lastname}
        list_.append(my_data)

    return web.json_response(list_)

@routes.get("/get/{name}")
async def getByName(request: web.Request) -> web.Response:

    result = [r for r in session.query(Person.Person).all()]

    # person = Person.Person((request.match_info.get("name", "")), (request.match_info.get("lastname", "")))
    namE = request.match_info.get("name", "")
    list_ = []

    for r in result:
        if r.name == namE:
            my_data = {"name":r.name,"lastname":r.lastname}
            list_.append(my_data)

    return web.json_response(list_)




async def init_app() -> web.Application:

    app = web.Application()
    app.add_routes(routes)

    return app

Base.metadata.create_all(engine)
web.run_app(init_app())