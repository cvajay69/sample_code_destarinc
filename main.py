
import json

class Employee:
    def __init__(self, name, emp_id, title, department):
        self.name = name
        self.emp_id = emp_id
        self.title = title
        self.department = department

    def display_details(self):
        print("Name:", self.name)
        print("ID:", self.emp_id)
        print("Title:", self.title)
        print("Department:", self.department)

    def __str__(self):
        return f"{self.name} ({self.emp_id})"


class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)

    def list_employees(self):
        for employee in self.employees:
            print(employee)

    def __str__(self):
        return f"Department: {self.name}"


class Company:
    def __init__(self):
        self.departments = {}

    def add_department(self, department):
        self.departments[department.name] = department

    def remove_department(self, department_name):
        del self.departments[department_name]

    def display_departments(self):
        for department in self.departments.values():
            print(department)

    def save_data(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.departments, f, default=lambda x: x.__dict__)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for name, employees in data.items():
                department = Department(name)
                for emp_data in employees:
                    employee = Employee(**emp_data)
                    department.add_employee(employee)
                self.add_department(department)


def print_menu():
    print("Menu:")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. List Employees in Department")
    print("4. Add Department")
    print("5. Remove Department")
    print("6. List Departments")
    print("7. Save Data")
    print("8. Load Data")
    print("9. Exit")


def main():
    company = Company()
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter employee name: ")
            emp_id = input("Enter employee ID: ")
            title = input("Enter employee title: ")
            department = input("Enter department name: ")
            if department in company.departments:
                employee = Employee(name, emp_id, title, department)
                company.departments[department].add_employee(employee)
            else:
                print("Department not found!")

        elif choice == '2':
            department = input("Enter department name: ")
            if department in company.departments:
                company.departments[department].list_employees()
                emp_id = input("Enter employee ID to remove: ")
                for employee in company.departments[department].employees:
                    if employee.emp_id == emp_id:
                        company.departments[department].remove_employee(employee)
                        print("Employee removed successfully!")
                        break
                else:
                    print("Employee not found!")
            else:
                print("Department not found!")

        elif choice == '3':
            department = input("Enter department name: ")
            if department in company.departments:
                company.departments[department].list_employees()
            else:
                print("Department not found!")

        elif choice == '4':
            department_name = input("Enter department name: ")
            department = Department(department_name)
            company.add_department(department)
            print("Department added successfully!")

        elif choice == '5':
            department_name = input("Enter department name to remove: ")
            if department_name in company.departments:
                company.remove_department(department_name)
                print("Department removed successfully!")
            else:
                print("Department not found!")

        elif choice == '6':
            company.display_departments()

        elif choice == '7':
            filename = input("Enter filename to save: ")
            company.save_data(filename)
            print("Data saved successfully!")

        elif choice == '8':
            filename = input("Enter filename to load: ")
            company.load_data(filename)
            print("Data loaded successfully!")

        elif choice == '9':
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
