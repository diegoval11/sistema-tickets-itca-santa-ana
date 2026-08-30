# 🎫 Sistema de Tickets — ITCA FEPADE

Plataforma web de **mesa de ayuda (helpdesk)** para gestionar solicitudes de soporte técnico en el ITCA FEPADE. Permite a usuarios reportar incidencias y a técnicos darles seguimiento, programar visitas, registrar su historial y exportar reportes.

> Proyecto de práctica académica — Django + Tailwind CSS.

---

## ✨ Funcionalidades

**Usuarios**
- Crear tickets de soporte con descripción, categoría, prioridad, equipo afectado y fotos (máx. 5, JPG/PNG).
- Consultar el estado y avance de sus tickets.
- Recibir notificaciones en la app y por correo sobre cada cambio.

**Técnicos**
- Dashboard con métricas: total, abiertos, en progreso, cerrados, tiempo promedio de resolución, tickets por categoría/prioridad/estado.
- Gestión de usuarios con **códigos de acceso** (login por correo + código).
- Actualizar tickets: cambiar estado, programar visitas, registrar motivo de rechazo / nota de cierre.
- Exportar reportes en **Excel (XLSX)** con métricas o **CSV**, con filtros de fecha.

**Generales**
- Roles (`TECNICO` / `USUARIO`) y permisos por vista.
- Historial de cambios (auditoría) por ticket.
- Archivo automático de tickets antiguos (30 días).
- Tema oscuro responsive (Tailwind CSS).

## 🛠️ Stack

| Capa | Tecnología |
|------|------------|
| Backend | Python · Django 5.0 |
| Base de datos | SQLite |
| Frontend | HTML + Tailwind CSS (CDN) |
| Reportes | openpyxl (XLSX) · CSV |
| Adjuntos | Pillow · `media/ticket_photos/` |

## 🚀 Cómo correrlo

```bash
# 1. Clonar
git clone https://github.com/diegoval11/sistema-tickets-itca-santa-ana.git
cd sistema-tickets-itca-santa-ana

# 2. Entorno virtual (Python 3.11+)
python3 -m venv .venv
source .venv/bin/activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Base de datos (viene commiteada con datos demo; si la quieres fresca, bórrala primero)
python manage.py migrate

# 5. Crear tu superusuario técnico
python manage.py createsuperuser

# 6. Levantar el servidor
python manage.py runserver
```

Abre <http://127.0.0.1:8000> e inicia sesión con tu correo institucional + código de acceso.

> ⚠️ El login no usa contraseña: cada usuario tiene un **código de acceso** de 12 caracteres visible en *Gestión de Usuarios* (rol técnico).

## 👤 Credenciales demo

| Rol | Correo | Código de acceso |
|-----|--------|------------------|
| Técnico | `admin@itca.edu.sv` | `5VSUPPWIMJB6` |
| Usuario | `usuario1@itca.edu.sv` | `ZWIXRBMX9LVQ` |

## 📁 Estructura

```
├── helpdesk_project/      # Configuración del proyecto (settings, urls, wsgi)
├── tickets/               # App principal (views, forms, models, admin)
├── templates/             # Plantillas HTML (Tailwind)
├── static/                # Estáticos (logo)
├── media/                 # Fotos adjuntas de tickets
├── manage.py
└── requirements.txt
```

## 🧭 Rutas principales

| URL | Vista |
|-----|-------|
| `/` | Login (correo + código de acceso) |
| `/tickets/` | Mis tickets |
| `/tickets/create/` | Crear ticket |
| `/tickets/<id>/` | Detalle del ticket |
| `/dashboard/` | Dashboard técnico |
| `/users/` | Gestión de usuarios |
| `/notifications/` | Notificaciones |
| `/export/` | Exportar reportes |