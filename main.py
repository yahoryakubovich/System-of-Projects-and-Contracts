from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///project_contract.db')
Session = sessionmaker(bind=engine)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    contracts = relationship('Contract', back_populates='project')


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    signed_at = Column(DateTime)
    status = Column(Enum('Draft', 'Active', 'Completed'), default='Draft')
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='contracts')

    def confirm_contract(self):
        if self.status == 'Draft':
            self.status = 'Active'
            self.signed_at = datetime.datetime.utcnow()
            self.project.contracts.append(self)
            self.session.commit()
            print(f"Contract '{self.name}' has been confirmed and marked as Active.")

    def complete_contract(self):
        if self.status == 'Active':
            self.status = 'Completed'
            self.session.commit()
            print(f"Contract '{self.name}' has been completed.")


Base.metadata.create_all(engine)


class System:
    def __init__(self):
        self.session = Session()

    def confirm_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            contract.confirm_contract()
        else:
            print("Contract not found.")

    def complete_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            contract.complete_contract()
        else:
            print("Contract not found.")

    def create_project(self, name):
        project = Project(name=name)
        self.session.add(project)
        self.session.commit()
        print(f"Project '{name}' created.")

    def create_contract(self, name):
        contract = Contract(name=name)
        self.session.add(contract)
        self.session.commit()
        print(f"Contract '{name}' created.")

    def list_projects(self):
        projects = self.session.query(Project).all()
        for project in projects:
            print(f"Project ID: {project.id}, Name: {project.name}")

    def list_contracts(self):
        contracts = self.session.query(Contract).all()
        for contract in contracts:
            print(f"Contract ID: {contract.id}, Name: {contract.name}")

    def close(self):
        self.session.close()


def main():
    system = System()

    while True:
        print("1. Create Project")
        print("2. Create Contract")
        print("3. List Projects")
        print("4. List Contracts")
        print("5. Confirm Contract")
        print("6. Complete Contract")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter project name: ")
            system.create_project(name)
        elif choice == '2':
            name = input("Enter contract name: ")
            system.create_contract(name)
        elif choice == '3':
            system.list_projects()
        elif choice == '4':
            system.list_contracts()
        elif choice == '5':
            contract_id = int(input("Enter contract ID to confirm: "))
            system.confirm_contract(contract_id)
        elif choice == '6':
            contract_id = int(input("Enter contract ID to complete: "))
            system.complete_contract(contract_id)
        elif choice == '7':
            system.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
