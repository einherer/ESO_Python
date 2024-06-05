from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=100)

class Account(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Character(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    character_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    faction_name = models.CharField(max_length=100, blank=True, null=True)
    race_name = models.CharField(max_length=100, blank=True, null=True)
    class_name = models.CharField(max_length=100, blank=True, null=True)
    level = models.IntegerField(default=0)  # Ensure default value
    champion_points = models.IntegerField(default=0)
    is_werewolf = models.BooleanField(default=False)
    is_vampire = models.BooleanField(default=False)

class Equipment(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    slot = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    item_link = models.TextField()
    quality = models.CharField(max_length=50)
    icon = models.TextField()
    set_info = models.TextField()
    set_bonus_info = models.TextField()
    enchant_info = models.TextField()

class ActiveAbility(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ability_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.TextField()

class ActiveBuff(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    buff_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.TextField()
