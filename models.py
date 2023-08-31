from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    contracts = relationship("Contract", back_populates="project")

    def has_active_contract(self):
        return any(contract.status == 'Active' for contract in self.contracts)

    def end_contract(self, contract_id):
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.status = 'Completed'
                self.session.commit()
                print(f"Contract '{contract.name}' has been marked as completed in project '{self.name}'.")
                return

        print("Contract not found in the project.")

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    signed_at = Column(DateTime)
    status = Column(String, default='Draft')
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="contracts")

engine = create_engine('sqlite:///projects_and_contracts.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
