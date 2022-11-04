from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    """Serializes an order request object."""
    date = serializers.DateField()
    time = serializers.CharField(max_length = 5)
    pick_up_place = serializers.CharField(max_length = 7)
    delivery_place = serializers.CharField(max_length = 7)
    driver = serializers.IntegerField()

    def validate_time(self, time):  
        """Validates time format (HH:MM)"""      
        if ":" not in time or len(time) != 5:
            raise ValidationError(f'{time} is not in a valid format (HH:MM).')
        
        try:
            if int(time.split(":")[0]) > 23 or int(time.split(":")[1]) > 59:
                raise ValidationError('')
        except ValidationError:
            raise ValidationError(f'{time} is not a valid hour.')
        except ValueError:
            raise ValidationError(f'{time} is not in a valid format (HH:MM).')
        
        return time

    def validate_pick_up_place(self, pick_up_place):
        """Validates pick up place format (100,100)"""
        if "," not in pick_up_place:
            raise ValidationError(f'{pick_up_place} is not in a valid format (0,0 to 100,100)')

        try:
            if int(pick_up_place.split(",")[0]) > 100 or int(pick_up_place.split(",")[1]) > 100:
                raise ValidationError('')
        except ValidationError:
            raise ValidationError(f'{pick_up_place} coordinate out of boundaries from 0,0 to 100,100')
        except ValueError:
            raise ValidationError(f'{pick_up_place} is not in a valid format (0,0 to 100,100)')
        
        return pick_up_place

    def validate_delivery_place(self, delivery_place):
        """Validates pick up place format (100,100)"""
        if "," not in delivery_place:
            raise ValidationError(f'{delivery_place} is not in a valid format (0,0 to 100,100)')

        try:
            if int(delivery_place.split(",")[0]) > 100 or int(delivery_place.split(",")[1]) > 100:
                raise ValidationError('')
        except ValidationError:
            raise ValidationError(f'{delivery_place} coordinate out of boundaries from 0,0 to 100,100')
        except ValueError:
            raise ValidationError(f'{delivery_place} is not in a valid format (0,0 to 100,100)')
        
        return delivery_place