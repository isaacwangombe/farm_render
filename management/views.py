from django.shortcuts import render, redirect
from .models import Batch, Deaths, Expenses, Revenue, Customers,UserProfile
from .forms import BatchForm, DeathsForm, ExpensesForm, RevenueForm, CustomersForm,UserProfileForm, ExpenseGroupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.

def about(request):
	
	return render(request, 'about/about.html', )

def landing(request):
	
	return render(request, 'landing/landing.html', )




def home(request, user):
	projects = Batch.filter_by_user(user) 
	
	return render(request, 'business/home.html',{'projects':projects})


def batch(request, id):
		# Batch queries
	projects = set(Batch.get_all())
	batch = Batch.get_by_id(id)
	purchase_price = Batch.purchase_cost(id)
	expected_revenue = Batch.expected_revenue(id)
	number_purchased = Batch.num_purchased(id)

# Deaths queries
	deaths = Deaths.death_by_batch(id) 
	death_sum =Deaths.death_sum(id)

# expences queries
	expense_sum = Expenses.expense_sum(id)
	expenses = Expenses.exp_by_batch(id) 
	expense_by_group = Expenses.sum_by_group_amount(id)
	expense_by_group_list = Expenses.sum_by_group_list()

# revenue queries
	revenue_sum = Revenue.total_revenue(id)
	revenue_by_customer_list = Revenue.sum_by_customer_list()
	revenue_by_customer_amount = Revenue.sum_by_customer_amount(id)
	revenue_by_customer_number = Revenue.sum_by_customer_number(id)
	revenue_by_customer_total = Revenue.sum_by_customer_total(id)
	avg_selling_price = Revenue.avg_selling_price(id)
	customers = Customers.customers_by_batch(id)

# profit calculation
	real_profit = revenue_sum - expense_sum
	diff_exp_real = (real_profit - expected_revenue)
 

#  Graph viewss
# batch graphs
	revenue_labels= ["Expected Gross Revenue","Total gross revenue","Actual revenue"]
	revenue_data =[expected_revenue,revenue_sum,real_profit ]
	revenue_diff = (expected_revenue -real_profit)
#Revenue to expenses
	expenses_to_revenue_label= ["Total Revenue","Total Expenses", "Net Revenue"]
	expenses_to_revenue_data= [revenue_sum,expense_sum, real_profit]

#loss to death
	loss_by_death = (death_sum * avg_selling_price)
	revenue_without_death = (revenue_sum + loss_by_death) 
	loss_to_death_label= ["Possible Revenue","loss by death","Actual revenue"]
	loss_to_death_data= [revenue_without_death,loss_by_death,revenue_sum]
	loss_to_death_labelv2= ["Possible Revenue","Actual revenue","loss by death"]
	loss_to_death_datav2= [revenue_without_death,revenue_sum,loss_by_death]

# Expenses graphs
# expenses per item
	expense_item_label= []
	expense_item_amount= []
	for expense in expenses:
			expense_item_label.append(str(expense.details))
			expense_item_amount.append(str(expense.amount))

# expenses by group
	expense_group_amount= []

	for expense in expense_by_group:
			expense_group_amount.append(expense)

	for label in expense_by_group_list:
			expense_group_label = label


# Deaths by reason
	death_label= []
	death_amount= []
	for death in deaths:
			death_label.append(str(death.reason))

			death_amount.append(str(death.number))


# revenue by customer
	rev_customer_amount= []
	num_per_customer_amount= []
	total_by_customer_amount= []

	for revenue in revenue_by_customer_amount:
			rev_customer_amount.append(revenue)
	for number in revenue_by_customer_number:
			num_per_customer_amount.append(number)

	for total in revenue_by_customer_total:
			total_by_customer_amount.append(total)

	for label in revenue_by_customer_list:
			revenue_customer_label = label


	#  calculating Selling price by profits
	# if 'desired_profit' in request.GET and request.GET['desired_profit']:
	result = int(request.GET.get('desired_profit',False))
	# 		print(result)
	if type(result) == int or type(result) == float:
			selling_price=(expense_sum+purchase_price+result)/(number_purchased-death_sum)
	# 		print(selling_price)
	else:
			selling_price = "Kindly enter a valid number"
			# 	print("error")

	return render(request, 'business/batch.html',
	{'deaths':deaths, 'id':id, 'death_sum':death_sum, 'purchase_price':purchase_price, 'expense_sum':expense_sum, 'label':label,'revenue_sum':revenue_sum, 'real_profit':real_profit, 'batch':batch, 'projects':projects, 'expense_by_group':expense_by_group, 'customers':customers,'expenses':expenses, 'expense_by_group_list':expense_by_group_list, 'revenue_by_customer_list':revenue_by_customer_list, 'revenue_by_customer_amount':revenue_by_customer_amount, 'revenue_by_customer_number':revenue_by_customer_number, 'revenue_by_customer_total':revenue_by_customer_total, 'expected_revenue':expected_revenue, 'revenue_labels':revenue_labels, 'revenue_data':revenue_data, 'expense_item_label':expense_item_label, 'expense_item_amount':expense_item_amount, 'expense_group_label':expense_group_label, 'expense_group_amount':expense_group_amount,'death_label':death_label, 'death_amount':death_amount,'rev_customer_amount':rev_customer_amount,'num_per_customer_amount':num_per_customer_amount, 'total_by_customer_amount':total_by_customer_amount, 'revenue_customer_label':revenue_customer_label, 'expenses_to_revenue_label':expenses_to_revenue_label, 'expenses_to_revenue_data':expenses_to_revenue_data, 'avg_selling_price':avg_selling_price, 'loss_to_death_label':loss_to_death_label, 'loss_to_death_data':loss_to_death_data,'loss_to_death_labelv2':loss_to_death_labelv2,'loss_to_death_datav2':loss_to_death_datav2, 'revenue_diff':revenue_diff,'diff_exp_real':diff_exp_real, 'selling_price':selling_price})



@login_required(login_url='/accounts/login/')
def new_batch(request):
	print('test')
	current_user = request.user	
	print('test1')
	if request.method == 'POST':
		print('test2')
		form = BatchForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.save(commit=False)
			name.user = current_user
			name.save()
		return redirect( 'home',  current_user.id )
	else:
		form = BatchForm()
			
	return render(request, 'business/new_batch.html', {'form': form})



@login_required(login_url='/accounts/login/')
def new_death(request, id):
	batch = Batch.get_by_id(id)
	current_user = request.user			
	if request.method == 'POST':
		form = DeathsForm(request.POST)
		if form.is_valid():
			name = form.save(commit=False)
			name.user = current_user
			name.batch = batch
			name.save()
		return redirect( 'batch', batch.id )
	else:
		form = DeathsForm()
			
	return render(request, 'business/new_death.html', {'form': form, 'batch':batch})



@login_required(login_url='/accounts/login/')
def new_customer(request, id):
	batch = Batch.get_by_id(id)
	current_user = request.user			
	if request.method == 'POST':
		form = CustomersForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.save(commit=False)
			name.user = current_user
			name.batch = batch
			name.save()
		return redirect( 'new_revenue', batch.id )
	else:
		form = CustomersForm()
			
	return render(request, 'business/new_customer.html', {'form': form, 'batch':batch})



@login_required(login_url='/accounts/login/')
def new_expense(request, id):
	batch = Batch.get_by_id(id)
	current_user = request.user			
	if request.method == 'POST':
		# form2 = ExpenseGroupForm(request.POST)
		form = ExpensesForm(request.POST)

		if form.is_valid():
			# name2 = form.save(commit=False)
			name = form.save(commit=False)
			name.user = current_user
			name.batch = batch
			name.save()
			# name2.save()
		return redirect( 'batch', batch.id)
	else:
		form = ExpensesForm()
			
	return render(request, 'business/new_expense.html', {'form': form, 'batch':batch})

@login_required(login_url='/accounts/login/')
def new_expense_group(request, id):
	batch = Batch.get_by_id(id)
	current_user = request.user			
	if request.method == 'POST':
		form = ExpenseGroupForm(request.POST)

		if form.is_valid():
			name = form.save(commit=False)
			name.user = current_user
			name.batch = batch
			name.save()
		return redirect( 'new_expense', batch.id)
	else:
		form = ExpenseGroupForm()
			
	return render(request, 'business/new_expense_group.html', {'form': form,'batch':batch})


	
@login_required(login_url='/accounts/login/')
def new_revenue(request, id):
	batch = Batch.get_by_id(id)
	current_user = request.user			
	if request.method == 'POST':
		form = RevenueForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.save(commit=False)
			name.user = current_user
			name.batch = batch
			name.save()
		return redirect( 'batch', batch.id )
	else:
		form = RevenueForm()
			
	return render(request, 'business/new_revenue.html', {'form': form, 'batch':batch})


@login_required(login_url='/accounts/login/')
def profile(request, editor):
		profile = UserProfile.get_by_profile(editor)

		return render(request, 'profile/profile.html', {'profile': profile, "editor": editor})



@login_required(login_url='/accounts/login/')
def new_profile(request):
		current_user = request.user

		if request.method == 'POST':
				form = UserProfileForm(request.POST, request.FILES)

				if form.is_valid():
						profile = form.save(commit=False)
						profile.editor = current_user
						profile.save()
				return redirect('profile', current_user)
		else:
				form = UserProfileForm()

		return render(request, 'profile/new_profile.html', {'form': form})



