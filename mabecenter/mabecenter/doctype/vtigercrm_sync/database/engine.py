import frappe
from sqlalchemy import create_engine

db_user = frappe.conf.db_user_vtiger
db_password = frappe.conf.db_password_vtiger
db_host = frappe.conf.db_host_vtiger
db_port = frappe.conf.db_port_vtiger
db_name = frappe.conf.db_name_vtiger

connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
    connection_string,
    pool_pre_ping=True,
    pool_timeout=30,  # Connection timeout in seconds
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "connect_timeout": 10  # MySQL connection timeout
    }
)


    