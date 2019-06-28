from django.db import models
from smart_selects.db_fields import ChainedForeignKey


# 가게 - 메뉴/카테고리 - 옵션/카테고리
class Store(models.Model):
    name = models.CharField(max_length=100)
    store_img = models.ImageField(upload_to='images/store/', blank=True)
    min_price_won = models.PositiveIntegerField()
    delivery_fee_won = models.PositiveIntegerField()
    menu_intro = models.TextField() #메뉴상단에 들어갈 문구
    menu_origin = models.CharField(max_length=300) #원산지 표기
    info = models.TextField() #정보탭에 들어갈 문구
    def __str__(self):
        return self.name

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    category_order = models.PositiveSmallIntegerField() #순서
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    store_img = models.ImageField(upload_to='images/menu/', blank=True)
    description = models.CharField(max_length=200)
    price_won = models.PositiveIntegerField()
    
    category = ChainedForeignKey(MenuCategory, chained_field="store", chained_model_field="store")

    #category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    def __str__(self):
        return self.category.name + '>' + self.name

class MenuOptionCategory(models.Model):
    name = models.CharField(max_length=50)
    required_yn = models.BooleanField() #필수선택여부
    category_order = models.PositiveSmallIntegerField() #순서
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    menu = ChainedForeignKey(Menu, chained_field="store", chained_model_field="store")
    #menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    def __str__(self):
        return self.menu.name + '>' + self.name

class MenuOption(models.Model):
    name = models.CharField(max_length=50)
    extra_price_won = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    category = ChainedForeignKey(MenuOptionCategory, chained_field="store", chained_model_field="store")
    #category = models.ForeignKey(MenuOptionCategory, on_delete=models.CASCADE)
    def __str__(self):
        return self.name