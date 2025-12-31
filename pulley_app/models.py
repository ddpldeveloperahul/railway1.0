from django.db import models
from Accounts.models import CustomUser
from django.utils import timezone

class PulleyDetection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    pole_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name/identifier of the pole")
    uploaded_image = models.ImageField(upload_to='uploads/')
    result_image = models.ImageField(upload_to='results/')
    temperature_c = models.FloatField(blank=True, null=True)
    htl_value = models.FloatField(blank=True, null=True)
    dist_p1_p2 = models.FloatField(blank=True, null=True)
    dist_p2_p3 = models.FloatField(blank=True, null=True)
    total_distance = models.FloatField(blank=True, null=True)
    expected_total = models.FloatField(blank=True, null=True)
    loss_mm = models.FloatField(blank=True, null=True)
    distances = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pulley Detection {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"



class DetectionRecord(models.Model):
    """Model to store camera detection data"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="detection_records",
        help_text="User who initiated the live detection",
    )
    pole_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name/identifier of the pole")
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Distance measurements (in mm)
    dist12 = models.FloatField(null=True, blank=True, help_text="Distance between pulley 1 and 2 (mm)")
    dist23 = models.FloatField(null=True, blank=True, help_text="Distance between pulley 2 and 3 (mm)")
    total = models.FloatField(null=True, blank=True, help_text="Total distance P1->P3 (mm)")
    
    # Expected values
    expected_total = models.FloatField(null=True, blank=True, help_text="Expected total distance (mm)")
    expected_dist12 = models.FloatField(null=True, blank=True, help_text="Expected distance P1->P2 (mm)")
    expected_dist23 = models.FloatField(null=True, blank=True, help_text="Expected distance P2->P3 (mm)")
    
    # Loss calculation
    loss_mm = models.FloatField(null=True, blank=True, help_text="Loss vs expected (mm)")
    
    # Detection info
    pulley_count = models.IntegerField(default=0, help_text="Number of pulleys detected")
    temperature_c = models.FloatField(null=True, blank=True, help_text="Temperature in Celsius")
    htl_value = models.FloatField(null=True, blank=True, help_text="HTL (L/2) value used for calculation")
    
    # Points data (stored as JSON-like format)
    points_json = models.TextField(null=True, blank=True, help_text="Pulley center points")
    image_path = models.ImageField(
        upload_to='best_captures/',
        null=True,
        blank=True,
        help_text="Saved annotated image file"
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"Detection at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.pulley_count} pulleys"
