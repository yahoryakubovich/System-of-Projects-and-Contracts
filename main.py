from system import System


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
            contract_id = int(input("Enter contract ID to add to project: "))
            project_id = int(input("Enter project ID to add contract to: "))
            system.add_contract_to_project(contract_id, project_id)
        elif choice == '8':
            system.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
