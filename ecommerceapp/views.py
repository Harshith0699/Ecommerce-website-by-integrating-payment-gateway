from math import ceil
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from ecommerceapp import keys
from ecommerceapp.models import Contact, OrderUpdate,Product,Orders

# Create your views here.
def index(request):
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    print(cats,catprods)
    for cat in cats:
        prod = Product.objects.filter(category = cat)

        n=len(prod)
        nslides = n//4 +(ceil(n/4) -(n//4))
        print(prod,n,nslides)

        allprods.append([prod,range(1,nslides),nslides])
    context={
        'allprods':allprods,
    }
    Product.objects.all()
    return render(request,"index.html",context)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        desc = request.POST['desc']
        phone = request.POST['phone']
        
        myquery = Contact(name=name,email=email,desc=desc,phone=phone)
        myquery.save()
        messages.info(request,"We will get back to you.")
    return render(request,"contact.html")
def about(request):
    return render(request,"about.html")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
# # PAYMENT INTEGRATION

        id = Order.order_id
        oid=str(id)+"ShopyCart"
        param_dict = {

            'MID':keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')

