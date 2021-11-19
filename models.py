import os
from sqlalchemy import Column, String, Integer, Float, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

# DATABASE URL
"""
DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'fwd2021')
DB_NAME = os.getenv('DB_NAME', 'covid')

database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
"""

database_path='postgresql://qrjpxglmlwfvmj:0704636590cebfd1a6fe3b8942bf8d8c936a8bd5e12bd3765f3a6c88af9fb604@ec2-23-23-133-10.compute-1.amazonaws.com:5432/dcup748f1vqo46'


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#def db_drop_and_create_all():
   # """
   #     drops the existing database tables & creates a new
   # """
   # db.drop_all()
   # #db.create_all()

'''
Cases

'''
class Cases(db.Model):  
  __tablename__ = 'cases_agegroup'

  age_group = Column(String, primary_key=True)
  total_num_case = Column(Integer)
  total_num_intensivecare = Column(Integer)
  total_num_death= Column(Integer)

  def __init__(self, age_group, total_num_case, total_num_intensivecare, total_num_death):
    self.age_group = age_group
    self.total_num_case = total_num_case
    self.total_num_intensivecare = total_num_intensivecare
    self.total_num_death = total_num_death

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'age_group': self.age_group,
      'total_num_case': self.total_num_case,
      'total_num_intensivecare': self.total_num_intensivecare,
      'total_num_death': self.total_num_death
    }

  def __repr__(self):
      return json.dumps(self.format())

'''
Vaccination

'''
class Vaccination(db.Model):  
  __tablename__ = 'vacc_region_agegroup'

  id = Column(Integer, primary_key=True)
  region = Column(String)
  kommun_namn  = Column(String)
  age_group  = Column(String, ForeignKey('cases_agegroup.age_group'))
  population = Column(Integer)
  num_minst_1_dos = Column(Integer)
  num_fully_vaccinated  = Column(Integer)
  proportion_of_minst_1_dos = Column(Float)
  proportion_of_fully_vaccinated = Column(Float)
  cases = relationship('Cases')

  def __init__(self, id, region, kommun_namn, age_group, population, num_minst_1_dos, num_fully_vaccinated, proportion_of_minst_1_dos, proportion_of_fully_vaccinated):

    self.id = id
    self.region = region
    self.kommun_namn = kommun_namn
    self.age_group = age_group
    self.population = population
    self.num_minst_1_dos = num_minst_1_dos
    self.num_fully_vaccinated = num_fully_vaccinated
    self.proportion_of_minst_1_dos = proportion_of_minst_1_dos
    self.proportion_of_fully_vaccinated = proportion_of_fully_vaccinated

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'vaccination_info_id': self.id,
      'region': self.region,
      'kommun_namn': self.kommun_namn,
      'age_group': self.age_group,
      'population': self.population,
      'num_minst_1_dos': self.num_minst_1_dos,
      'num_fully_vaccinated': self.num_fully_vaccinated,
      'proportion_of_minst_1_dos': self.proportion_of_minst_1_dos,
      'proportion_of_fully_vaccinated': self.proportion_of_fully_vaccinated

    }

  def __repr__(self):
      return json.dumps(self.format())
