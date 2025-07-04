class AgeRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only apply logic after view has been processed
        if hasattr(request, 'user') and request.user.is_authenticated:
            # List of paths that require age verification
            age_restricted_paths = [
                '/api/v1/products/',  # Add your restricted endpoints here
            ]
            
            # Check if the current path requires age verification
            requires_age_check = any(request.path.startswith(path) for path in age_restricted_paths)
            
            if requires_age_check and hasattr(request.user, 'is_adult') and not request.user.is_adult:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Age restriction: You must be at least 18 years old'}, status=403)
                
        return response
