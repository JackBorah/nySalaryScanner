from bs4 import BeautifulSoup
from dataclasses import asdict, dataclass
import csv

@dataclass
class Employee:
    name: str
    employer: str
    total_pay: int
    subagency: str
    title: str
    rate_of_pay: int
    pay_year: str
    pay_basis: str
    major_category: str

def convert_dollars_to_int(dollars: str):
    return int(dollars.replace('$', '').replace(',', ''))


def parse(fileName: str, output_csv: str = "salaries.csv"):
    employees = []

    with open(fileName) as f:
        soup = BeautifulSoup(f, 'html.parser')
        data = soup.find_all('tr')[1:]
        for i in range(0, len(data), 2):
            cells = data[i].find_all("td")
            additional_cells = data[i+1].find_all(class_="col-xs-6")

            employees.append(Employee(
                cells[1].get_text(),
                cells[2].get_text(),
                convert_dollars_to_int(cells[3].get_text()),
                cells[4].get_text(),
                additional_cells[1].get_text(),
                convert_dollars_to_int(additional_cells[2].get_text()),
                additional_cells[3].get_text(),
                additional_cells[4].get_text(),
                additional_cells[5].get_text(),
            ))

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=Employee.__dataclass_fields__.keys()
        )

        writer.writeheader()

        for emp in employees:
            writer.writerow(asdict(emp))