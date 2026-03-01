function handleFormSubmit() {
  const doctor = localStorage.getItem("doctor");
  
  const formData = {
    name: document.getElementById('name').value.trim(),
    age: document.getElementById('age').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    email: document.getElementById('email').value.trim(),
    gender: document.getElementById('gender').value,
    date: document.getElementById('appointment-date').value,
    time: document.getElementById('appointment-time').value,
    reason: document.getElementById('reason').value.trim(),
    visitType: document.getElementById('first').value,
    doctor: doctor,
  };

  if (!formData.name || !formData.age || !formData.phone || !formData.email || 
      !formData.date || !formData.time || !formData.reason) {
    alert('Please fill in all required fields.');
    return false; 
  }

  if (formData.gender === 'disabled' || formData.visitType === 'disabled') {
    alert('Please select all dropdown options.');
    return false;
  }

  
  sessionStorage.setItem('appointmentData', JSON.stringify(formData));
  
  const appointments = JSON.parse(localStorage.getItem("appointments")) || [];
  const newAppt = {
    date: formData.date,
    time: formData.time,
    doc: doctor,
    email: formData.email,
  };
  appointments.push(newAppt);
  localStorage.setItem("appointments", JSON.stringify(appointments));
  
  return true; 
}