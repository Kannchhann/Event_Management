from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson.objectid import ObjectId  # MongoDB ID handling
from datetime import datetime, timedelta
import threading
import time

import os

# Email Configuration
EMAIL_ADDRESS = "kpevents45@gmail.com"
EMAIL_PASSWORD = "ohor dama cjgb ndjt"  # Use an app password if needed

# Flask App Initialization
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Secret key for session management

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['event_management']
bookings_collection = db['bookings']
# Contact Enquiry Collection
contact_collection = db['contact_enquiries']

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Routes for Pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/party')
def party():
    return render_template('party.html')

@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/termscondition.html')
def termscondition():
    return render_template('termscondition.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


# Event Detail Pages
@app.route('/wedding')
def wedding_details():
    return render_template('wedding.html')

@app.route('/wp')
def wp():
    return render_template('wp.html') 



@app.route('/birthday')
def birthday_details():
    return render_template('birthday.html')
@app.route('/bbook')
def bbook():
    return render_template('Bbook.html')



@app.route('/anniversary')
def anniversary_details():
    return render_template('anniversary.html')
@app.route('/abook')
def abook():
    return render_template('Abook_now.html')


@app.route('/newyear')
def newyear_details():
    return render_template('newyear.html')
@app.route('/nybook')
def nybook():
    return render_template('NYbook.html')



@app.route('/business_meetings')
def bm_details():
    return render_template('business_meetings.html')

@app.route('/schedule_meeting')
def sm_form():
    return render_template('schedule_meeting.html')

@app.route('/christmas')
def christmas_details():
    return render_template('christmas.html')

@app.route('/cbook')
def cbook():
    return render_template('Cbook_now.html')


@app.route('/clubparty_details')
def clubparty_details():
    return render_template('clubparty_details.html')


@app.route('/clubBook')
def clubBook():
    package_name = request.args.get('package', 'Custom Package')

    # Define details for each package
    package_offers = {
        'Silver Party Package': [
            'Venue for 4 hours',
            'Basic DJ Setup',
            'Mocktails + Light Snacks',
            'Basic Decorations',
            'Selfie Point',
            'Basic Lounge Area for Relaxation'
        ],
        'Gold Party Package': [
            'Venue for 6 hours',
            'DJ with Lights & Smoke',
            'Snacks + Drinks',
            'Theme-based Decor',
            'Photo Booth with Props',
            'Return Gifts'
        ],
        'Platinum Party Package': [
            'Full Night Venue',
            'Premium DJ + Live Artist',
            'Food + Mocktail Bar',
            'Laser Lights + Smoke Machine',
            'VIP Lounge Access'
        ]
    }
    
    # Define prices for each package
    package_prices = {
        'Silver Party Package': 17698,
        'Gold Party Package': 29498,
        'Platinum Party Package': 47198,
    }

    # Get the selected package's details and price
    package_details = package_offers.get(package_name, [])
    price = package_prices.get(package_name, 0)  # Default price is 0 for Custom Package

    return render_template("clubBook.html", package_name=package_name, package_details=package_details, price=price)

@app.route('/submit_booking_club', methods=['POST'])
def submit_booking_club():
    booking_data = {
        'package_name': request.form['package_name'],
        'name': request.form['name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'guests': request.form['guests'],
        'date': request.form['date'],
        'requests': request.form['requests'],
        'total-cost': request.form['total-cost'],
    }

# Save the booking data into MongoDB
    bookings_collection.insert_one(booking_data)


    return render_template('clubBooking_success.html', booking=booking_data)



# 📌 Package Details for Bookings
@app.route('/book/<package_name>')
def book(package_name):
    package_details_map = {
        "The Catholic Wedding": [
            "- Beachside venue with elegant decor",
            "- Customized Catholic wedding rituals setup",
            "- Catering services with continental and Goan cuisine",
            "- Live choir and music band",
            "- Wedding photography and videography",
            "- Accommodation arrangements for guests"
        ],
        "The Royal Wedding": [
            "- Grand palace venue with royal-themed decorations",
            "- Traditional Rajasthani welcome for guests",
            "- Sangeet night with cultural performances",
            "- Included honeymoon suite for the couple",
            "- Full catering services with royal cuisine",
            "- Horse and elephant entry for the groom"
        ],
          "The South Indian Wedding": [
            "- Serene resort by the backwaters with floral decor",
            "- Traditional South Indian wedding rituals",
            "- Haldi and reception arrangements included",
            "- Authentic South Indian vegetarian cuisine",
            "- Carnatic music and classical dance performances",
            "- Coconut welcome drinks and on-site coordinators"
        ],
        "The Grand Wedding": [
            "- Historic fort venue with Maharashtrian-themed decor",
            "- Haldi and reception events included",
            "- In-house and outside decorators available",
            "- Traditional Peshwa-style wedding arrangements",
            "- Lavish buffet with Maharashtrian and North Indian cuisine",
            "- Dhol-Tasha performance and fireworks show"
        ],
        "The Funky Wedding": [
            "- Luxury resort venue with modern and quirky decor",
            "- Haldi and engagement event setups included",
            "- Outside decorators allowed for personalized touch",
            "- Fusion cuisine catering with global delicacies",
            "- Entertainment with DJs and live performances",
            "- Adventure activities for guests (optional)"
        ],
        "The Punjabi & Sikhs Wedding": [
            "- Vibrant venue with colorful Punjabi decor",
            "- Engagement and reception events included",
            "- Traditional Sikh wedding setup (Anand Karaj)",
            "- Bhangra and Gidda dance performers",
            "- Authentic Punjabi cuisine with live tandoor station",
            "- Dhol entry for Baraat and open bar"
        ]
    }

    package_details = package_details_map.get(package_name, ["Package details not found."])
    return render_template('Wbook_package.html', package_name=package_name, package_details=package_details)

# 📧 Function to Send Confirmation Email
def send_confirmation_email(to_email, subject, name):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    
    email_body = f"""
    Dear {name},

    🎉 Congratulations! Your event booking has been successfully confirmed. 
    
    If you need any modifications to your booking or have any questions, feel free to reach out to us.

   
    ✉ Email: kpevents45@gmail.com  

    Thank you for choosing KP Event Management! We look forward to making your event a grand success. 🎊

    Best Regards,  
    KP Event Management Team  
    """

    # ✅ Use email_body instead of body
    msg.attach(MIMEText(email_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"📧 Email sent successfully to {to_email}")
    except Exception as e:
        print(f"⚠ Failed to send email: {e}")



def send_reminder_email():
    while True:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')

        bookings = bookings_collection.find({'event_date': tomorrow_str, 'reminder': "Enabled"})

        for booking in bookings:
            send_confirmation_email(
                booking['email'],
                "📅 Event Reminder: Your Event is Tomorrow!",
                booking['name'],
                booking['event_date'],
                booking['event_time'],
                booking['guests'],
                booking['special_requests'],
                booking['reminder']
            )

        time.sleep(86400)  # 24 hours


# Start the reminder function in a separate thread
reminder_thread = threading.Thread(target=send_reminder_email, daemon=True)
reminder_thread.start()


@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    data = request.form
    print(f"DEBUG: Full request form data -> {data}")  # Debugging print

    name = data.get('name', 'Guest')
    email = data.get('email', '')
    phone = data.get('phone', '')
    event_date = data.get('date', '')
    hour = data.get('timehour', '')
    minute = data.get('minute', '')
    ampm = data.get('ampm','')
    guests = data.get('guests', '0')
    special_requests = data.get('message', 'None')
    reminder = 'Enabled' if data.get('reminder') == 'on' else 'Not Enabled'
    

    time = f"{hour}:{minute} {ampm}"  # Combine all three

    file = request.files.get("payment_screenshot")
    file_path = None
    if file and file.filename:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)  # Save file on server

    # ✅ Store file_path in MongoDB
    booking_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'event_date': event_date,
        'event_time': time,
        'guests': guests,
        'message': special_requests,
        'reminder': reminder,
    }

    booking_id = bookings_collection.insert_one(booking_data).inserted_id

    # ✅ Send confirmation email
    send_confirmation_email(email, "Your Event Booking is Confirmed!", name)

    flash("Booking submitted!", "success")
    return redirect(url_for("booking_success", booking_id=booking_id))




    

@app.route('/booking_success/<booking_id>')
def booking_success(booking_id):
    try:
        booking = bookings_collection.find_one({'_id': ObjectId(booking_id)})
        if not booking:
            flash("❌ Booking not found.", "danger")
            return redirect(url_for('home'))
    except Exception:
        flash("⚠ Invalid booking ID.", "warning")
        return redirect(url_for('home'))

    return render_template('Wbooking_success.html', booking=booking)



@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    full_name = request.form['full_name']
    phone = request.form['phone']
    email = request.form['email']
    message = request.form['message']

    # Save to MongoDB
    contact_data = {
        'full_name': full_name,
        'phone': phone,
        'email': email,
        'message': message,
        'submitted_at': datetime.now()
    }
    contact_collection.insert_one(contact_data)

    

    # Send confirmation email
    subject = "📩 Thank You for Contacting KP Event Management!"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject

    body = f"""
    Dear {full_name},

    Thank you for reaching out to KP Event Management!

    We have received your enquiry and will get back to you shortly.

    Your Message:
    "{message}"

    📞 Phone: {phone}
    📧 Email: {email}

    Thank you again for your interest.

    Best Regards,  
    KP Event Management Team
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        print(f"✅ Enquiry email sent to {email}")
    except Exception as e:
        print(f"❌ Failed to send enquiry email: {e}")

    return render_template('contact.html', enquiry_submitted=True)

    


def send_meeting_confirmation_email(to_email, name, date, guests, hours ,time, meeting_type):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "📅 Meeting Scheduled Confirmation"

    email_body = f"""
    Dear {name},

    🎉 Your meeting has been successfully scheduled with us!

    Below are the meeting details:

    📅 *Date:* {date}
    ⏰ *Time:* {time}
    👥 *Guests:* {guests}
    🕒 *Hours of Meeting:* {hours}
    📌 *Meeting Type:* {meeting_type}

    If you need any modifications or further assistance, feel free to contact us.

    ✉ Email: kpevents45@gmail.com  

    Thank you for choosing KP Event Management! We look forward to a productive meeting with you.

    Best Regards,  
    KP Event Management Team  
    """

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"📧 Email sent successfully to {to_email}")
    except Exception as e:
        print(f"⚠ Failed to send email: {e}")

     

@app.route('/schedule_meeting', methods=['GET', 'POST'])
def schedule_meeting():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        organization = request.form['organization']
        venue = request.form['venue']
        guests = request.form['guests']
        date = request.form['date']
        hour = request.form['timehour']
        minute = request.form['minute']
        ampm = request.form['ampm']
        hours = request.form['hours']
        meeting_type = request.form['meeting-type']
        total_cost = request.form['total-cost']
        reminder = request.form.get('reminder') == 'on'

        time = f"{hour}:{minute} {ampm}"  # Combine all three

        # Ensure all required fields are provided
        if not name or not email or not date or not time or not meeting_type or not total_cost:
            flash("All fields are required.", "danger")
            return redirect(url_for('schedule_meeting'))


        # Save form data to MongoDB
        meeting_data = {
            'name': name,
            'email': email,
            'organization': organization,
            'venue': venue,
            'guests': guests,
            'date': date,
            'time': time,
            'hours': hours,
            'meeting_type': meeting_type,
            'total_cost': total_cost,
            'reminder': reminder
        }

        try:
            meeting_id = db['meetings'].insert_one(meeting_data).inserted_id
        except Exception as e:
            flash(f"Failed to save meeting: {e}", "danger")
            return redirect(url_for('schedule_meeting'))

        # Send a confirmation email
        send_meeting_confirmation_email(email, name, date, guests, hours ,time, meeting_type)

        flash("Meeting scheduled successfully!", "success")
        return redirect(url_for('meeting_success', meeting_id=meeting_id))

    return render_template('schedule_meeting.html')  # You need to create a form for this template

@app.route('/meeting_success/<meeting_id>')
def meeting_success(meeting_id):
    try:
        # Find the meeting by its ID from MongoDB
        meeting = db['meetings'].find_one({'_id': ObjectId(meeting_id)})
        if not meeting:
            flash("❌ Meeting not found.", "danger")
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"⚠ Error retrieving meeting details: {e}", "warning")
        return redirect(url_for('home'))
    
    # Pass the meeting data to the template
    return render_template('meeting_success.html', meeting=meeting)




if __name__ == '__main__':
    app.run(debug=True)