from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Patient, Patient_treatment_details
from django.contrib.auth import logout
from django.shortcuts import redirect
import os

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
        
        contact_no = contact_no.replace(' ', '')
        
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

        is_img_changed = True


        try:
            img = request.FILES['img']
        except:
            img = ''


        # select query

        pat = Patient.objects.raw(f"""SELECT * FROM public."Data_manager_patient"  WHERE id = '{ patient_id }'  """) 
        for i in pat:
            if name == '' or name == None:
                name = i.name
            
            if gender == '' or gender == None:
                gender = i.gender

            if dob == '' or dob == None:
                dob = i.dob

            if problem == '' or problem == None:
                problem = i.problem

            if medical_history == '' or medical_history == None:
                medical_history = i.medical_history

            if operation_history == '' or operation_history == None:
                operation_history = i.operation_history

            if other_details == '' or other_details == None:
                other_details = i.other_details

            if contact_no == '' or contact_no == None:
                contact_no = i.contact_no

            if name == '' or name == None:
                name = i.name
            
            if img == '' or img == None:
                img = i.img
                is_img_changed = False
        

        # change_query = f""" UPDATE public."Data_manager_patient" SET name='{name}', img='{img}', gender='{gender}', dob='{dob}', problem='{problem}', medical_history='{medical_history}',
        #                         operation_history='{operation_history}', other_details='{other_details}', contact_no='{contact_no}'  WHERE id={id} """
        # Patient.objects.raw(change_query, Patient.id)
        
        
        # if img=='':
        #     Patient.objects.filter(id=id).update(name=name,  gender=gender, dob=dob, problem=problem, medical_history=medical_history, operation_history=operation_history, other_details=other_details, contact_no=contact_no)
        # else:
        #     Patient.objects.filter(id=id).update(name=name, img=img, gender=gender, dob=dob, problem=problem, medical_history=medical_history, operation_history=operation_history, other_details=other_details, contact_no=contact_no)
        
        if is_img_changed:
            remove_patient_deletion_performer(request, True, False, patient_id)
        else:
            remove_patient_deletion_performer(request, False, False, patient_id)


        # Adding that same patient in database again

        patient = Patient(patient_id, name, img, gender, dob, problem, medical_history, operation_history, other_details, contact_no)

        patient.save()

    
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

        #  To return only most recent treatment 


        # part to return the total remaining amount of patient to be paid (in total)

        total_remaining_amt = 0

        for det in patient_all_treatment_details:
            total_remaining_amt += float(det.fees_remaining)

        
        print('total_remaining_amt  ================>>>> ', total_remaining_amt)
        


        ## --------------------------------------------------------------------------
        
    
        
        return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'dob': dob, 'total_remaining_amt':total_remaining_amt} )
    

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
        symptoms = request.POST['symptoms']

        treatment_given = request.POST['treatment_given']
        medicine_prescribed = request.POST['medicine_prescribed']

        fees_charged = request.POST['fees_charged']
        fees_paid = request.POST['fees_paid']
        
        fees_charged = float(fees_charged)
        fees_paid = float(fees_paid)

        fees_remaining = fees_charged - fees_paid


        next_checkup = request.POST['next_checkup']
        current_checkup_date = request.POST['current_checkup_date']

        remarks = request.POST['remarks']    
    
        # next_checkup = '2002-12-12'


      
        
        last_entry = Patient_treatment_details.objects.last()

        if last_entry is None:
            patient_treatment_details = Patient_treatment_details(1, patient_id, treatment_no, problem, symptoms, treatment_given, 
                                                                medicine_prescribed, fees_charged, fees_paid, fees_remaining, current_checkup_date, next_checkup, remarks)

        else:
            patient_treatment_details = Patient_treatment_details((last_entry.id + 1), patient_id, treatment_no , problem, symptoms, treatment_given, 
                                                                  medicine_prescribed, fees_charged, fees_paid, fees_remaining, current_checkup_date, next_checkup, remarks)
        

        try:
            patient_treatment_details.save()
        except:
            return patient_details(request)

        treatment_no = 1

    # patients = Patient.objects.all()
 
    # return render(request, 'patient_details.html', {'patients_list': patients})

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

    #  To return only most recent treatment 

    return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'dob': dob})
    

def remove_patient(request):

    patients = Patient.objects.all()

    return render(request, 'remove_patient.html', {'patients_list': patients})


def remove_patient_from_db(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id_in']

        
    return remove_patient_deletion_performer(request, True, True, patient_id)
    

def remove_patient_deletion_performer(request, delete_img, remove_record, patient_id):
    # if request.method == 'POST':
    #     patient_id = request.POST['patient_id_in']


    print('deletion is called...')

    pat = Patient.objects.raw(f"""SELECT * FROM public."Data_manager_patient"  WHERE id = '{ patient_id }'  """) 
    for i in pat:
        image_name = i.img


    if str(image_name) != '' and delete_img:

        image_name = str(image_name)
        image_name = "media/" + image_name
        if os.path.exists(image_name):
            os.remove(image_name)

        

        # Patient.objects._raw_delete(f"""DELETE FROM public."Data_manager_patient" WHERE id = { patient_id } """)
         

    Patient.objects.filter(id=patient_id).delete()

    if remove_record:
        Patient_treatment_details.objects.filter(patient_id=patient_id).delete()

        # Taking name of the img from database to delete the photo from the folder

    patients = Patient.objects.all()
    return render(request, 'remove_patient.html', {'patients_list': patients})


def change_treatment_details(request):
    if request.method == 'POST':
        patient_treatement_no = request.POST['treatment_no']
        patient_id = request.POST['patient_id_change_treatment']

        print('Patient_id --------------------->>>>> ', patient_id)

        patient_that_treatment_detail = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' AND n_th_treatment = '{patient_treatement_no}'; """)
        
        pk_for_treatment_detail = None
        detail = None
        for pat in patient_that_treatment_detail:
            detail = pat

        pk_for_treatment_detail = detail.id

        current_checkup_date = str(detail.current_checkup_date).replace(" ", "")
        next_checkup_date = str(detail.next_checkup_date).replace(" ", "")





#    return render(request, 'change_treatment_details.html', {'treatment_details'})
    return render(request, 'change_treatment_details.html', {'detail': detail, 'patient_id': patient_id, 'pk_for_treatment_detail': pk_for_treatment_detail, 'current_checkup_date': current_checkup_date, 'next_checkup_date': next_checkup_date})



# def change_treatment_details_in_db(request):
#     if request.method == "POST":
#         patientId = request.POST['patientId']
#         n_th_treatment = request.POST['n_th_treatment']
#         id = request.POST['pk_for_treatment_detail']

#         problem = request.POST['problem']
#         treatment_given = request.POST['treatment_given']
#         medicine_pres = request.POST['medicine_prescribed']
#         current_checkup_date = request.POST['current_checkup_date']
#         next_checkup_date = request.POST['next_checkup']

#         patient_that_treatment_detail = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patientId }' AND n_th_treatment = '{n_th_treatment}'; """)
                
#         detail = None
#         for pat in patient_that_treatment_detail:
#             detail = pat
#             break

#         if problem == '' or problem == None:
#             problem = detail.problem_detail

#         if treatment_given == '' or treatment_given == None:
#             treatment_given = detail.treatment_given

#         if medicine_pres == '' or medicine_pres == None:
#             medicine_pres = detail.medicine_prescribed

#         if current_checkup_date == '' or current_checkup_date == None:
#             current_checkup_date = detail.current_checkup_date

#         if next_checkup_date == '' or next_checkup_date == None:
#             next_checkup_date = detail.next_checkup_date

#         change_query = f""" UPDATE public."Patient_treatment_details" SET problem_detail='{problem}', treatment_given='{treatment_given}', medicine_prescribed='{medicine_pres}', 
#                             current_checkup_date='{current_checkup_date}, next_checkup_date='{next_checkup_date}' WHERE patient_id='{patientId}' AND n_th_treatment='{n_th_treatment}'; """

#         Patient_treatment_details.objects.raw(change_query, Patient_treatment_details.id)



#     patient_id = request.POST['patient_id_in']
        
     
#     patient = Patient.objects.get(pk=patient_id)

#     try:
#         patient_treatment_details = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' """)
#         patient_all_treatment_details = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' ORDER BY id DESC """)
#     except:
#         print('no table present')
    
    
#     treatment_no = 1

    
#     if patient_treatment_details is not None:
#         for details in patient_treatment_details:
                
#             if treatment_no < details.n_th_treatment:
#                 treatment_no = details.n_th_treatment
#             elif treatment_no == details.n_th_treatment:
#                 treatment_no = treatment_no + 1

#     dob = str(patient.dob).replace(" ", "")

#     #  To return only most recent treatment 

#     return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'dob': dob})


def change_treatment_details_in_db(request):
    global patient_id

    if request.method == "POST":
        pk = request.POST['pk_for_treatment_detail'] 
        # patient_id = str(request.POST.get('patientId', False)).replace(" ", '')
        n_th_treatment = request.POST['n_th_treatment']

        problem = request.POST['problem']
        symptoms = request.POST['symptoms']

        treatment_given = request.POST['treatment_given']
        medicine_prescribed = request.POST['medicine_prescribed']

        fees_charged = request.POST['fees_charged']
        fees_paid = request.POST['fees_paid']

        fees_charged = float(fees_charged)
        fees_paid = float(fees_paid)

        fees_remaining = fees_charged - fees_paid

        current_checkup_date = request.POST['current_checkup_date']
        next_checkup_date = request.POST['next_checkup_date']

        remarks = request.POST['remarks']

        try:
            Patient_treatment_details.objects.filter(id=pk).delete()

            treatment = Patient_treatment_details(pk, patient_id, n_th_treatment, problem, symptoms, treatment_given, medicine_prescribed, fees_charged, fees_paid, fees_remaining, current_checkup_date, next_checkup_date, remarks)

            treatment.save()


            messages.success(request, "Treament details have been changed")
        except:
            messages.success(request, "Couldn't change patient details!")

    

        
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

    #  To return only most recent treatment 

    return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'dob': dob})
