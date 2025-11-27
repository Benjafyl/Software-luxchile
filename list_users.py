from app.db.database import SessionLocal
from app.models.users import User

db = SessionLocal()
users = db.query(User).all()

print('\n' + '='*60)
print('  USUARIOS REGISTRADOS EN EL SISTEMA')
print('='*60)

for i, u in enumerate(users, 1):
    print(f'\n[{i}] Usuario: {u.username}')
    print(f'    Rol: {u.role}')
    print(f'    RUT: {u.rut or "N/A"}')
    print(f'    Nombre: {u.full_name or "N/A"}')

print('\n' + '='*60)
print(f'Total de usuarios: {len(users)}')
print('='*60)

db.close()
