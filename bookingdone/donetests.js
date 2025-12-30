window.addEventListener('DOMContentLoaded', function() {
    
    const appointmentData = JSON.parse(sessionStorage.getItem('appointmentData'));
    
    if (appointmentData) {
        console.log('Appointment data found:', appointmentData);
        populateReceipt(appointmentData);
    } else {
        console.error('No appointment data found in sessionStorage');
    
        alert('No appointment data found. Redirecting to home...');
        window.location.href = '/';
    }
});

function populateReceipt(data) {
    try {
        const testId = 'TST-' + generateRandomId();
        document.querySelector('.id-value').textContent = testId;
        
        const detailItems = document.querySelectorAll('.detail-item');
        
        detailItems.forEach(item => {
            const label = item.querySelector('.detail-label').textContent.toLowerCase();
            const valueElement = item.querySelector('.detail-value');
            
            if (label.includes('patient name')) {
                valueElement.textContent = data.name || 'N/A';
            }
            else if (label.includes('date')) {
                valueElement.textContent = formatDate(data.date) || 'N/A';
            }
            else if (label.includes('test')) {
                valueElement.textContent = data.test || 'N/A';
            }
            else if (label.includes('time')) {
                valueElement.textContent = formatTime(data.time) || 'N/A';
            }
            else if (label.includes('contact')) {
                valueElement.textContent = data.phone || 'N/A';
            }
            else if (label.includes('prerequisite')) {
                valueElement.innerHTML = getTestPrerequisites(data.test);
            }
        });
        
        document.querySelector('.subtitle').textContent = 
            `Your ${data.test} test has been successfully booked. Here are your appointment details:`;
            
    } catch (error) {
        console.error('Error populating receipt:', error);
    }
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'numeric', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options);
}

function formatTime(timeSlot) {
    if (!timeSlot) return 'N/A';
    
    const timeMap = {
        '8-9am': '08:00 - 09:00',
        '9-10am': '09:00 - 10:00',
        '10-11am': '10:00 - 11:00',
        '11-12pm': '11:00 - 12:00',
        '2-3pm': '14:00 - 15:00',
        '3-4pm': '15:00 - 16:00',
        '4-5pm': '16:00 - 17:00'
    };
    
    return timeMap[timeSlot] || timeSlot;
}

function getTestPrerequisites(testType) {
    if (!testType) return 'Follow general guidelines';
    
    const prerequisites = {
        'X-Ray': 'No metal objects<br>Wear hospital gown<br>Avoid if pregnant',
        'MRI': 'No metal implants<br>Remove jewelry<br>Inform if claustrophobic',
        'CT Scan': '12hrs fasting may be required<br>Remove metal accessories<br>Inform about allergies'
    };
    
    return prerequisites[testType] || 'Follow general test guidelines';
}

function generateRandomId() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 8; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

function downloadReceipt() {
    window.print();
}

function bookAnother() {
    sessionStorage.removeItem('appointmentData');
    window.location.href = '/BookTests/booktests.html';
}

function goHome() {
    sessionStorage.removeItem('appointmentData');
    window.location.href = '/dashboard/dashboard.html';
}