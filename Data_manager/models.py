from django.db import models # type: ignore

# Create your models here.


class Patient(models.Model):
    #id auto
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='imgs', default=None)
    gender = models.CharField(max_length=1)
    age = models.SmallIntegerField()
    problem = models.TextField()
    medical_history = models.TextField()
    operation_history = models.TextField()
    other_details = models.TextField()
    contact_no = models.CharField(max_length=13, default="000000000000")
    profile_created_on_or_first_diagnos = models.DateField()
    address = models.TextField()


class Patient_treatment_details(models.Model):
    patient_id = models.CharField(max_length=11)
    n_th_treatment = models.IntegerField()
    
    problem_detail = models.TextField()
    symptoms = models.TextField()

    blood_pressure = models.CharField(max_length=4)
    oxygen = models.CharField(max_length=4)
    pulse = models.CharField(max_length=4)
    sugar = models.CharField(max_length=4)
    weigth = models.CharField(max_length=4)

    vitals_extra = models.TextField()

    treatment_given = models.TextField()
    medicine_prescribed = models.TextField()

    fees_charged = models.DecimalField(decimal_places=2, max_digits=10)
    fees_paid = models.DecimalField(decimal_places=2, max_digits=10)
    fees_remaining = models.DecimalField(decimal_places=2, max_digits=10)      ## auto -> fee_remaining = fees_charged - fees_paid
    
    current_checkup_date = models.DateField()
    next_checkup_date = models.DateField() 

    remarks = models.TextField()                # new


class Patient_treatment_images(models.Model):
    #id
    patient_id = models.CharField(max_length=11)
    treatment_id = models.CharField(max_length=12)
    trt_img = models.ImageField(upload_to='treatment_images')

