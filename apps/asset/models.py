from django.db import models
from django.contrib.auth.models import User

class InvestementLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=50)
    total_profit = models.DecimalField(max_digits=12, decimal_places=2)
    last_nav_upadate = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"self.asset_name - {self.user.username}"