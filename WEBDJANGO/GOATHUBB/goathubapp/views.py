from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import FarmerRegistration, VetConsultation, SpecialCase, Veterinary, ConsultationReply
from .forms import FarmerRegistrationForm, VetConsultationForm, SpecialCaseForm, VeterinaryForm

def index(request):
    """Render the index page with the logged-in farmer's name."""
    farmer_name = None
    if 'farmer_id' in request.session:
        farmer = FarmerRegistration.objects.filter(registration_id=request.session['farmer_id']).first()
        if farmer:
            farmer_name = f"{farmer.first_name} {farmer.last_name}"
    return render(request, "index.html", {'farmer_name': farmer_name})

def index1(request):
    """Render the secondary index page."""
    return render(request, "index1.html")

def admin_hub(request):
    """Render the admin hub page."""
    return render(request, "adminHub.html")

def add_vet(request):
    """Handle adding a new veterinary entry."""
    form = VeterinaryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Veterinary added successfully!")
        return redirect('adminHub')
    return render(request, "add_vet.html", {'form': form})

def consult_a_vet(request):
    """Handle vet consultation requests."""
    form = VetConsultationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Your consultation request has been submitted successfully!")
        return redirect('index')
    return render(request, "consult_a_vet.html", {'form': form})

def education(request):
    """Render the education page."""
    return render(request, "education.html")

def login_view(request):
    """Handle farmer login."""
    if request.method == 'POST':
        farmer_id = request.POST.get('farmer_id')
        password = request.POST.get('password')

        if not farmer_id or not password:
            messages.error(request, 'Please provide both Farmer ID and password.')
        else:
            try:
                farmer = FarmerRegistration.objects.get(id_number=farmer_id)
                if farmer.check_password(password):
                    request.session['farmer_id'] = farmer.registration_id
                    messages.success(request, '')
                    return redirect('index')
                else:
                    messages.error(request, 'Invalid Farmer ID or password.')
            except FarmerRegistration.DoesNotExist:
                messages.error(request, 'Invalid Farmer ID or password.')

    return render(request, "login.html")

def register_farmer(request):
    """Handle farmer registration."""
    form = FarmerRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_farmer = form.save()
        messages.success(request, f"Registration successful! Welcome, {new_farmer.first_name} {new_farmer.last_name}.")
        return redirect('login')
    return render(request, 'register_farmer.html', {'form': form})

def special_cases(request):
    """Handle special case submissions."""
    form = SpecialCaseForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Special case submitted successfully!")
        return redirect('index')
    return render(request, "special_cases.html", {'form': form})

def vet_message(request):
    """Display messages related to veterinary consultations."""
    messages_list = []
    farmer_name = None

    if 'farmer_id' in request.session:
        farmer = FarmerRegistration.objects.filter(registration_id=request.session['farmer_id']).first()
        if farmer:
            farmer_name = f"{farmer.first_name} {farmer.last_name}"
            consultations = VetConsultation.objects.filter(farmer=farmer)
            messages_list = ConsultationReply.objects.filter(consultation__in=consultations)

    return render(request, "vet_message.html", {
        'messages': messages_list,
        'farmer_name': farmer_name,
        'farmer_id': request.session.get('farmer_id')
    })

def products(request):
    """Render the products page."""
    return render(request, 'products.html')

def farmer_list(request):
    """List all farmers with optional search functionality."""
    search_query = request.GET.get('search', '')
    farmers = FarmerRegistration.objects.filter(
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) |
        Q(id_number__icontains=search_query)
    )

    return render(request, 'farmer_list.html', {'farmers': farmers, 'search_query': search_query})

def cooperative_farmers(request):
    """Retrieve and display all farmers with the last name 'Cooperative', with optional search."""
    search_query = request.GET.get('search', '')
    
    if search_query:
        cooperative_farmers = FarmerRegistration.objects.filter(
            last_name__iexact='cooperative'
        ).filter(
            Q(first_name__icontains=search_query) |
            Q(id_number__icontains=search_query)
        )
    else:
        cooperative_farmers = FarmerRegistration.objects.filter(last_name__iexact='cooperative')

    return render(request, 'cooperative_farmers.html', {'farmers': cooperative_farmers, 'search_query': search_query})

def farmer_detail(request, farmer_id):
    """Display details for a specific farmer."""
    farmer = get_object_or_404(FarmerRegistration, pk=farmer_id)
    return render(request, 'farmer_detail.html', {'farmer': farmer})

def farmer_edit(request, farmer_id):
    """Edit a specific farmer's information inline."""
    farmer = get_object_or_404(FarmerRegistration, registration_id=farmer_id)

    if request.method == 'POST':
        farmer.first_name = request.POST.get('first_name', farmer.first_name)
        farmer.last_name = request.POST.get('last_name', farmer.last_name)
        farmer.phone_number = request.POST.get('phone_number', farmer.phone_number)
        farmer.district = request.POST.get('district', farmer.district)
        farmer.save()  # Save the updated farmer information
        messages.success(request, "Farmer updated successfully.")
        return redirect('farmer_list')

    return render(request, 'farmer_edit.html', {'farmer': farmer})  # Show the edit form

def farmer_delete(request, farmer_id):
    """Delete a specific farmer's record."""
    farmer = get_object_or_404(FarmerRegistration, pk=farmer_id)
    if request.method == 'POST':
        farmer.delete()
        messages.success(request, "Farmer deleted successfully.")
        return redirect('farmer_list')
    return render(request, 'farmer_confirm_delete.html', {'farmer': farmer})

def consultations(request):
    """List all veterinary consultations."""
    consultations = VetConsultation.objects.all()
    return render(request, 'consultations.html', {'consultations': consultations})


def veterinary_list(request):
    """List all veterinary entries with optional search functionality."""
    query = request.GET.get('search', '')
    veterinary_list = Veterinary.objects.filter(name__icontains=query) if query else Veterinary.objects.all()
    return render(request, 'veterinary_list.html', {'veterinary_list': veterinary_list})

def edit_veterinary(request, id):
    """Edit a specific veterinary entry."""
    veterinary = get_object_or_404(Veterinary, veterinary_id=id)
    form = VeterinaryForm(request.POST or None, instance=veterinary)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Veterinary updated successfully!")
            return redirect('veterinary_list')

    return render(request, 'edit_vet.html', {'form': form, 'veterinary': veterinary})

def delete_veterinary(request, id):
    """Delete a specific veterinary entry."""
    veterinary = get_object_or_404(Veterinary, veterinary_id=id)
    if request.method == 'POST':
        veterinary.delete()
        messages.success(request, "Veterinary deleted successfully!")
        return redirect('veterinary_list')
    return render(request, 'vet_confirm_delete.html', {'veterinary': veterinary})


from django.shortcuts import render
from .models import ConsultationReply

def all_replies(request):
    search_query = request.GET.get('search')
    searched_reply = None

    if search_query:
        searched_reply = ConsultationReply.objects.filter(farmer_name__icontains=search_query).first()

    context = {
        'searched_reply': searched_reply,
        'search_query': search_query,
    }

    return render(request, 'all_replies.html', context)

from django.shortcuts import redirect

def logout(request):
    """Logout the farmer by clearing the session."""
    if 'farmer_id' in request.session:
        del request.session['farmer_id']
    
    # Redirect to the login page after logout
    return redirect('login')




def reply_to_farmer(request):
    if request.method == 'POST':
        consultation_id = request.POST.get('consultation_id')
        reply_message = request.POST.get('reply_message')
        reply_image = request.FILES.get('reply_image')

        consultation = get_object_or_404(VetConsultation, pk=consultation_id)

        # Get the farmer's name from the form
        farmer_name = request.POST.get('farmer_name', 'Veterinary Staff')  # Default name if not provided

        reply = ConsultationReply(
            consultation=consultation,
            reply_message=reply_message,
            reply_image=reply_image,
            farmer_name=farmer_name  # Set the farmer's name
        )
        reply.save()

        messages.success(request, "Reply sent successfully!")
        return redirect('consultations')

    messages.error(request, "Invalid request.")
    return redirect('consultations')




