from .models import Status

def get_unaccepted_car_count(self):
    car_count = Status.objects.filter(status = False).count()
    return {
        "car_count": car_count
    }
