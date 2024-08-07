from django.db import models

# Create your models here.


class Patient(models.Model):
    #id auto
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='imgs', default=None)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    problem = models.TextField()
    medical_history = models.TextField()
    operation_history = models.TextField()
    other_details = models.TextField()
    contact_no = models.CharField(max_length=13, default="000000000000")




class Patient_treatment_details(models.Model):
    patient_id = models.CharField(max_length=11)
    n_th_treatment = models.IntegerField()
    problem_detail = models.TextField()
    treatment_given = models.TextField()
    medicine_prescribed = models.TextField()
    current_checkup_date = models.DateField()
    next_checkup_date = models.DateField() 
 
