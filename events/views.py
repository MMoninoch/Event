# events/views.py
import base64
import os
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Event, Material
import qrcode
from django.http import HttpResponse
from django.core.files.base import ContentFile
from io import BytesIO
from zipfile import ZipFile


def about(request):
    return render(request, 'events/about.html')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def materials_list(request, slug):
    event_materials = Material.objects.filter(event__slug=slug)
    return render(request, 'events/materials_list.html', {'materials': event_materials, 'event_slug': slug})

def generate_qr_code_for_event_list(request, event_slug):
    # Create a QR code for the material list URL of the specified event
    data = request.build_absolute_uri(reverse('materials_list', kwargs={'slug': event_slug}))
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=100,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an in-memory stream to save the image
    stream = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(stream, "PNG")

    # Return the base64-encoded QR code data
    return base64.b64encode(stream.getvalue())

def download_all_materials(request, event_slug):
    # Get all materials for the specified event
    materials = Material.objects.filter(event__slug=event_slug)

    # Create a temporary zip file
    zip_filename = f"{event_slug}_materials.zip"
    zip_path = os.path.join("/tmp", zip_filename)

    with ZipFile(zip_path, 'w') as zip_file:
        for material in materials:
            # Add each material to the zip file
            file_path = material.file.path
            zip_file.write(file_path, os.path.basename(file_path))

    # Create a response with the zip file
    response = HttpResponse(content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    with open(zip_path, 'rb') as zip_data:
        response.write(zip_data.read())

    # Delete the temporary zip file
    os.remove(zip_path)

    return response

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    materials = Material.objects.filter(event=event)

    # Generate QR code for the material list URL of the event
    qr_code_for_event_list = generate_qr_code_for_event_list(request, event.slug)

    for material in materials:
        if material.file:
            # Generate QR code for each material's download link
            download_link = request.build_absolute_uri(material.file.url)
            qr_code = generate_qr_code_for_event(download_link)
            # Save the base64-encoded QR code data in the material model
            material.qr_code = qr_code.decode('utf-8')

            # Generate QR code for the material detail URL
            material_detail_url = request.build_absolute_uri(reverse('material_detail', kwargs={'pk': material.pk}))
            material.qr_code_for_detail = generate_qr_code_for_event(material_detail_url).decode('utf-8')

    return render(request, 'events/event_detail.html', {'event': event, 'materials': materials, 'qr_code_for_event_list': qr_code_for_event_list})

def generate_qr_code_for_event_list(request, event_slug):
    # Generate QR code for the event material list URL
    event_material_list_url = request.build_absolute_uri(reverse('materials_list', kwargs={'slug': event_slug}))
    qr = generate_qr_code_for_event(event_material_list_url)
    return qr.decode('utf-8')

def generate_qr_code_for_event(data):
    # Create a QR code for the provided data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an in-memory stream to save the image
    stream = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(stream, "PNG")

    # Return the base64-encoded QR code data
    return base64.b64encode(stream.getvalue())

def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'events/material_detail.html', {'material': material})
