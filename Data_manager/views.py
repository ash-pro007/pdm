from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Patient, Patient_treatment_details
from django.contrib.auth import logout
from django.shortcuts import redirect

user = ''

patient_id = 0
treatment_no = 1

def index(request):
    return render(request, 'index.html')


def signin(request):
    global user
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.username
            patients = Patient.objects.all()
            return render(request, 'home.html', {'fname': fname, 'patients_list': patients})
        else:
            messages.error(request, "Bad Credentials")
            return render(request, 'authenticate/signin.html')


    return render(request, 'authenticate/signin.html')


def signout(request):
    logout(request)
    return redirect('index')


def home(request):
    patients = Patient.objects.all()
    patients = patients.reverse
    return render(request, 'home.html', { 'patients_list': patients})


def home_lin(request):
    patients = Patient.objects.all()
    patients = patients.reverse

    return render(request, 'home.html', {'patients_list': patients})


def register_patient(request):
    global treatment_no
    if request.method == "POST":
        name = request.POST['name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        problem = request.POST['problem']
        medical_history = request.POST['medical_history']
        operation_history = request.POST['operation_history']
        other_details = request.POST['other_details']
        contact_no = request.POST['contact_no']
        
        try:
            img = request.FILES['img']
        except:
            img = ''

        if img is None:
            img = ''


        last_patient = Patient.objects.last()
        
        treatment_no = 1

        if last_patient is None: 
            patient = Patient(100000, name, img, gender, dob, problem, medical_history, operation_history, other_details, contact_no)
            
        else:
            last_patient.id = int(last_patient.id) + 1
            patient = Patient(last_patient.id, name, img, gender, dob, problem, medical_history, operation_history, other_details, contact_no)
            
        
        patient.save()
        patient = None
        messages.success(request, "Patient details have been saved")

    else:
        messages.error(request, "Couldn't save")
        
    patients = Patient.objects.all()
    return render(request, 'home.html', {'patients_list': patients})



def patient_details(request):
    global patient_id
    global treatment_no

    patient_all_treatment_details = None

    if request.method == "POST":
        patient_id = request.POST['patient_id_in']
        
     
        patient = Patient.objects.get(pk=patient_id)

        try:
            patient_treatment_details = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' """)
            patient_all_treatment_details = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' ORDER BY id DESC """)
        except:
            print('no table present')
        
        
        treatment_no = 1

        
        if patient_treatment_details is not None:
            for details in patient_treatment_details:
                   
                if treatment_no < details.n_th_treatment:
                    treatment_no = details.n_th_treatment
                elif treatment_no == details.n_th_treatment:
                    treatment_no = treatment_no + 1

        dob = str(patient.dob).replace(" ", "")
    
        
        return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'dob': dob})
    


def show_searched_patient(request):

    if request.method == 'POST':
        patient_name = request.POST['searched_name']

        patient_name = patient_name.lower()
        


        patients_found = None

        try:
    
            # # query = 'SELECT * FROM public."DataManager_patient" WHERE name LIKE \'' + patient_name + '%\''
            # query = "SELECT * FROM public.\"DataManager_patient\" WHERE name='Ayush Pawar'"

            # # query = "SELECT * FROM public.\"DataManager_patient\" WHERE name='Aeriell Debling'"

            # query = """SELECT * FROM public."DataManager_patient" WHERE name LIKE 'A%' or name LIKE 'a%' """

            patients_found = Patient.objects.all()

            list_of_matched_patient = []
            
            for i in patients_found:
                if(patient_name in i.name.lower()):
                    list_of_matched_patient.append(i) 
        except:
            print('no table present')

     
    # patients = Patient.objects.all()
    # return render(request, 'home.html', {'patients_list': patients})

    patients = Patient.objects.all()
    return render(request, 'home.html', {'patients_list': patients, 'list_of_matched_patient': list_of_matched_patient})


def show_searched_patient_for_remove_patient(request):

   

    if request.method == 'POST':
        patient_name = request.POST['searched_name']

        patient_name = patient_name.lower()
        

   

        patients_found = None

        try:
            # # query = 'SELECT * FROM public."DataManager_patient" WHERE name LIKE \'' + patient_name + '%\''
            # query = "SELECT * FROM public.\"DataManager_patient\" WHERE name='Ayush Pawar'"

            # # query = "SELECT * FROM public.\"DataManager_patient\" WHERE name='Aeriell Debling'"

            # query = """SELECT * FROM public."DataManager_patient" WHERE name LIKE 'A%' or name LIKE 'a%' """

            patients_found = Patient.objects.all()

            list_of_matched_patient = []
            
            for i in patients_found:
                if(patient_name in i.name.lower()):
                    list_of_matched_patient.append(i) 
        except:
            print('no table present')

     
    
    # patients = Patient.objects.all()
    # return render(request, 'home.html', {'patients_list': patients})

    patients = Patient.objects.all()
    return render(request, 'remove_patient.html', {'patients_list': patients, 'list_of_matched_patient': list_of_matched_patient})



def save_treatment_details(request):
    global patient_id
    global treatment_no


    if request.method == 'POST':
        problem = request.POST['problem']
        treatment_given = request.POST['treatment_given']
        medicine_prescribed = request.POST['medicine_prescribed']
        next_checkup = request.POST['next_checkup']
        current_checkup_date = request.POST['current_checkup_date']
        # next_checkup = '2002-12-12'

      
        
        last_entry = Patient_treatment_details.objects.last()

        if last_entry is None:
            patient_treatment_details = Patient_treatment_details(1, patient_id, treatment_no, problem, treatment_given, 
                                                                medicine_prescribed, current_checkup_date, next_checkup)

        else:
            patient_treatment_details = Patient_treatment_details((last_entry.id + 1), patient_id, treatment_no , problem, treatment_given, 
                                                                  medicine_prescribed, current_checkup_date, next_checkup)
        

        try:
            patient_treatment_details.save()
        except:
            return patient_details(request)

        treatment_no = 1

    patients = Patient.objects.all()
 
    return render(request, 'home.html', {'patients_list': patients})


def remove_patient(request):

    patients = Patient.objects.all()

    return render(request, 'remove_patient.html', {'patients_list': patients})


def remove_patient_from_db(request):

 

    if request.method == 'POST':
        patient_id = request.POST['patient_id_in']

  

        # Patient.objects._raw_delete(f"""DELETE FROM public."Data_manager_patient" WHERE id = { patient_id } """)
        # Patient_treatment_details.objects._raw_delete(f"""DELETE FROM public."Data_manager_patient_treatment_details" WHERE patient_id = { patient_id } """)

        Patient.objects.filter(id=patient_id).delete()
        Patient_treatment_details.objects.filter(patient_id=patient_id).delete()
        

    patients = Patient.objects.all()
    return render(request, 'remove_patient.html', {'patients_list': patients})


def change_patient_details(request):
    if request.method == "POST":
        id = request.POST['patient_id_to_change_data']
        name = request.POST['name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        problem = request.POST['problem']
        medical_history = request.POST['medical_history']
        operation_history = request.POST['operation_history']
        other_details = request.POST['other_details']
        contact_no = request.POST['contact_no']
        
        try:
            img = request.FILES['img']
        except:
            img = ''

        if img is None:
            img = ''

        # change_query = f""" UPDATE public."Data_manager_patient" SET name='{name}', img='{img}', gender='{gender}', dob='{dob}', problem='{problem}', medical_history='{medical_history}',
        #                         operation_history='{operation_history}', other_details='{other_details}', contact_no='{contact_no}'  WHERE id={id} """
        # Patient.objects.raw(change_query, Patient.id)
        
        
        Patient.objects.filter(id=id).update(name=name, img=img, gender=gender, dob=dob, problem=problem, medical_history=medical_history, operation_history=operation_history, other_details=other_details, contact_no=contact_no)
        
    
        messages.success(request, "Patient details have been changed")

    else:
        messages.error(request, "Couldn't change the details save")

    try:
        patient_all_treatment_details = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' ORDER BY id DESC """)
    except: 
        print('No table found!')
        
    patients = Patient.objects.all()
    patients = patients.reverse
    return render(request, 'home.html', { 'patients_list': patients})

     
