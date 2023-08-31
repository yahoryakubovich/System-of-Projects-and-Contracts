from models import Session, Project, Contract
import datetime

class System:
    def __init__(self):
        self.session = Session()

    def create_project(self, name):
        project = Project(name=name)
        self.session.add(project)
        self.session.commit()
        print(f"Project '{name}' has been created.")

    def create_contract(self, name):
        contract = Contract(name=name)
        self.session.add(contract)
        self.session.commit()
        print(f"Contract '{name}' has been created.")

    def list_projects(self):
        projects = self.session.query(Project).all()
        if projects:
            print("Projects:")
            for project in projects:
                print(f"{project.id}. {project.name} ({len(project.contracts)} contracts)")
        else:
            print("No projects available.")

    def list_contracts(self):
        contracts = self.session.query(Contract).all()
        if contracts:
            print("Contracts:")
            for contract in contracts:
                project_name = contract.project.name if contract.project else "No project"
                print(f"{contract.id}. {contract.name} - Status: {contract.status}, Project: {project_name}")
        else:
            print("No contracts available.")

    def confirm_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            if contract.status == 'Draft':
                contract.status = 'Active'
                contract.signed_at = datetime.datetime.utcnow()
                self.session.commit()
                print(f"Contract '{contract.name}' has been confirmed and marked as Active.")
            else:
                print("Contract is not in Draft status and cannot be confirmed.")
        else:
            print("Contract not found.")

    def complete_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            if contract.status == 'Active':
                contract.status = 'Completed'
                self.session.commit()
                print(f"Contract '{contract.name}' has been completed.")
            else:
                print("Contract is not in Active status and cannot be completed.")
        else:
            print("Contract not found.")

    def add_contract_to_project(self, contract_id, project_id):
        contract = self.session.query(Contract).get(contract_id)
        project = self.session.query(Project).get(project_id)

        if not contract:
            print("Contract not found.")
            return

        if not project:
            print("Project not found.")
            return

        if contract.status != 'Active':
            print("Contract is not in Active status and cannot be added to a project.")
            return

        if project.has_active_contract():
            print("Project already has an active contract. Cannot add another active contract.")
            return

        contract.project = project
        self.session.commit()
        print(f"Contract '{contract.name}' has been added to project '{project.name}'.")

    def end_contract_in_project(self, contract_id, project_id):
        project = self.session.query(Project).get(project_id)
        if not project:
            print("Project not found.")
            return
        project.end_contract(contract_id)

    def close(self):
        self.session.close()
