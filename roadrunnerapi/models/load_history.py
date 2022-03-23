from django.db import models


class LoadHistory(models.Model):
    "Model for a LoadHistory object"
    load = models.ForeignKey("Load", on_delete=models.CASCADE)
    load_status = models.ForeignKey(
        "LoadStatus", on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=2)
    timestamp = models.DateTimeField(auto_now_add=True)
