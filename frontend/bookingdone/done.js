
const appointmentData = JSON.parse(sessionStorage.getItem('appointmentData'));
console.log('Data from sessionStorage:', appointmentData);

const elements = {
  name: document.getElementById('name'),
  age: document.getElementById('age'), 
  phone: document.getElementById('phone'),
  email: document.getElementById('email'),
  gender: document.getElementById('gender'),
  date: document.getElementById('date'),
  time: document.getElementById('time'),
  reason: document.getElementById('reason'),
  first: document.getElementById('first')
};

console.log('Elements found:', elements);

Object.keys(elements).forEach(key => {
  if (!elements[key]) {
    console.log(`MISSING ELEMENT: ${key}`);
  } else {
    console.log(`FOUND ELEMENT: ${key} - current text: "${elements[key].textContent}"`);
  }
});

if (appointmentData) {
  Object.keys(elements).forEach(key => {
    if (elements[key] && appointmentData[key]) {
      elements[key].textContent = appointmentData[key];
      console.log(`Updated ${key} with: ${appointmentData[key]}`);
    }
  });
}
function downloadReceipt() {
  const element = document.getElementById('receipt');
  console.log("element:", element);
  
  if (!element) {
    console.error("Receipt element not found");
    return;
  }
  
  const opt = {
    margin: [0, 0, 0, 0],
    filename: 'booking-receipt.pdf',
    image: { type: 'jpeg', quality: 1 },
    html2canvas: { scale: 2, useCORS: true },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };

  console.log("options:", opt);
  html2pdf().set(opt).from(element).save();
}


document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("downloadReceipt");
  if (btn) {
    btn.addEventListener("click", downloadReceipt);
  }
});
