# Generated by Django 3.2.3 on 2023-08-01 16:46

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_rename_countingredient_ingredientinrecipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.IntegerField(validators=[recipes.validators.validate_ingredientInRecipe_amount]),
        ),
    ]