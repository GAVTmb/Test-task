import datetime
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

mushrooms_list = [
    {'id': 1, 'name': 'подберезовик', 'edibility': 'yes', 'weight': 50, 'freshness': '2024-09-01'},
    {'id': 3, 'name': 'белый', 'edibility': 'yes', 'weight': 60, 'freshness': '2024-09-01'},

]

baskets_list = [
    {'id': 1, 'name': 'Alex', 'volume': 2000,
     'mushrooms': [{'id': 2, 'name': 'мухомор', 'edibility': 'no', 'weight': 30, 'freshness': '2024-09-01'}, ]},
    {'id': 2, 'name': 'Bob', 'volume': 1500, 'mushrooms': []}
]


# Модель грибов.
# По поводу съедобности наверно было бы лучше сделать тип bool.
# И неуспел сделать автоматическое проставление id.
class Mushrooms(BaseModel):
    id: int
    name: str
    edibility: str
    weight: int
    freshness: datetime.date


# Модель корзинки
class Baskets(BaseModel):
    id: int
    name: str
    volume: int
    mushrooms: Optional[List[Mushrooms]] = []


# Создаем гриб и добавляем в базу(склад)
@app.post('/mushroom')
async def add_mushroom(mushroom: Mushrooms):
    mushrooms_list.append(mushroom.model_dump())
    return {'ok': True, 'data': mushrooms_list}


# Создаем корзинку и добавляем в базу
@app.post('/basket')
async def add_basket(basket: Baskets):
    baskets_list.append(basket.model_dump())
    return {'ok': True, 'data': baskets_list}


# Получаем гриб по id
@app.get('/mushroom/{mushroom_id}', response_model=Mushrooms)
def get_mushroom(mushroom_id: int):
    for mashroom in mushrooms_list:
        if mashroom['id'] == mushroom_id:
            return mashroom


# Получаем корзинку по id
@app.get('/basket/{basket_id}', response_model=Baskets)
def get_basket(basket_id: int):
    for basket in baskets_list:
        if basket['id'] == basket_id:
            return basket


# Добавляем гриб в карзину и удалям со склада.
# Хорошо было бы сделать отдельную функцию которая проверяла поместиться гриб в корзину или нет.
@app.post('/mushroom_in_the_basket')
def mushroom_in_the_basket(mushroom_id: int, basket_id: int):
    mash = get_mushroom(mushroom_id)
    basket = get_basket(basket_id).get('mushrooms')
    basket.append(mash)
    mushrooms_list.remove(mash)
    return {'ok': True, 'basket': baskets_list, 'mushroom': mushrooms_list}

# Удаляем гриб из корзинки и добавляем обратно на склад.
@app.delete('/remove_the_mushroom_from_the_basket')
def remove_the_mushroom_from_the_basket(basket_id: int, mushroom_id: int):
    mashrooms = get_basket(basket_id).get('mushrooms')
    for meshrum in mashrooms:
        if meshrum['id'] == mushroom_id:
            mushrooms_list.append(meshrum)
            mashrooms.remove(meshrum)
            return {'ok': True, 'basket': baskets_list, 'mushroom': mushrooms_list}
