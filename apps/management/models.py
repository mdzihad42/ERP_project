from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country.name})"

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class UnitNumber(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='units')
    unit_no = models.CharField(max_length=50, unique=True) # e.g. Dhaka-01
    description = models.TextField(blank=True)

    def __str__(self):
        return self.unit_no

class Department(models.Model):
    # Departments are city/unit based as requested for Super Admin creation
    unit = models.ForeignKey(UnitNumber, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.unit.unit_no}"

class Position(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"
