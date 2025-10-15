from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from .models import Contact, Group
import json

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
    all_contacts = Contact.objects.all().order_by('first_name')

    groups_with_counts = []
    for group in groups:
        groups_with_counts.append({
            'id': group.id,
            'name': group.name,
            'contact_count': group.contacts.count()
        })

    contacts_json = json.dumps([{
        'id': contact.id,
        'first_name': contact.first_name,
        'full_name': contact.get_full_name(),
        'phone_number': contact.phone_number
    } for contact in all_contacts])

    return render(request, 'group.html', {
        'groups': groups_with_counts,
        'all_contacts': all_contacts,
        'all_contacts_json': contacts_json
    })

@transaction.atomic
def create_group(request):
    """Create a new group with atomic transaction"""
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_ids = request.POST.getlist('contacts')

        if name and contact_ids:
            try:
                group = Group.objects.create(name=name)

                contacts = Contact.objects.filter(id__in=contact_ids)
                if contacts.count() != len(contact_ids):
                    raise ValueError("Some contacts do not exist")

                group.contacts.set(contacts)

            except Exception as e:
                print(f"Error creating group: {e}")

        return redirect('groups')

    return redirect('groups')

@transaction.atomic
def update_group(request, group_id):
    """Update an existing group with atomic transaction"""
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        contact_ids = request.POST.getlist('contacts')

        if name:
            try:
                group.name = name
                group.save()

                if contact_ids:
                    contacts = Contact.objects.filter(id__in=contact_ids)
                    if contacts.count() != len(contact_ids):
                        raise ValueError("Some contacts do not exist")

                    group.contacts.set(contacts)
                else:
                    group.contacts.clear()

            except Exception as e:
                print(f"Error updating group: {e}")

        return redirect('groups')

    return redirect('groups')

@transaction.atomic
def delete_group(request, group_id):
    """Delete a group with atomic transaction"""
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        try:

            group.delete()

        except Exception as e:
            print(f"Error deleting group: {e}")

        return redirect('groups')

    return redirect('groups')

def group_members(request, group_id):
    """Get group members as JSON"""
    group = get_object_or_404(Group, id=group_id)
    member_ids = list(group.contacts.values_list('id', flat=True))

    return JsonResponse({
        'member_ids': member_ids
    })