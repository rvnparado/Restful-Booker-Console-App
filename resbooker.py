import requests
import json
import sys
import time
from datetime import datetime

BASE_URL = 'https://restful-booker.herokuapp.com/'

# method = input('What method do you want to use?: ')
methods = ['GET', 'POST', 'PUT', 'PATCH', 'DEL']
schema_keys = ['firstname','lastname','totalprice','depositpaid','bookingdates','additionalneeds', 'EXIT PATCH']
auth_details = {'username': 'admin', 'password': 'password123'}
save_booking = "booking_body.json"

def run(run_again):
    while run_again in ['Y', 'N']:
        # print(run_again)       
        if run_again == 'N':
            print('Exiting the program.')
            time.sleep(5)
            break
        elif run_again == 'Y':
            pull_requests()              
            run_again = input('Do you want to run the program again? (Y/N): ').upper()
            while run_again not in ['Y', 'N']:
                print('Invalid answer! Please enter Y or N.')
                run_again = input('Do you want to run the program again? (Y/N): ').upper()       

def create_token():
    print(auth_details)
    token = f'{BASE_URL}auth'
    response = requests.post(token, json=auth_details)  # json= should be the authorization details if there's any
    token_created = response.json()
    print(token_created)
    return token_created

def get_valid_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            # Try to parse the input as a date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')  # Return the formatted date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def save_body(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_items(filepath):
    try:
        with open(filepath, "r") as f:  # "r" stands for read
            data = json.load(f)  # this will read the python dictionary of the json data
        return data
    except:
        return {}

def booking_body():

    while True:  # Validating firstname
        firstname = input('Firstname: ')
        if firstname:
            break
        else:
            print("Firstname cannot be empty.")

    while True:  # Validating lastname
        lastname = input('Lastname: ')
        if lastname:
            break
        else:
            print("Lastname cannot be empty.")

    while True:  # Validating totalprice
        totalprice = input('Totalprice: ')
        if totalprice.isdigit():
            break
        else:
            print("Totalprice must be a number.")

    while True:  # Validating depositpaid
        depositpaid_input = input('Deposit paid? (Y/N): ').upper()
        if depositpaid_input in ['Y', 'N']:
            depositpaid = depositpaid_input == 'Y'
            break
        else:
            print("Please enter 'Y' for Yes or 'N' for No.")

    checkin = get_valid_date_input('Checkin (YYYY-MM-DD): ')  # Validating checkin

    checkout = get_valid_date_input('Checkout (YYYY-MM-DD): ')  # Validating checkout

    additionalneeds = input('Additional needs: ')  # Validating additionalneeds

    data = {
        'firstname': firstname,
        'lastname': lastname,
        'totalprice': totalprice,
        'depositpaid': depositpaid,
        'bookingdates': {
            'checkin': checkin,
            'checkout': checkout
        },
        'additionalneeds': additionalneeds
    }

    while True:  # Validating if the user wants to save the data
        is_booking_save = input(f'{data}\nDo you want to save this data? (Y/N): ').upper()
        if is_booking_save in ['Y', 'N']:
            if is_booking_save == 'Y':
                save_body(save_booking, data)
                # print('1')
                load_items(save_booking)
                # print(data)             
                break
            else:
                print('Data not saved!')
                break
        else:
            print("Please enter 'Y' for Yes or 'N' for No.")
    return data, is_booking_save

def get_booking():
    bookingid = input('Input booking id?: ')
    booking = f'{BASE_URL}booking/{bookingid}'
    response = requests.get(booking)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def post_booking(filepath):   
    _, is_booking_save = booking_body()
    if is_booking_save != 'N':
        print('Data saved!')
        data = load_items(save_booking)
        # load_items(save_booking)
        with open(filepath, 'r') as f:
            booking_body_details = json.load(f)
            booking = f'{BASE_URL}booking'
            response = requests.post(booking, json=booking_body_details)       
            if response.status_code == 200:
                data = response.json()
                print(f'{data}\nData Created!')
            else:
                print(f"Error: {response.status_code} - {response.text}")

def put_booking(filepath):
    token_created = create_token()  
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json', 'Cookie': f'token={token_created['token']}'}
    bookingid = input('Input booking id?: ')
    booking = f'{BASE_URL}booking/{bookingid}'
    response = requests.get(booking)
    
    try:
        if response.status_code == 200:
            data = response.json()            
            save_body(filepath,data)
            booking_body_details = load_items(filepath)            
            print(booking_body_details)
            updated_booking = booking_body()  
            response = requests.put(booking, json=updated_booking, headers=headers)           
            if response.status_code == 200:
                data = response.json()
                print(f'{data}\nBooking data updated!')                
            else:
                print(f"Error: {response.status_code} - {response.text}")          
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.HTTPError as errh:
         print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")        

def display_keys(schema_keys):
    schema_details = ''
    for index, key in enumerate(schema_keys, start=1):
        schema_details += f"{index} - {key}\n"
    return schema_details

def patch_booking(filepath):    
    token_created = create_token()  
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json', 'Cookie': f'token={token_created['token']}'}
    bookingid = input('Input booking id?: ')
    booking = f'{BASE_URL}booking/{bookingid}'
    response = requests.get(booking)
    try:
        if response.status_code == 200:
            data = response.json()            
            save_body(filepath,data)
            booking_body_details = load_items(filepath)            
            print(booking_body_details)       
            while True:
                selected_index = input(f'{display_keys(schema_keys)} \nSelect the details you want to Patch: ')
                try:    
                    if 1 <= int(selected_index) <= len(schema_keys) - 1 : 
                        print(selected_index)                       
                        selected_details = schema_keys[int(selected_index)-1]
                        if int(selected_index) in [1,2,6]: # this filter if the key is string
                            # print('Yes1')
                            if selected_details in booking_body_details:
                                print(f'{booking_body_details[selected_details]}')
                                updated_detail = input(f'Old: {booking_body_details[selected_details]} to New: ')
                                is_booking_save = input(f'{booking_body_details[selected_details]} to {updated_detail}\nDo you want to save this data? (Y/N): ').upper()
                                if is_booking_save in ['Y', 'N']:
                                    if is_booking_save == 'Y':
                                        # print('Yes')
                                        booking_body_details[selected_details] = updated_detail
                                        print(booking_body_details)
                                        save_body(save_booking, booking_body_details)
                                        patched_booking = load_items(save_booking) 
                                        response = requests.patch(booking, json=patched_booking, headers=headers)
                                        if response.status_code == 200:
                                            data = response.json()
                                            # print(f'{data}\nBooking data updated!')  
                                            print(f'Booking data updated!\n')             
                                        else:
                                            print(f"Error: {response.status_code} - {response.text}")              
                                    else:
                                        print('Data not saved!')                                       
                                else:              
                                    print("Please enter 'Y' for Yes or 'N' for No.")
                            else:        
                                print(f"The selected key '{selected_details}' does not exist.")
                                update_non_existing = input("Do you want to update the booking with this key? (Y/N): ").upper()       
                                if update_non_existing == 'Y':
                                    updated_detail = input(f"Enter the value for '{selected_details}': ")
                                    booking_body_details[selected_details] = updated_detail
                                    save_body(save_booking, booking_body_details)
                                    patched_booking = load_items(save_booking) 
                                    response = requests.patch(booking, json=patched_booking, headers=headers)
                                    if response.status_code == 200:
                                        data = response.json()
                                        # print(f'{data}\nBooking data updated!')
                                        print(f'Booking data updated!\n')                  
                                    else:
                                        print(f"Error: {response.status_code} - {response.text}") 
                                break
                        elif int(selected_index) in (3,4): # this filter if the key is int or bool
                            if int(selected_index) == 3:
                                while True:  # Validating totalprice
                                    print(f'{booking_body_details[selected_details]}')
                                    updated_detail = input(f'Old: {booking_body_details[selected_details]} to New: ')
                                    if updated_detail.isdigit():
                                        is_booking_save = input(f'{booking_body_details[selected_details]} to {updated_detail}\nDo you want to save this data? (Y/N): ').upper()
                                        if is_booking_save in ['Y', 'N']:
                                            if is_booking_save == 'Y':
                                                print('Yes')
                                                booking_body_details[selected_details] = updated_detail
                                                print(booking_body_details)
                                                save_body(save_booking, booking_body_details)
                                                patched_booking = load_items(save_booking) 
                                                response = requests.patch(booking, json=patched_booking, headers=headers)
                                                if response.status_code == 200:
                                                    data = response.json()
                                                    # print(f'{data}\nBooking data updated!')  
                                                    print(f'Booking data updated!\n')                
                                                else:
                                                    print(f"Error: {response.status_code} - {response.text}")              
                                            else:
                                                print('Data not saved!')                                       
                                        else:              
                                            print("Please enter 'Y' for Yes or 'N' for No.")
                                    else:
                                        print("Totalprice must be a number.")
                            else:
                                while True:  # Validating depositpaid
                                    updated_detail = input(f'Old: {booking_body_details[selected_details]} to New (Y/N): ').upper()
                                    if updated_detail in ['Y', 'N']:
                                        depositpaid = updated_detail == 'Y' # this will make depositpaid as bool
                                        is_booking_save = input(f'{booking_body_details[selected_details]} to {depositpaid}\nDo you want to save this data? (Y/N): ').upper()
                                        if is_booking_save in ['Y', 'N']:
                                            if is_booking_save == 'Y':
                                                # print('Yes')
                                                booking_body_details[selected_details] = depositpaid
                                                print(booking_body_details)
                                                save_body(save_booking, booking_body_details)
                                                patched_booking = load_items(save_booking) 
                                                response = requests.patch(booking, json=patched_booking, headers=headers)
                                                if response.status_code == 200:
                                                    data = response.json()
                                                    # print(f'{data}\nBooking data updated!')
                                                    print(f'Booking data updated!\n')                  
                                                else:
                                                    print(f"Error: {response.status_code} - {response.text}")              
                                            else:
                                                print('Data not saved!')                                       
                                        else:              
                                            print("Please enter 'Y' for Yes or 'N' for No.")
                                        break
                                    else:
                                        print("Please enter 'Y' for Yes or 'N' for No.")
                                print(selected_details)
                        elif int(selected_index) == 5: # this filter if the key is date
                            print(f'{booking_body_details[selected_details]}')
                            updated_detail_checkin = get_valid_date_input(f'Checkin - Old: {booking_body_details[selected_details]['checkin']} to New: ')
                            updated_detail_checkout = get_valid_date_input(f'Checkout - Old: {booking_body_details[selected_details]['checkout']} to New: ')
                            is_booking_save = input(f'checkin: {booking_body_details[selected_details]['checkin']} to {updated_detail_checkin}\ncheckout: {booking_body_details[selected_details]['checkout']}'
                                f'to {updated_detail_checkout}\nDo you want to save this data? (Y/N): ').upper()
                            if is_booking_save in ['Y', 'N']:
                                if is_booking_save == 'Y':
                                    booking_body_details[selected_details]['checkin'] = updated_detail_checkin
                                    booking_body_details[selected_details]['checkout'] = updated_detail_checkout
                                    print(booking_body_details)
                                    save_body(save_booking, booking_body_details)
                                    patched_booking = load_items(save_booking) 
                                    response = requests.patch(booking, json=patched_booking, headers=headers)
                                    if response.status_code == 200:
                                        data = response.json()
                                        print(f'{data}\nBooking data updated!')                
                                    else:
                                        print(f"Error: {response.status_code} - {response.text}")              
                                else:
                                    print('Data not saved!')                                       
                            else:              
                                print("Please enter 'Y' for Yes or 'N' for No.")
                            # print(updated_detail_checkin + ' | ' + updated_detail_checkout)                                                  
                    elif int(selected_index) == 7:
                        print('Exiting Patch method!')
                        break
                    else:
                        print("Please select details from 1 to 6!")                        
                except ValueError:
                    print("Please enter a valid integer!")         
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.HTTPError as errh:
         print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")  

def pull_requests():
    method = input(f'What method do you want to use? {methods[0:5]}:').upper()
    if method.upper() in methods:
        if method.upper() in methods[0]:
            print(f'METHOD: {method}')
            get_booking()
            return
        elif method.upper() in methods[1]:
            print(f'METHOD: {method}')
            post_booking(save_booking)
            return
        elif method.upper() in methods[2:5]:  # 2 is the place to start in the array and 5(number of lists) is the end of the array
            if method.upper() in methods[2]:
                print(f'METHOD: {method} - not yet developed.')
                put_booking(save_booking)
            elif method.upper() in methods[3]:
                print(f'METHOD: {method} - not yet developed.')
                patch_booking(save_booking)
            elif method.upper() in methods[4]:
                print(f'METHOD: {methods[4]} - not yet developed.')
    else:
        print('You have entered an unknown HTTP Method!')

run('Y')
# display_keys(save_booking)

# patch_booking(save_booking)
