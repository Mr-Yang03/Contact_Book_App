from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Contact

def home(request):
    """Display all contacts"""
    contacts = Contact.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')

    if search_query:
        contacts = contacts.filter(
            first_name__icontains=search_query
        ) | contacts.filter(
            last_name__icontains=search_query
        ) | contacts.filter(
            phone_number__icontains=search_query
        )

    return render(request, 'index.html', {
        'contacts': contacts,
        'search_query': search_query
    })

def create_contact(request):
    """Create a new contact"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        birthday = request.POST.get('birthday')

        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email if email else None,
            address=address,
            birthday=birthday if birthday else None
        )
        return redirect('home')

    return redirect('home')

def update_contact(request, contact_id):
    """Update an existing contact"""
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.first_name = request.POST.get('first_name')
        contact.last_name = request.POST.get('last_name')
        contact.phone_number = request.POST.get('phone_number')
        contact.email = request.POST.get('email')
        contact.address = request.POST.get('address')
        contact.birthday = request.POST.get('birthday')

        if not contact.email:
            contact.email = None
        if not contact.birthday:
            contact.birthday = None

        contact.save()
        return redirect('home')

    return redirect('home')

def delete_contact(request, contact_id):
    """Delete a contact"""
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('home')

    return redirect('home')