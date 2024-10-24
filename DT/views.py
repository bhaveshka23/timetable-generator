import  random
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import SavedTimetable
from django.contrib import messages

@login_required
def lecture(request):
    if request.method == "POST":
        batch = request.POST.get('batch')
        lecture_names = request.POST.getlist('lectureName[]')
        lecture_counts = request.POST.getlist('lectureCount[]')
        practical_names = request.POST.getlist('practicalName[]')
        practical_counts = request.POST.getlist('practicalCount[]')

        lecture_data = [
            (name, int(count)) for name, count in zip(lecture_names, lecture_counts)
            if name and count.isdigit() and int(count) > 0
        ]
 
        practical_data = [
            (name, int(count)) for name, count in zip(practical_names, practical_counts)
            if name and count.isdigit() and int(count) > 0
        ]

        lectures_data = {
            "lecture_names": [name for name, _ in lecture_data],
            "lecture_counts": [count for _, count in lecture_data],
            "practical_names": [name for name, _ in practical_data],
            "practical_counts": [count for _, count in practical_data],
            "batch": batch
        }

        return table(request, lectures_data)

    return render(request, "lectures.html")

@login_required
def table(request, lectures_data):
    
    lecture_names = lectures_data['lecture_names']
    lecture_counts = lectures_data['lecture_counts']
    practical_names = lectures_data['practical_names']
    practical_counts = lectures_data['practical_counts']
    batch = lectures_data['batch']

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]  # Added Saturday back

    
    timetable = {day: [""] * 6 for day in days} 

   
    practical_slots = [2, 3]
    

    practical_index = 0
    for day in days:
        if practical_index < len(practical_names):  
            for slot in practical_slots:
                timetable[day][slot] = practical_names[practical_index]  
            
            practical_counts[practical_index] -= 1
            
            if practical_counts[practical_index] == 0:
                practical_index += 1

   
    morning_slots = [0, 1]  
    afternoon_slots = [4, 5] 

    
    all_lectures = []
    for i, name in enumerate(lecture_names):
        all_lectures.extend([name] * lecture_counts[i])

    
    random.shuffle(all_lectures)

    
    for day in days[:-1]: 
        assigned_subjects = set() 
        for slot in morning_slots:
            if all_lectures:  
                for lecture in all_lectures:
                    if lecture.split()[0] not in assigned_subjects:
                        timetable[day][slot] = lecture
                        assigned_subjects.add(lecture.split()[0])  
                        all_lectures.remove(lecture) 
                        break  

    
    for day in days[:-1]: 
        assigned_subjects_morning = set()  
        for slot in morning_slots:
            assigned_subjects_morning.add(timetable[day][slot].split()[0]) 
        
        assigned_subjects_afternoon = set()  
        for slot in afternoon_slots:
            if all_lectures:  
                for lecture in all_lectures:
                    if lecture.split()[0] not in assigned_subjects_morning and lecture.split()[0] not in assigned_subjects_afternoon:
                        timetable[day][slot] = lecture
                        assigned_subjects_afternoon.add(lecture.split()[0]) 
                        all_lectures.remove(lecture)  
                        break  


    timetable_list = [(day, timetable[day]) for day in days]


    if (batch=='Afternoon'):
        context = {
            "timetable": timetable_list,
            "time_slots": ["10.25-11.20", "11.20-12.15", "1.05-2.00", "2.00-2.55", "3.05-4.00", "4.00-4.55"],
            "batch": batch 
        } 
    else :
        context = {
            "timetable": timetable_list,
            "time_slots": ["8.10-9.10", "9.10-10.10", "10.25-11.20", "11.20-12.15", "01.05-02.00", "02.00-02.55"],
            "batch": batch 
        } 
    
    return render(request, "table.html", context)


def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,username=email,password=password)
        if user is not None:
           auth_login(request,user)
           return redirect('homepage')
        else :
            return HttpResponse("email or password is incorrect or create the account first")

    return render(request, "login.html")
def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            return HttpResponse("Your does not match")
        else:
            user=User.objects.create_user(email,pass1,pass2)
            user.save()
            return redirect('login')        

    return render(request, "signup.html")

@login_required
def homepage(request):
    return render(request, "homepage.html")
@login_required
def logout_page(request):
    logout(request)
    return redirect('landingpage')
def landingpage(request):
    return render(request, "landingpage.html")

# views.py


@login_required
def save_timetable(request):
    if request.method == "POST":
        try:
            # Get the raw timetable data from the form
            timetable_str = request.POST.get('timetable_data')
            batch = request.POST.get('batch')
            name = request.POST.get('timetable_name')
            
            # Convert string representation of list to actual list
            import ast
            timetable_data = ast.literal_eval(timetable_str)
            
            # Create the SavedTimetable object
            SavedTimetable.objects.create(
                user=request.user,
                name=name,
                batch=batch,
                timetable_data=timetable_data
            )
            
            messages.success(request, "Timetable saved successfully!")
            return redirect('saved_timetables')
        except Exception as e:
            messages.error(request, f"Error saving timetable: {str(e)}")
            return redirect('table')
    
    return redirect('homepage')

@login_required
def saved_timetables(request):
    timetables = SavedTimetable.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "saved_timetables.html", {"timetables": timetables})

@login_required
@login_required
def view_saved_timetable(request, timetable_id):
    timetable = get_object_or_404(SavedTimetable, id=timetable_id, user=request.user)
    
    # Format the timetable data for the template
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    # Ensure timetable data is in the correct format
    if isinstance(timetable.timetable_data, str):
        import ast
        timetable_data = ast.literal_eval(timetable.timetable_data)
    else:
        timetable_data = timetable.timetable_data
        
    # Convert timetable data to the format expected by the template
    formatted_timetable = []
    for day in days:
        day_slots = next((slots for d, slots in timetable_data if d == day), [""] * 6)
        formatted_timetable.append((day, day_slots))
    
    # Get appropriate time slots based on batch
    if timetable.batch == 'Afternoon':
        time_slots = ["10.25-11.20", "11.20-12.15", "1.05-2.00", "2.00-2.55", "3.05-4.00", "4.00-4.55"]
    else:
        time_slots = ["8.10-9.10", "9.10-10.10", "10.25-11.20", "11.20-12.15", "01.05-02.00", "02.00-02.55"]
    
    context = {
        "timetable": formatted_timetable,
        "time_slots": time_slots,
        "batch": timetable.batch,
        "name": timetable.name
    }
    return render(request, "view_saved_timetable.html", context)

