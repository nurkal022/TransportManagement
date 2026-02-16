from app import app, db, User, CargoType, Vehicle, Driver, Route
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_database():
    # Пересоздаем все таблицы
    db.drop_all()
    db.create_all()
    
    # Создаем администратора
    admin = User(
        username='admin',
        password=generate_password_hash('admin')
    )
    db.session.add(admin)
    
    # Создание типов грузов
    cargo_types = [
        CargoType(name='Сборный груз', description='Разные типы товаров в одной перевозке'),
        CargoType(name='Продукты питания', description='Скоропортящиеся продукты, требующие особых условий'),
        CargoType(name='Стройматериалы', description='Строительные материалы и оборудование'),
        CargoType(name='Техника', description='Бытовая техника и электроника'),
        CargoType(name='Мебель', description='Мебель и предметы интерьера')
    ]
    
    for cargo_type in cargo_types:
        db.session.add(cargo_type)
    
    # Создание транспортных средств
    vehicles = [
        Vehicle(number='777KZ01', model='Volvo FH16', year=2022, status='active'),
        Vehicle(number='888KZ01', model='Mercedes Actros', year=2021, status='active'),
        Vehicle(number='999KZ01', model='MAN TGX', year=2023, status='active'),
        Vehicle(number='111KZ01', model='Scania R500', year=2020, status='active'),
        Vehicle(number='222KZ01', model='DAF XF', year=2021, status='active')
    ]
    
    for vehicle in vehicles:
        db.session.add(vehicle)
    
    # Применяем изменения, чтобы получить ID
    db.session.commit()
    
    # Создание водителей
    drivers = [
        Driver(name='Ахметов Азамат', contact='+7 (701) 555-11-11', vehicle_id=vehicles[0].id),
        Driver(name='Сериков Бауыржан', contact='+7 (702) 555-22-22', vehicle_id=vehicles[1].id),
        Driver(name='Нурланов Ерлан', contact='+7 (703) 555-33-33', vehicle_id=vehicles[2].id),
        Driver(name='Касымов Дархан', contact='+7 (705) 555-44-44', vehicle_id=vehicles[3].id),
        Driver(name='Жумабаев Марат', contact='+7 (707) 555-55-55', vehicle_id=vehicles[4].id)
    ]
    
    for driver in drivers:
        db.session.add(driver)
    
    # Сохраняем все изменения
    db.session.commit()
    print("База данных успешно заполнена базовыми данными!")

def seed_test_data():
    with app.app_context():
        # Очистка существующих данных
        Route.query.delete()
        Driver.query.delete()
        Vehicle.query.delete()
        CargoType.query.delete()
        
        # Создание типов грузов
        cargo_types = [
            CargoType(name='Продукты питания', description='Скоропортящиеся продукты'),
            CargoType(name='Строительные материалы', description='Тяжелые стройматериалы'),
            CargoType(name='Мебель', description='Мебель и предметы интерьера'),
            CargoType(name='Техника', description='Электроника и бытовая техника'),
        ]
        for ct in cargo_types:
            db.session.add(ct)
        db.session.commit()
        
        # Создание транспортных средств
        vehicles = [
            Vehicle(number='A001BC', model='Volvo FH16', year=2022, status='active'),
            Vehicle(number='B002CD', model='Mercedes Actros', year=2021, status='active'),
            Vehicle(number='C003DE', model='Scania R500', year=2023, status='active'),
            Vehicle(number='D004EF', model='MAN TGX', year=2022, status='active'),
        ]
        for v in vehicles:
            db.session.add(v)
        db.session.commit()
        
        # Создание водителей
        drivers = [
            Driver(name='Иванов Иван', contact='+7-900-111-22-33', vehicle_id=vehicles[0].id),
            Driver(name='Петров Петр', contact='+7-900-222-33-44', vehicle_id=vehicles[1].id),
            Driver(name='Сидоров Сидор', contact='+7-900-333-44-55', vehicle_id=vehicles[2].id),
            Driver(name='Александров Александр', contact='+7-900-444-55-66', vehicle_id=vehicles[3].id),
        ]
        for d in drivers:
            db.session.add(d)
        db.session.commit()
        
        # Создание маршрутов
        base_date = datetime.now()
        routes = [
            Route(
                name='Доставка продуктов в сеть магазинов',
                start_point='Москва',
                end_point='Санкт-Петербург',
                date=base_date + timedelta(days=1),
                estimated_arrival=base_date + timedelta(days=1, hours=8),
                cargo_type_id=cargo_types[0].id,
                vehicle_id=vehicles[0].id,
                driver_id=drivers[0].id,
                cargo_weight=5000,
                cargo_volume=20,
                trips_count=1,
                notes='Срочная доставка'
            ),
            Route(
                name='Перевозка стройматериалов',
                start_point='Екатеринбург',
                end_point='Челябинск',
                date=base_date + timedelta(days=2),
                estimated_arrival=base_date + timedelta(days=2, hours=6),
                cargo_type_id=cargo_types[1].id,
                vehicle_id=vehicles[1].id,
                driver_id=drivers[1].id,
                cargo_weight=15000,
                cargo_volume=30,
                trips_count=2,
                notes='Тяжелый груз'
            ),
            Route(
                name='Доставка мебели',
                start_point='Новосибирск',
                end_point='Красноярск',
                date=base_date + timedelta(days=3),
                estimated_arrival=base_date + timedelta(days=3, hours=10),
                cargo_type_id=cargo_types[2].id,
                vehicle_id=vehicles[2].id,
                driver_id=drivers[2].id,
                cargo_weight=3000,
                cargo_volume=40,
                trips_count=1,
                notes='Хрупкий груз'
            ),
            Route(
                name='Перевозка бытовой техники',
                start_point='Казань',
                end_point='Нижний Новгород',
                date=base_date + timedelta(days=4),
                estimated_arrival=base_date + timedelta(days=4, hours=5),
                cargo_type_id=cargo_types[3].id,
                vehicle_id=vehicles[3].id,
                driver_id=drivers[3].id,
                cargo_weight=2500,
                cargo_volume=15,
                trips_count=1,
                notes='Ценный груз'
            ),
            # Дополнительные маршруты с разными датами
            Route(
                name='Доставка продуктов в гипермаркет',
                start_point='Санкт-Петербург',
                end_point='Москва',
                date=base_date - timedelta(days=1),
                estimated_arrival=base_date - timedelta(hours=16),
                cargo_type_id=cargo_types[0].id,
                vehicle_id=vehicles[0].id,
                driver_id=drivers[0].id,
                cargo_weight=4500,
                cargo_volume=18,
                trips_count=1,
                notes='Обратный рейс'
            ),
            Route(
                name='Перевозка строительного оборудования',
                start_point='Челябинск',
                end_point='Екатеринбург',
                date=base_date + timedelta(days=5),
                estimated_arrival=base_date + timedelta(days=5, hours=6),
                cargo_type_id=cargo_types[1].id,
                vehicle_id=vehicles[1].id,
                driver_id=drivers[1].id,
                cargo_weight=12000,
                cargo_volume=25,
                trips_count=1,
                notes='Специальное оборудование'
            ),
        ]
        for r in routes:
            db.session.add(r)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_database()
        seed_test_data()
        print("База данных успешно заполнена базовыми данными и тестовыми данными!") 