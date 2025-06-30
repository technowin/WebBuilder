from django.shortcuts import render

# Create your views here.

def workflow_starts(request):
    try:
        return render(request, 'Workflow/index.html')
    except Exception as e:
        # Optional: log the error or show a custom error page
        print(f"Error in workflow_starts view: {e}")
        return render(request, 'error.html', {'error_message': str(e)})