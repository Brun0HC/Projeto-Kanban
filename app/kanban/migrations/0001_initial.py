# Generated by Django 5.1.1 on 2024-09-20 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Kanban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('imagem', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('image_file', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('idKanban', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.kanban')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(default='99999999999', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('textDescription', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('position', models.IntegerField(default=0)),
                ('start', models.DateField(auto_now_add=True)),
                ('due', models.DateField(auto_now_add=True)),
                ('concluded', models.BooleanField(default=False)),
                ('column', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='kanban.column')),
                ('idMemberCreator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kanban.member')),
            ],
        ),
        migrations.AddField(
            model_name='column',
            name='idKanban',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.kanban'),
        ),
        migrations.CreateModel(
            name='CardLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.card')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.label')),
            ],
        ),

        migrations.AddField(
            model_name='kanban',
            name='idMemberCreator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kanban.member'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('idCard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.card')),
                ('idMember', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.member')),
            ],
        ),
        migrations.CreateModel(
            name='CardMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.card')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.member')),
            ],
        ),
        migrations.CreateModel(
            name='MemberInKanban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('GUEST', 'Guest'), ('ADMIN', 'Admin')], default='GUEST', max_length=6)),
                ('idKanban', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.kanban')),
                ('idMember', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanban.member')),
            ],
        ),
    ]