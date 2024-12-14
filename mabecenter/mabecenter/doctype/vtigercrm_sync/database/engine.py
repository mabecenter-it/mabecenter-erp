# Import Frappe framework for configuration access
import frappe
# Import SQLAlchemy engine creation function
from sqlalchemy import create_engine

# Get database connection details from Frappe configuration
db_user = frappe.conf.db_user_vtiger
db_password = frappe.conf.db_password_vtiger
db_host = frappe.conf.db_host_vtiger
db_port = frappe.conf.db_port_vtiger
db_name = frappe.conf.db_name_vtiger

# Build MySQL connection string
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" if db_user and db_password and db_host and db_port and db_name else None

# Create SQLAlchemy engine with connection pooling settings
if connection_string:
    engine = create_engine(
        connection_string,
        pool_pre_ping=True,         # Check connection before use
        pool_timeout=30,            # Connection timeout in seconds
        pool_recycle=3600,          # Recycle connections after 1 hour
        connect_args={
            "connect_timeout": 10   # MySQL connection timeout
        }
    )


    