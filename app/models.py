from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    PrimaryKeyConstraint
)

from app import db


class Champion(db.Model):
    __tablename__ = 'champions'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    title = Column(String(50))
    blurb = Column(String(500))
    infoAttack = Column(Integer, nullable=False)
    infoMagic = Column(Integer, nullable=False)
    infoDefense = Column(Integer, nullable=False)
    infoDifficulty = Column(Integer, nullable=False)
    statHP = Column(Float, nullable=False)
    statMP = Column(Float, nullable=False)
    statMoveSpeed = Column(Integer, nullable=False)
    statArmor = Column(Float, nullable=False)
    statAttackRange = Column(Integer, nullable=False)
    statAttackDamage = Column(Float, nullable=False)
    statAttackSpeed = Column(Float, nullable=False)

    def __repr__(self):
        return '<Champion %r>' % self.name

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'blurb': self.blurb,
            'infoAttack': self.infoAttack,
            'infoMagic': self.infoMagic,
            'infoDefense': self.infoDefense,
            'infoDifficulty': self.infoDifficulty,
            'statHP': self.statHP,
            'statMP': self.statMP,
            'statMoveSpeed': self.statMoveSpeed,
            'statArmor': self.statArmor,
            'statAttackRange': self.statAttackRange,
            'statAttackDamage': self.statAttackDamage,
            'statAttackSpeed': self.statAttackSpeed,
        }


class Class(db.Model):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

    def toDict(self):
        return {'id': self.id, 'name': self.name}


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

    def toDict(self):
        return {'id': self.id, 'name': self.name}


class ChampionClass(db.Model):
    __tablename__ = 'champion_class'
    __table_args__ = (
        PrimaryKeyConstraint('championId', 'classId'),
    )
    championId = Column(Integer, ForeignKey('champions.id', ondelete='CASCADE'), nullable=False)
    classId = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=True)

    def toDict(self):
        return {
            'championId': self.championId,
            'classId': self.classId,
        }

class ChampionRole(db.Model):
    __tablename__ = 'champion_role'
    __table_args__ = (
        PrimaryKeyConstraint('championId', 'roleId'),
    )
    championId = Column(Integer, ForeignKey('champions.id', ondelete='CASCADE'), nullable=False)
    roleId = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=True)

    def toDict(self):
        return {
            'championId': self.championId,
            'roleId': self.roleId,
        }


class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    explain = Column(String(200))
    buyPrice = Column(Integer, nullable=False)
    sellPrice = Column(Integer, nullable=False)
    tag = Column(String(30))

    def __repr__(self):
        return '<Item %r>' % self.name

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'explain': self.explain,
            'buyPrice': self.buyPrice,
            'sellPrice': self.sellPrice,
            'tag': self.tag
        }
