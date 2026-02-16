from app import app, db, User, CargoType, Vehicle, Driver, Route
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_user_data():
    with app.app_context():
        # Создаем пользователя gulim если не существует
        user = User.query.filter_by(username='gulim').first()
        if not user:
            user = User(username='gulim', password=generate_password_hash('gulim'))
            db.session.add(user)
            db.session.commit()

        # Создаем типы груза для gulim
        cargo_types_data = [
            {'name': 'Электроника', 'description': 'Электронные устройства и комплектующие'},
            {'name': 'Мебель', 'description': 'Мебель и предметы интерьера'},
            {'name': 'Продукты', 'description': 'Продовольственные товары'},
        ]

        for cargo_data in cargo_types_data:
            if not CargoType.query.filter_by(name=cargo_data['name'], user_id=user.id).first():
                cargo = CargoType(**cargo_data, user_id=user.id)
                db.session.add(cargo)

        db.session.commit()

        # Создаем транспорт для gulim
        vehicles_data = [
            {'number': 'GULIM001', 'model': 'КамАЗ-65115', 'year': 2020, 'status': 'active'},
            {'number': 'GULIM002', 'model': 'ГАЗель Next', 'year': 2021, 'status': 'active'},
            {'number': 'GULIM003', 'model': 'MAN TGX', 'year': 2019, 'status': 'repair'},
        ]

        for vehicle_data in vehicles_data:
            if not Vehicle.query.filter_by(number=vehicle_data['number'], user_id=user.id).first():
                vehicle = Vehicle(**vehicle_data, user_id=user.id)
                db.session.add(vehicle)

        db.session.commit()

        # Создаем водителей для gulim
        drivers_data = [
            {'name': 'Иван Петров', 'contact': '+7 (999) 111-22-33'},
            {'name': 'Алексей Сидоров', 'contact': '+7 (999) 222-33-44'},
            {'name': 'Михаил Кузнецов', 'contact': '+7 (999) 333-44-55'},
        ]

        for driver_data in drivers_data:
            if not Driver.query.filter_by(name=driver_data['name'], user_id=user.id).first():
                driver = Driver(**driver_data, user_id=user.id)
                db.session.add(driver)

        db.session.commit()

        # Привязываем водителей к транспорту
        vehicles = Vehicle.query.filter(Vehicle.number.like('GULIM%'), Vehicle.user_id == user.id).all()
        drivers = Driver.query.filter(Driver.name.in_([d['name'] for d in drivers_data]), Driver.user_id == user.id).all()

        if len(drivers) >= 2 and len(vehicles) >= 2:
            drivers[0].vehicle_id = vehicles[0].id
            drivers[1].vehicle_id = vehicles[1].id

        db.session.commit()

        # Создаем маршруты для gulim
        cargo_types = CargoType.query.filter_by(user_id=user.id).all()
        routes_data = [
            {
                'name': 'Москва → Санкт-Петербург',
                'start_point': 'Москва',
                'end_point': 'Санкт-Петербург',
                'date': datetime.utcnow() + timedelta(days=1),
                'cargo_type_id': cargo_types[0].id if cargo_types else None,
                'vehicle_id': vehicles[0].id if vehicles else None,
                'driver_id': drivers[0].id if drivers else None,
                'cargo_weight': 15.5,
                'cargo_volume': 25.0,
                'fuel': 120.5,
                'trips_count': 2,
                'notes': 'Срочная доставка электроники'
            },
            {
                'name': 'Екатеринбург → Челябинск',
                'start_point': 'Екатеринбург',
                'end_point': 'Челябинск',
                'date': datetime.utcnow() + timedelta(days=2),
                'cargo_type_id': cargo_types[1].id if len(cargo_types) > 1 else None,
                'vehicle_id': vehicles[1].id if len(vehicles) > 1 else None,
                'driver_id': drivers[1].id if len(drivers) > 1 else None,
                'cargo_weight': 8.2,
                'cargo_volume': 15.0,
                'fuel': 45.0,
                'trips_count': 1,
                'notes': 'Доставка мебели'
            },
            {
                'name': 'Новосибирск → Омск',
                'start_point': 'Новосибирск',
                'end_point': 'Омск',
                'date': datetime.utcnow() - timedelta(days=5),
                'cargo_type_id': cargo_types[2].id if len(cargo_types) > 2 else None,
                'vehicle_id': vehicles[0].id if vehicles else None,
                'driver_id': drivers[0].id if drivers else None,
                'cargo_weight': 12.0,
                'cargo_volume': 18.0,
                'fuel': 85.0,
                'trips_count': 1,
                'notes': 'Продукты питания',
                'invoice_paid': True
            }
        ]

        for route_data in routes_data:
            # Проверяем, существует ли уже такой маршрут
            existing_route = Route.query.filter_by(
                name=route_data['name'],
                date=route_data['date'],
                user_id=user.id
            ).first()

            if not existing_route:
                route = Route(**route_data, user_id=user.id)
                db.session.add(route)

        db.session.commit()

        print("Данные для пользователя 'gulim' успешно добавлены!")

if __name__ == '__main__':
    seed_user_data()
