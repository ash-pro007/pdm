from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib import messages # type: ignore
from .models import Patient, Patient_treatment_details, Patient_treatment_images # type: ignore
from django.contrib.auth import logout # type: ignore
from django.shortcuts import redirect # type: ignore

from django.db import connection # type: ignore


import base64
import uuid 
from django.core.files.base import ContentFile # type: ignore
from django.shortcuts import render, redirect # type: ignore



import os

user = ''

patient_id = 0
treatment_no = 1


def reverse_date(date_str):
    """Reverses a date from YYYY-MM-DD to DD-MM-YYYY format."""

    year, month, day = date_str.split('-')
    return f"{day}-{month}-{year}"


def is_date_greater(date1, date2):
    return date1 < date2


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
    # try:
    if request.method == "POST":
        name = str(request.POST['name'])
        gender = str(request.POST['gender'])
        age = str(request.POST['age'])
        problem = str(request.POST['problem'])
        medical_history = str(request.POST['medical_history'])
        operation_history = str(request.POST['operation_history'])
        other_details = str(request.POST['other_details'])
        contact_no = str(request.POST['contact_no'])
        profile_created_on_or_first_diagnos = str(request.POST['profile_created_on_or_first_diagnos'])
        address = str(request.POST['address'])
        

        name = name.strip()
        gender = gender.strip()
        age = age.strip()
        problem = problem.strip()
        medical_history = medical_history.strip()
        operation_history = operation_history.strip()
        other_details = other_details.strip()

        contact_no = contact_no.replace(' ', '')
        contact_no = contact_no.strip()
        address = address.strip()


        if name == '' or name == ' ' or name == None:
            name = 'Unknown'

        if gender == '' or gender == ' ' or gender == None:
            gender = 'o'
        
        if age == '' or age == ' ' or age == None:
            age = 0

        if medical_history == '' or medical_history == ' ' or medical_history == None:
            medical_history = 'NA'

        if operation_history == '' or operation_history == ' ' or operation_history == None:
            operation_history = 'NA'

        if other_details == '' or other_details == ' ' or other_details == None:
            other_details = 'NA'

        if contact_no == '' or contact_no == ' ' or contact_no == None:
            contact_no = '0000000000'

        if profile_created_on_or_first_diagnos == '' or profile_created_on_or_first_diagnos == None:
            profile_created_on_or_first_diagnos = 'NA'

        if address == '' or address == None:
            address = 'NA'
        



        last_patient = Patient.objects.last()
        
        treatment_no = 1

        image_data = ''
        try:
            #img = request.FILES['img']
            cropped_image_data = request.POST.get('cropped_image')
            if cropped_image_data:
                # Decode the base64 image data
                format, imgstr = cropped_image_data.split(';base64,') 
                ext = format.split('/')[-1]

                unique_filename = f'patient_image_{uuid.uuid4()}.{ext}'
                image_data = ContentFile(base64.b64decode(imgstr),  name=unique_filename)
            
                
        except:
            image_data = ''
            messages.error(request, "Image error....!")

        # if img is None:
        #     img = ''

        if image_data == None:
            image_data = ''
        

        if last_patient is None: 
            patient = Patient(100000, name, image_data, gender, age, problem, medical_history, operation_history, other_details, contact_no, profile_created_on_or_first_diagnos, address)
            
        else:
            last_patient.id = int(last_patient.id) + 1
            patient = Patient(last_patient.id, name, image_data, gender, age, problem, medical_history, operation_history, other_details, contact_no, profile_created_on_or_first_diagnos, address)
            
        
        patient.save()
        patient = None
        messages.success(request, "Patient details have been saved")

    else:
        messages.error(request, "Couldn't save")

    # except:
    #     messages.error(request, "Couldn't create patient profile! Please check given field data.")
        
    patients = Patient.objects.all()
    return render(request, 'home.html', {'patients_list': patients})


def change_patient_details(request):
    try:
        if request.method == "POST":
            id = str(request.POST['patient_id_to_change_data'])

            name = str(request.POST['name'])
            gender = str(request.POST['gender'])
            age = str(request.POST['age'])
            profile_created_on_or_first_diagnos = str(request.POST['profile_created_on_or_first_diagnos'])
            problem = str(request.POST['problem'])
            medical_history = str(request.POST['medical_history'])
            operation_history = str(request.POST['operation_history'])
            other_details = str(request.POST['other_details'])
            contact_no = str(request.POST['contact_no'])
            address = str(request.POST['address'])

            is_img_changed = True

            # try:
            #     img = request.FILES['img']
            # except:
            #     img = ''


            # select query


            image_data = ''
            try:
                #img = request.FILES['img']
                cropped_image_data = request.POST.get('cropped_image')
                if cropped_image_data:
                    # Decode the base64 image data
                    format, imgstr = cropped_image_data.split(';base64,') 
                    ext = format.split('/')[-1]

                    unique_filename = f'patient_image_{uuid.uuid4()}.{ext}'
                    image_data = ContentFile(base64.b64decode(imgstr),  name=unique_filename)
                
                    
            except:
                image_data = ''
                messages.error(request, "Image error....!")

            pat = Patient.objects.raw(f"""SELECT * FROM public."Data_manager_patient"  WHERE id = '{ patient_id }'  """) 
            for i in pat:
                if name == '' or name == None:
                    name = i.name
                
                if gender == '' or gender == None:
                    gender = i.gender

                if age == '' or age == None:
                    age = i.age

                if profile_created_on_or_first_diagnos == '' or gender == None:
                    profile_created_on_or_first_diagnos = '2024-01-01'

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
                
                if image_data == '' or image_data == None:
                    image_data = i.img
                    is_img_changed = False

                if address == '' or address == None:
                    address = i.address
            

                # change_query = f""" UPDATE public."Data_manager_patient" SET name='{name}', img='{img}', gender='{gender}', age='{age}', problem='{problem}', medical_history='{medical_history}',
                #                         operation_history='{operation_history}', other_details='{other_details}', contact_no='{contact_no}'  WHERE id={id} """
                # Patient.objects.raw(change_query, Patient.id)
                
                
                # if img=='':
                #     Patient.objects.filter(id=id).update(name=name,  gender=gender, age=age, problem=problem, medical_history=medical_history, operation_history=operation_history, other_details=other_details, contact_no=contact_no)
                # else:
                #     Patient.objects.filter(id=id).update(name=name, img=img, gender=gender, age=age, problem=problem, medical_history=medical_history, operation_history=operation_history, other_details=other_details, contact_no=contact_no)
                
            


            
            if is_img_changed:
                remove_patient_deletion_performer(request, True, False, patient_id)
            else:
                remove_patient_deletion_performer(request, False, False, patient_id)


            # Adding that same patient in database again
            patient = Patient(patient_id, name, image_data, gender, age, problem, medical_history, operation_history, other_details, contact_no, profile_created_on_or_first_diagnos, address)



            patient.save()

        
            messages.success(request, "Patient details have been changed")

        else:
            messages.error(request, "Couldn't change the details save")

    except:
        messages.error(request, "Couldn't change the patient details. There must be some problem with the given input.")

        # except:
        #     messages.error(request, "Couldn't change patient details")

    try:
        patient_all_treatment_details = Patient_treatment_details.objects.raw(f"""SELECT * FROM public."Data_manager_patient_treatment_details" WHERE patient_id = '{ patient_id }' ORDER BY id DESC """)
    except: 
        print('No table found!')
        
    patients = Patient.objects.all()
    patients.reverse()
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

        profile_created_on_or_first_diagnos = str(patient.profile_created_on_or_first_diagnos).strip()

        #  To return only most recent treatment 


        # part to return the total remaining amount of patient to be paid (in total)

        total_remaining_amt = 0

        for det in patient_all_treatment_details:
            total_remaining_amt += float(det.fees_remaining)

        


        ## --------------------------------------------------------------------------
        
        ## Returning images lst of all treatment 

        ### list inside list

        img_list_of_patient = []

        cursor = connection.cursor()
        cursor.execute(f''' SELECT * FROM public."Data_manager_patient_treatment_images" WHERE patient_id='{patient_id}'; ''')
        img_list_of_patient = cursor.fetchall()
        
    
        t_lst = []

        print(':::::::::::::::::::::::::::::::::::::::::::::::::::::\n\n')
        print('img_list_of_patinet ---------------------------------')
            
        for i in img_list_of_patient:
            img_obj = Patient_treatment_images(i[0], i[1], i[2], i[3])
            t_lst.append(img_obj)


        for i in t_lst:
            print(i)

        print(':::::::::::::::::::::::::::::::::::::::::::::::::::::')


        img_list_of_patient = t_lst


        
        return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 
                                                        'patient_all_treatment_details': patient_all_treatment_details,
                                                        'profile_created_on_or_first_diagnos': profile_created_on_or_first_diagnos,
                                                        'total_remaining_amt':total_remaining_amt, 'img_list_of_patient': img_list_of_patient},)
    

def show_searched_patient(request):
    list_of_matched_patient = []
    patient_name = ""
    try:
        if request.method == 'POST':
            patient_name = request.POST['searched_name']
            actul_input = patient_name
            if patient_name == None or patient_name == '':
                messages.error(request,'Please enter a vaild patient name to search!')
            else:
                patient_name = patient_name.lower()
        
                patients_found = None

                try:
            
                    # # query = 'SELECT * FROM public."DataManager_patient" WHERE name LIKE \'' + patient_name + '%\''
                    # query = "SELECT * FROM public.\"DataManager_patient\" WHERE name='Ayush Pawar'"

                    # # query = "SELECT * FROM public.\"DataManager_patient\" WHERE name='Aeriell Debling'"

                    # query = """SELECT * FROM public."DataManager_patient" WHERE name LIKE 'A%' or name LIKE 'a%' """

                    patients_found = Patient.objects.all()
 
                    
                    for i in patients_found:
                        if(patient_name in i.name.lower()):
                            list_of_matched_patient.append(i) 
                    if(len(list_of_matched_patient) <= 0):
                        mess = 'No patient found with by name: ' + actul_input
                        messages.error(request, mess)
                except:
                    print('no table present')
            

    except:
        messages.error(request,'Something went wront with enter input!')

     
    # patients = Patient.objects.all()
    # return render(request, 'home.html', {'patients_list': patients})

    patients = Patient.objects.all()



    return render(request, 'home.html', {'patients_list': patients, 'list_of_matched_patient': list_of_matched_patient})


def show_searched_patient_by_date_range(request):
    matched_patients_object = []
    if request.method == 'POST':
        try:
            date_from = str(request.POST['input-form-search-by-date-from'])
            date_to = str(request.POST['input-form-search-by-date-to'])

          
            if(is_date_greater(date_from, date_to) or date_from == date_to):
                try:
                    cursor = connection.cursor()
                    cursor.execute(f''' SELECT * FROM public."Data_manager_patient_treatment_details" WHERE current_checkup_date BETWEEN '{date_from}' AND '{date_to}'; ''')
                    row = cursor.fetchall()

                    patient_id_lst = []

                    for i in row:
                        patient_id_lst.append(i[1])

                    
                    all_patients = Patient.objects.all()


                    matched_patients_object = []
                    for i in all_patients:
                        if str(i.id) in patient_id_lst:
                            matched_patients_object.append(i)

                    if(len(matched_patients_object) <= 0):
                        mess1 = 'There is no patient who visited from ' + reverse_date(date_from) + ' to ' + reverse_date(date_to)
                        messages.error(request, mess1)
                        
                except:
                    print('no table present')
                    messages.error(request,"Couldn't search patient for the entered date. Please enter vaild dates and try again!")

            else:
                messages.error(request, "Invaild searched date input. Date1 must be smaller than Date2")
                
            
        except:
            messages.error(request,"Couldn't search patient for the entered date.Please enter vaild dates and try again!")
   
            
    patients = Patient.objects.all()

    

    return render(request, 'home.html', {'patients_list': patients, 'list_of_matched_patient': matched_patients_object})


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
        problem = str(request.POST['problem'])
        symptoms = str(request.POST['symptoms'])

        blood_pressure = str(request.POST['blood_pressure'])
        oxygen = str(request.POST['oxygen'])
        pulse = str(request.POST['pulse'])
        sugar = str(request.POST['sugar'])
        weigth = str(request.POST['weight'])

        vitals_extra = str(request.POST['vital_extra'])
        

        treatment_given = str(request.POST['treatment_given'])
        medicine_prescribed = str(request.POST['medicine_prescribed'])

        fees_charged = str(request.POST['fees_charged'])
        fees_paid = str(request.POST['fees_paid'])
        

        next_checkup = str(request.POST['next_checkup'])
        current_checkup_date = str(request.POST['current_checkup_date'])

        remarks = str(request.POST['remarks'])

        # -----------------------------------------------------

        images_ = request.FILES.getlist('images') 

        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

    


        # next_checkup = '2002-12-12'

        # type-checking for the inputs 

        problem = problem.strip()
        symptoms = symptoms.strip()
        treatment_given = treatment_given.strip()
        medicine_prescribed = medicine_prescribed.strip()
        remarks = remarks.strip()

        # adding double check

        if problem == '' or problem == None:
            problem = 'NA'

        if symptoms == '' or symptoms == None:
            symptoms = 'NA'

        if blood_pressure == None:
            blood_pressure = ''
        
        if oxygen == None:
            oxygen = ''

        if sugar == None:
            sugar = ''

        if pulse == None:
            pulse = ''
        
        if weigth == None:
            weigth = ''

        if vitals_extra == None or vitals_extra == '':
            vitals_extra = 'NA'

        if treatment_given == '' or treatment_given == None:
            treatment_given = 'NA'

        if medicine_prescribed == '' or medicine_prescribed == None:
            medicine_prescribed = 'NA'

        if fees_charged == '' or fees_charged == ' ' or fees_charged == None:
            fees_charged = 0.0

        if fees_paid == '' or fees_paid == ' ' or fees_paid == None:
            fees_paid = 0.0

        if current_checkup_date == '' or next_checkup == None or current_checkup_date == ' ':
            current_checkup_date = '1111-11-11'

        if next_checkup == '' or next_checkup == ' ':
            next_checkup = '1111-11-11'

        if remarks == '' or remarks == None:
            remarks = 'remarks'

        fees_charged = float(fees_charged)
        fees_paid = float(fees_paid)
      
        fees_remaining = fees_charged - fees_paid
        
        last_entry = Patient_treatment_details.objects.last()


        treatment_id = None

        if last_entry is None:
            patient_treatment_details = Patient_treatment_details(id=1, patient_id=patient_id, n_th_treatment=treatment_no, problem_detail=problem, 
                                                                  symptoms=symptoms, treatment_given=treatment_given,
                                                                medicine_prescribed=medicine_prescribed, fees_charged=fees_charged, fees_paid=fees_paid, 
                                                                fees_remaining=fees_remaining, current_checkup_date=current_checkup_date, 
                                                                next_checkup_date=next_checkup, remarks=remarks, blood_pressure=blood_pressure,
                                                                 oxygen=oxygen, pulse=pulse, vitals_extra=vitals_extra, weigth=weigth, sugar=sugar)
            treatment_id = 1

        else:
            patient_treatment_details = Patient_treatment_details((last_entry.id + 1), patient_id=patient_id, n_th_treatment=treatment_no, problem_detail=problem, 
                                                                  symptoms=symptoms, treatment_given=treatment_given,
                                                                medicine_prescribed=medicine_prescribed, fees_charged=fees_charged, fees_paid=fees_paid, 
                                                                fees_remaining=fees_remaining, current_checkup_date=current_checkup_date, 
                                                                next_checkup_date=next_checkup, remarks=remarks, blood_pressure=blood_pressure,
                                                                 oxygen=oxygen, pulse=pulse, vitals_extra=vitals_extra, weigth=weigth, sugar=sugar)
            
            treatment_id = last_entry.id + 1
            
        

        # print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        # print(patient_treatment_details)

        # print("patient_treatment_details.id = ",  patient_treatment_details.id)
        # print("patient_treatment_details.patientID = ", patient_treatment_details.patient_id)
        # print("patient_treatment_details.n_th_treatment = ", patient_treatment_details.n_th_treatment)
        # print("patient_treatment_details.problem_treatment = ", patient_treatment_details.problem_detail)
        # print("patient_treatment_details.symptoms = ", patient_treatment_details.symptoms)
        # print("patient_treatment_details.treatment_given = ", patient_treatment_details.treatment_given)
        # print("patient_treatment_details.medicine_prescribed = ", patient_treatment_details.medicine_prescribed)
        # print("patient_treatment_details.fees_charged = ", patient_treatment_details.fees_charged)
        # print("patient_treatment_details.fees_paid", patient_treatment_details.fees_paid)
        # print("patient_treatment_details.fee_remaining = ", patient_treatment_details.fees_remaining)
        # print("patient_treatment_details.current_checkup_date = ", patient_treatment_details.current_checkup_date)
        # print("patient_treatment_details.next_checkup = ", patient_treatment_details.next_checkup_date)
        # print("patient_treatment_details.remarks = ", patient_treatment_details.remarks)
        # print("patient_treatment_details.blood_pressure = ", patient_treatment_details.blood_pressure)
        # print("patient_treatment_details.pulse = ", patient_treatment_details.pulse)
        # print("patient_treatment_details.vital_extra = ", patient_treatment_details.vitals_extra)
        # print("patient_treatment_details.weight = ", patient_treatment_details.weigth)
        # print("patient_treatment_details.sugar = ", patient_treatment_details.sugar)
    

        # print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        

        
        try:
            print('patient id in save_treatment() ==---------------->> ', patient_id)
            patient_treatment_details.save()


            print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

            print('images = ', images_)

            for i in images_:
                print("i = ", i, " || type(i) = ", type(i))

            last_img_obj = Patient_treatment_images.objects.last()

            if images_ is not None:
                for imgg in images_:
                    if last_img_obj is None:
                        treatment_image_table_obj = Patient_treatment_images(1, patient_id, treatment_id, imgg)
                        last_img_obj = Patient_treatment_images.objects.last()
                    else:
                        treatment_image_table_obj = Patient_treatment_images((last_img_obj.id + 1), patient_id, treatment_id, imgg)
                        last_img_obj = Patient_treatment_images.objects.last()
                    
                    treatment_image_table_obj.save()

            print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


        except:
            messages.success(request, "Couldn't add treatment details!")
            return home(request)
        
        

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

    age = str(patient.age).replace(" ", "")

    #  To return only most recent treatment 

    return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'age': age})
    

def remove_patient(request):

    patients = Patient.objects.all()

    return render(request, 'remove_patient.html', {'patients_list': patients})


def remove_patient_from_db(request):
    if request.method == 'POST':
        patient_id = str(request.POST['patient_id_in'])

        patient_id = patient_id.strip()
        
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


def change_treatment_details_in_db(request):
    global patient_id

    if request.method == "POST":
        pk = str(request.POST['pk_for_treatment_detail'] )


        print('type of pk => ', type(pk))

        # patient_id = str(request.POST.get('patientId', False)).replace(" ", '')
        n_th_treatment = str(request.POST['n_th_treatment'])

        problem = str(request.POST['problem'])
        symptoms = str(request.POST['symptoms'])

        treatment_given = str(request.POST['treatment_given'])
        medicine_prescribed = str(request.POST['medicine_prescribed'])

        fees_charged = str(request.POST['fees_charged'])
        fees_paid = str(request.POST['fees_paid'])

        print('type of fee_charged => ', type(fees_charged))

        current_checkup_date = str(request.POST['current_checkup_date'])
        next_checkup_date = str(request.POST['next_checkup_date'])

        remarks = str(request.POST['remarks'])



        pk = pk.strip()
        n_th_treatment = n_th_treatment.strip()

        problem = problem.strip()
        symptoms = symptoms.strip()

        treatment_given = treatment_given.strip()
        medicine_prescribed = medicine_prescribed.strip()

        fees_charged = fees_charged.strip()
        fees_paid = fees_paid.strip()

        current_checkup_date = current_checkup_date.strip()
        next_checkup_date = next_checkup_date.strip()

        remarks = remarks.strip()


        if pk == '' or pk ==' ' or pk == None:
            pk = 'NA'

        if n_th_treatment == '' or n_th_treatment ==' ' or n_th_treatment == None:
            n_th_treatment = 'NA'  

        if problem == '' or problem ==' ' or problem == None:
            problem = 'NA'

        if symptoms == '' or symptoms ==' ' or symptoms == None:
            symptoms = 'NA'
        
        if treatment_given == '' or treatment_given ==' ' or treatment_given == None:
            treatment_given = 'NA'


        if medicine_prescribed == '' or medicine_prescribed ==' ' or medicine_prescribed == None:
            medicine_prescribed = 'NA'

        if fees_charged == '' or fees_charged ==' ' or fees_charged == None:
            fees_charged = 'NA'

        if fees_paid == '' or fees_paid ==' ' or fees_paid == None:
            fees_paid = 'NA'

        if current_checkup_date == '' or current_checkup_date ==' ' or current_checkup_date == None:
            current_checkup_date = 'NA'

        if next_checkup_date == '' or next_checkup_date ==' ' or next_checkup_date == None:
            next_checkup_date = 'NA'

        if remarks == '' or remarks ==' ' or remarks == None:
            remarks = 'NA'
        


        fees_charged = float(fees_charged)
        fees_paid = float(fees_paid)

        fees_remaining = fees_charged - fees_paid

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

    age = str(patient.age).replace(" ", "")

    #  To return only most recent treatment 

    return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'age': age})



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

#     age = str(patient.age).replace(" ", "")

#     #  To return only most recent treatment 

#     return render(request, 'patient_details.html', {'patient': patient, 'treatment_no': treatment_no, 'patient_all_treatment_details': patient_all_treatment_details, 'age': age})

