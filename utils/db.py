import sqlite3
import os
from flask import current_app, g

def get_db():
      if 'db' not in g:
         # Use PostgreSQL in production, SQLite in development
         database_url = current_app.config.get('DATABASE_URL')
         
         if database_url and database_url.startswith('postgres'):
            # PostgreSQL connection for production (Render)
            try:
               import psycopg2
               from psycopg2.extras import RealDictCursor
               g.db = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
               g.db_type = 'postgres'
            except Exception as e:
               print(f"PostgreSQL connection failed: {e}")
               raise
         else:
            # SQLite connection for development
            g.db = sqlite3.connect(
               current_app.config['DATABASE'],
               detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
            g.db_type = 'sqlite'

      return g.db


def close_db(e=None):
      db = g.pop('db', None)

      if db is not None:
         db.close()

def init_db():
   db = get_db()
   with current_app.open_resource('Schema.sql') as f:
      sql_script = f.read().decode('utf8')
      
      # Handle different database types
      if hasattr(g, 'db_type') and g.db_type == 'postgres':
         # For PostgreSQL, execute statements one by one
         cursor = db.cursor()
         try:
            cursor.execute(sql_script)
            db.commit()
         except Exception as e:
            print(f"Error initializing PostgreSQL database: {e}")
            db.rollback()
            raise
         finally:
            cursor.close()
      else:
         # For SQLite, use executescript
         db.executescript(sql_script)

def init_app(app):
   app.teardown_appcontext(close_db)