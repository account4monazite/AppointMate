window.addEventListener('DOMContentLoaded', () => {
  const test = localStorage.getItem("Test");
  if (test) {
    const box = document.getElementById("prerequisites");
    const inf = document.getElementById("inf");
    const hed = document.getElementById("test");

    hed.innerText = 'Book ' + test;

    if (test === 'X-Ray') {
      box.innerText = "Prerequisites: No metal Objects | Wear hospital Gown | Avoid if Pregnant";
      inf.innerText = "Price: ₹1000 | Duration: 15-20 Minutes";
    } else if (test === 'MRI') {
      box.innerText = "Prerequisites: No metal Implants | Remove Jewelry | Inform if Claustrophobic";
      inf.innerText = "Price: ₹3500 | Duration: 30-60 Minutes";
    } else if (test === 'CT Scan') {
      box.innerText = "Prerequisites: Contrast agent may be used | Remove Jewelry | Inform about allergies";
      inf.innerText = "Price: ₹2000 | Duration: 20-30 Minutes";
    }
  }
});

document.querySelector('.forms').addEventListener('submit', function (e) {
  e.preventDefault();
  
  console.log('Form submission started'); 

  const date = document.getElementById('appointment-date').value;
  const time = document.getElementById('appointment-time').value;
  const testType = localStorage.getItem('Test');

  const name = document.getElementById('name').value.trim();
  const age = document.getElementById('age').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const email = document.getElementById('email').value.trim();
  const gender = document.getElementById('gender').value;
  const reason = document.getElementById('reason').value.trim();

  // Check if all required fields are filled
  if (!name || !age || !phone || !email || !date || !time || !reason) {
    alert('Please fill in all required fields.');
    return;
  }

  if (gender === 'disabled' || !gender) {
    alert('Please select your gender.');
    return;
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }

  console.log('Validation passed'); // Debug log

  const formData = {
    name: name,
    age: age,
    phone: phone,
    email: email,
    gender: gender,
    date: date,
    time: time,
    reason: reason,
    test: testType
  };

  console.log('Form data collected:', formData);


  const tests = JSON.parse(localStorage.getItem("tests")) || [];
  
  const newAppt = {
    date: date,
    time: time,
    test: testType,
    email: email, 
    patientName: name,
    id: Date.now()
  };

  console.log('New appointment object:', newAppt); 

  const conflict = tests.some(a =>
    a.test === newAppt.test && a.date === newAppt.date && a.time === newAppt.time
  );

  if (conflict) {
    alert(`This time slot is already booked for ${testType}! Please select a different time.`);
    return;
  }

  const patientConflict = tests.some(a =>
    a.email === newAppt.email && a.date === newAppt.date
  );

  if (patientConflict) {
    alert('You already have a test scheduled for this date. Please select a different date.');
    return;
  }


  tests.push(newAppt);
  localStorage.setItem("tests", JSON.stringify(tests));
  
  sessionStorage.setItem('appointmentData', JSON.stringify(formData));

  console.log('Data stored successfully'); // Debug log
  console.log('Stored data:', sessionStorage.getItem('appointmentData'));

  alert("Test appointment booked successfully!");
  
  console.log('About to redirect to: /bookingdone/done_tests.html'); // Debug log
  
  window.location = "/bookingdone/done_tests.html";
});