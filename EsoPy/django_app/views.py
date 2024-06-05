from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import luadata
from django_app.utilities import load_data_into_database
from django_app.models import Account, Character

def welcome(request):
    return render(request, 'welcome.html')

def file_upload_form(request):
    return render(request, 'file_upload_form.html')

@csrf_exempt  # For simplicity, disable CSRF protection for this view
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        lua_content = uploaded_file.read().decode('utf-8')
        # Process the uploaded file
        try:
            lua_data = luadata.unserialize(lua_content)
            load_data_into_database(lua_data)
            return JsonResponse({'message': 'File uploaded and processed successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'File upload failed or file not provided.'}, status=400)
    
def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'account_list.html', {'accounts': accounts})

def account_detail(request, account_name):
    account = get_object_or_404(Account, name=account_name)
    characters = Character.objects.filter(account=account)
    return render(request, 'account_detail.html', {'account': account, 'characters': characters})

def character_detail(request, character_id):
    character = get_object_or_404(Character, character_id=character_id)
    return render(request, 'character_detail.html', {'character': character})