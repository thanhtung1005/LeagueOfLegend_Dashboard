from app import db


class Champion(db.Model):
    __tablename__ = 'champions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(50))
    blurb = db.Column(db.String(500))
    infoAttack = db.Column(db.Integer, nullable=False)
    infoMagic = db.Column(db.Integer, nullable=False)
    infoDefense = db.Column(db.Integer, nullable=False)
    infoDifficulty = db.Column(db.Integer, nullable=False)
    statHP = db.Column(db.Float, nullable=False)
    statMP = db.Column(db.Float, nullable=False)
    statMoveSpeed = db.Column(db.Integer, nullable=False)
    statArmor = db.Column(db.Float, nullable=False)
    statAttackRange = db.Column(db.Integer, nullable=False)
    statAttackDamage = db.Column(db.Float, nullable=False)
    statAttackSpeed = db.Column(db.Float, nullable=False)

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def toDict(self):
        return {'id': self.id, 'name': self.name}


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def toDict(self):
        return {'id': self.id, 'name': self.name}


class ChampionClassRole(db.Model):
    __tablename__ = 'champion_class_role'
    id = db.Column(db.Integer, primary_key=True)
    championName = db.Column(db.String(20), db.ForeignKey('champions.name', ondelete='CASCADE'), nullable=False)
    className = db.Column(db.String(20), db.ForeignKey('classes.name', ondelete='CASCADE'), nullable=False)
    roleName = db.Column(db.String(20), db.ForeignKey('roles.name', ondelete='CASCADE'), nullable=False)

    def toDict(self):
        return {
            'id': self.id,
            'championName': self.championName,
            'className': self.className,
            'roleName': self.roleName
        }


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    explain = db.Column(db.String(200))
    buyPrice = db.Column(db.Integer, nullable=False)
    sellPrice = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(30))

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
