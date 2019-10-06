from gavel.models import db
import gavel.crowd_bt as crowd_bt
from sqlalchemy.orm.exc import NoResultFound

view_table = db.Table('view',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('annotator_id', db.Integer, db.ForeignKey('annotator.id'))
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    viewed = db.relationship('Annotator', secondary=view_table)
    prioritized = db.Column(db.Boolean, default=False, nullable=False)

    mu = db.Column(db.Float)
    sigma_sq = db.Column(db.Float)

    quest_beginner = db.Column(db.Integer)
    quest_entertainment = db.Column(db.Integer)
    quest_esri = db.Column(db.Integer)
    quest_fintech = db.Column(db.Integer)
    quest_security = db.Column(db.Integer)
    quest_hardware = db.Column(db.Integer)
    quest_startup = db.Column(db.Integer)

    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description
        self.mu = crowd_bt.MU_PRIOR
        self.sigma_sq = crowd_bt.SIGMA_SQ_PRIOR
        self.quest_beginner = 0
        self.quest_entertainment = 0
        self.quest_esri = 0
        self.quest_fintech = 0
        self.quest_security = 0
        self.quest_hardware = 0
        self.quest_startup = 0

    @classmethod
    def by_id(cls, uid):
        if uid is None:
            return None
        try:
            item = cls.query.get(uid)
        except NoResultFound:
            item = None
        return item
