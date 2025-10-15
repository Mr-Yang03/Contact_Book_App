from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Contact, Group

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

def groups(request):
    """Display all groups"""
    groups = Group.objects.all().order_by('name')

    # Count contacts for each group
    groups_with_counts = []
    for group in groups:
        groups_with_counts.append({
            'id': group.id,
            'name': group.name,
            'contact_count': group.contacts.count()
        })

    return render(request, 'group.html', {
        'groups': groups_with_counts
    })

def create_group(request):
    """Create a new group"""
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            Group.objects.create(name=name)

        return redirect('groups')

    return redirect('groups')

def update_group(request, group_id):
    """Update an existing group"""
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            group.name = name
            group.save()

        return redirect('groups')

    return redirect('groups')

def delete_group(request, group_id):
    """Delete a group"""
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        group.delete()
        return redirect('groups')

    return redirect('groups')