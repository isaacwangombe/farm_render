from hashlib import blake2b
from tokenize import blank_re
from django.db import models
from django.db.models import Avg, Sum, Count, Max
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save

# Create your models here.



class Batch(models.Model):
	farm = models.CharField(max_length=30)
	picture = models.ImageField(upload_to = 'batch/',default='batch/default.jpg')
	purchased = models.IntegerField()
	unit_price = models.IntegerField()
	projected_SP = models.IntegerField()
	start_date = models.DateField(auto_now_add=True)
	end_date = models.DateField(auto_now_add=False)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

	def get_all():
		result = Batch.objects.all()
		return result


	@classmethod
	def get_by_id(cls, id):
		result = cls.objects.get(id=id)
		return result

	@classmethod
	def filter_by_user(cls, user):
		result = cls.objects.filter(user=user).order_by('-id')
		return result
	
	def purchase_cost(id):
			u_p = list(Batch.objects.filter(id=id).aggregate(Sum('unit_price')).values())
			u_p = int("".join(map(str,u_p)))
			
			purch = list(Batch.objects.filter(id=id).aggregate(Sum('purchased')).values())
			purch = int("".join(map(str,purch)))
			cost = u_p * purch
			return cost

	def expected_revenue(id):
			s_p = list(Batch.objects.filter(id=id).aggregate(Sum('projected_SP')).values())
			s_p = int("".join(map(str,s_p)))
			
			purch = list(Batch.objects.filter(id=id).aggregate(Sum('purchased')).values())
			purch = int("".join(map(str,purch)))
			cost = s_p * purch
			return cost
	def num_purchased(id):
			purch = list(Batch.objects.filter(id=id).aggregate(Sum('purchased')).values())
			purch = int("".join(map(str,purch)))
			return purch

class Customers(models.Model):
	name = models.CharField(max_length=30)
	number = models.IntegerField()
	date = models.DateField(auto_now_add=True)
	batch = models.ForeignKey(Batch, on_delete=models.DO_NOTHING)


	def __str__(self):
		return self.name

	@classmethod
	def customers_by_batch(cls, id):
		result = Customers.objects.filter(batch = id)
		return result

		
class Deaths(models.Model):
	number = models.IntegerField()
	reason = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

	@classmethod
	def death_by_batch(cls, id):
		result = Deaths.objects.filter(batch = id)
		return result

	@classmethod
	def death_sum(cls, id):
			table = list(Deaths.objects.filter(batch_id=id).aggregate(Sum('number')).values())
			test = all( i == None for i in table)
			if (test) == True:
					return 1
			else:
					table = int("".join(map(str,table)))
					return table


class ExpenseGroup(models.Model):
		group = models.CharField( max_length=30)
		batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

	
		def __str__(self):
			return self.group



class Expenses(models.Model):
	amount = models.IntegerField()
	group = models.ForeignKey(ExpenseGroup, on_delete=models.DO_NOTHING)
	details = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	batch = models.ForeignKey(Batch, on_delete=models.CASCADE)


	def __str__(self):
		return str(f"expense- {self.id}")


	@classmethod
	def exp_by_batch(cls, id):
		result = Expenses.objects.filter(batch = id)
		return result

	@classmethod
	def search(cls, id, group):
			test =  Expenses.objects.filter(batch__id= id, group__group__contains=group)
			return test


	@classmethod
	def sum_by_group_list(cls):
		group = ExpenseGroup.objects.all()
		group_list = []
		for i in group:
				group_list.append(i.group)
				# group_list= ("".join(map(str,group_list)))
		yield group_list

	@classmethod
	def sum_by_group_amount(cls, id):
		group = ExpenseGroup.objects.all()
		group_list = []
		for i in group:
				group_list.append(i.group)
		lists = group_list
		for i in lists:

			table =  list(Expenses.objects.filter(batch__id= id, group__group__contains=i).aggregate(Sum('amount')).values())
			test = all( i == None for i in table)
			if (test) == True:
					return 1
			else:
					table = int("".join(map(str,table)))
			yield table


	@classmethod
	def expense_sum(cls, id):
			table = list(Expenses.objects.filter(batch_id=id).aggregate(Sum('amount')).values())
			test = all( i == None for i in table)
			if (test) == True:
					return 1
			else:
					table = int("".join(map(str,table)))
					return table

	@classmethod
	def expense_sum_per(cls, id):
			table = list(Expenses.objects.filter(batch_id=id).values('group').annotate(sum=Sum('amount')))

			# table = table[0]
			# table = table.get('sum')
			table = len(table)

			return table




class Revenue(models.Model):
	sell_price = models.IntegerField()
	number = models.IntegerField()
	date = models.DateField(auto_now_add=True)
	batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customers, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

	@classmethod
	def avg_selling_price(cls, id):
			table = list(Revenue.objects.filter(batch_id=id).aggregate(Avg('sell_price')).values())
			test = all( i == None for i in table)
			if (test) == True:
					return 1
			else:
					table = float("".join(map(str,table)))

					return table


	@classmethod
	def total_revenue(cls, id):
			s_price = list(Revenue.objects.filter(batch_id=id).aggregate(Sum('sell_price')).values())	
			test = all( i == None for i in s_price)
			if (test) == True:
					return 1
			else:
					s_price = int("".join(map(str,s_price)))
			num = list(Revenue.objects.filter(batch_id=id).aggregate(Sum('number')).values())
			test = all( i == None for i in num)
			if (test) == True:
					return 1
			else:
					num = int("".join(map(str,num)))

			total = s_price * num

			return total					
	

	@classmethod
	def sum_by_customer_list(cls):
		group = Customers.objects.all()
		group_list = []
		for i in group:
				group_list.append(i.name)
		yield group_list

	@classmethod
	def sum_by_customer_amount(cls, id):
		group = Customers.objects.all()
		group_list = []
		for i in group:
				group_list.append(i.name)
		lists = group_list
		for i in lists:

			table =  list(Revenue.objects.filter(batch__id= id, customer__name__contains=i).aggregate(Sum('number')).values())
			test = all( i == None for i in table)
			if (test) == True:
					return 1
			else:
					table = int("".join(map(str,table)))
			yield table

	@classmethod
	def sum_by_customer_number(cls, id):
		group = Customers.objects.all()
		group_list = []
		for i in group:
				group_list.append(i.name)
		lists = group_list
		for i in lists:

			table =  list(Revenue.objects.filter(batch__id= id, customer__name__contains=i).aggregate(Sum('sell_price')).values())
			test = all( i == None for i in table)
			if (test) == True:
					return 1
			else:
					table = int("".join(map(str,table)))
			yield table

	@classmethod
	def sum_by_customer_total(cls, id):
		group = Customers.objects.all()
		group_list = []
		for i in group:
				group_list.append(i.name)
		lists = group_list
		for i in lists:

			s_price = list(Revenue.objects.filter(batch__id=id, customer__name__contains=i).aggregate(Sum('sell_price')).values())
			test = all( i == None for i in s_price)
			if (test) == True:
					return 1
			else:
					s_price = int("".join(map(str,s_price)))
			num = list(Revenue.objects.filter(batch__id=id, customer__name__contains=i).aggregate(Sum('number')).values())
			test = all( i == None for i in num)
			if (test) == True:
					return 1
			else:
					num = int("".join(map(str,num)))

			total = s_price * num

			yield total		

class UserProfile(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	picture = CloudinaryField('image')
	editor = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)


	@classmethod
	def get_by_profile(cls, editor):
		profile = UserProfile.objects.filter(editor__username=editor).last()

		return profile