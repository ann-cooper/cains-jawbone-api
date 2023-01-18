from datetime import datetime

from flask_alembic import Alembic
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy

# Create the mongo service
mgdb = MongoEngine()

# Create postgres service
db = SQLAlchemy()

# Create marshmallow serialization
mllw = Marshmallow()

# Create alembic DB migration service
alembic = Alembic()
# alembic.rev_id = lambda: datetime.utcnow().strftime("%Y%m%d%H%M%S%f")  # TODO delete

migrate = Migrate()