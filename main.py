'''
# Path parameter vs query parameter ----------------------------------------------------------------------------------------------
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def read_root():
    return{"hello": "world"}

@app.get("/user/{id}")
async def read_user(id: str):
    #return id
    return{"id":id}

# 8000/?id='1'&id1='2'&id2='3'
# @app.get("/user/")
# async def read_root(id, id1, id2):
#     return id

@app.get("/user/")
async def read_user(id: str=Query(max_length=5)):
    return{"id": id}
'''

'''
# 메뉴정보 CRUD -------------------------------------------------------------------------------------------------------------------
from fastapi import FastAPI

app = FastAPI()

# 메뉴 저장 리스트
menu_list:list = []

# healthcheck
@app.get("/")
async def read_root():
    return{"hello":"world"}

# 특정 메뉴 취득
@app.get("/menu/{food}")
async def read_menu(food:str):
    for menu in menu_list:
        if menu["food"] == food:
            return menu
    return "선택한 메뉴는 없습니다."

# 메뉴 전체 취득
@app.get("/menus/")
async def read_menus():
    return menu_list

# 메뉴 등록
@app.post("/menu/")
async def create_menu(food: str, img: str):
    menu_list.append({"food":food, "img":img})
    return "메뉴가 등록되었습니다."

# 메뉴 정보 수정
@app.put("/menu/")
async def update_menu(food:str, img:str):
    for menu in menu_list:
        if menu["food"] == food:
            menu["img"] = img
            return "수정 되었습니다."
    return "없는 메뉴는 없습니다."

# 특적 메뉴 삭제
@app.delete("/menu/{food}")
async def delete_menu(food:str):
    for menu in menu_list:
        if menu["food"] == food:
            menu_list.remove(menu)
            return "삭제가 되었습니다."
    return "없는 메뉴는 없습니다."

'''
# 메뉴 정보 CRUD(DB) - DB Connection------------------------------------------------------------------------------------------------------
from model import Menu
from db import session
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 처리
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# healthcheck
@app.get("/")
async def read_root():
    return{"hello":"world"}

# 특정 메뉴 취득
@app.get("/menu/{food}")
async def read_menu(food:str):
    menu = session.query(Menu).filter(Menu.food == food).first()
    if not menu:
        return "선택한 메뉴는 없습니다."
    return menu

# 메뉴 전체 취득
@app.get("/menus/")
async def read_menus():
    return session.query(Menu).all()

# 메뉴 등록
@app.post("/menu/")
async def create_menu(food: str = Body(...), rating: int = Body(...), courseId: int = Body(...)):
    print(food, rating)
    menu = Menu()
    menu.food = food
    menu.rating = rating
    menu.courseId = courseId
    try:
        session.add(menu)
        session.commit()
        return {"message": "메뉴가 등록되었습니다."}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="고유키 제약 조건을 위반했습니다.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="서버 에러가 발생했습니다.")

# 메뉴 정보 수정
@app.put("/menu/")
async def update_menu(food: str = Body(...), rating: str = Body(...)):
    menu = session.query(Menu).filter(Menu.food == food).first()
    if not menu:
        return "없는 메뉴는 없습니다."
    menu.rating = rating
    session.commit()
    return "수정이 되었습니다."


# 특적 메뉴 삭제
@app.delete("/menu/{food}")
async def delete_menu(food:str):
    menu = session.query(Menu).filter(Menu.food == food).delete()
    if menu == 0:
        return "없는 메뉴는 없습니다."
    session.commit()
    return "삭제가 되었습니다."

'''
# UI 적용해서 만들기
from fastapi import FastAPI, Body
from model import Menu, Order
from db import session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],     
    allow_headers=["*"],     
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# 특정 메뉴 취득 
@app.get("/menu/{food}")
async def read_menu(food: str):
    menu = session.query(Menu).filter(Menu.food == food).first()
    if not menu: 
        return "선택한 메뉴는 없습니다"
    return menu

# 메뉴 전체 취득
@app.get("/menus/")
async def read_menus():
    return session.query(Menu).all()

# 메뉴 등록
@app.post("/menu/")
async def create_menu(food: str = Body(...), img: str = Body(...)):
    menu = Menu()
    menu.food = food
    menu.img = img
    session.add(menu)
    session.commit()
    return "메뉴가 등록되었습니다!"

# 메뉴 정보 수정
@app.put("/menu/")
async def update_menu(food: str = Body(...), img:str = Body(...)):
    menu = session.query(Menu).filter(Menu.food == food).first()
    if not menu:
        return "없는 메뉴는 없습니다"
    menu.img = img
    session.commit()
    return "수정이 되었습니다!"

# 특정 메뉴 삭제
@app.delete("/menu/{food}")
async def delete_menu(food: str):
    menu = session.query(Menu).filter(Menu.food == food).delete()
    if menu == 0:
        return "없는 메뉴는 없습니다"
    session.commit()
    return "삭제가 되었습니다!"

# 주문 정보 등록
@app.post("/order/")
async def create_order(name: str = Body(...), food: str = Body(...)):
    order = Order()
    order.name = name
    order.food = food
    session.add(order)
    session.commit()
    return "주문이 등록되었습니다!"

# 주문 정보 취득
@app.get("/order/")
async def get_order():
    results =  session.query(Order, Menu).filter(Order.food == Menu.food).all()
    response = [{"name": order.name, "food": menu.food ,"img": menu.img} for order, menu in results]
    return response

# 특정 메뉴 삭제
@app.delete("/order/{food}")
async def delete_menu(food: str):
    menu = session.query(Order).filter(Order.food == food).delete()
    if menu == 0:
        return "없는 메뉴는 없습니다"
    session.commit()
    return "삭제가 되었습니다!"
'''