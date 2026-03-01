let users = JSON.parse(localStorage.getItem("users")) || [];

// SIGNUP
const sign_form = document.getElementById("sign-up");
if (sign_form) {
    
    sign_form.addEventListener("submit", (e) => {
        e.preventDefault();
        const s_email = document.getElementById("mail");
        const s_pass = document.getElementById("password");
        const s_rep_pass = document.getElementById("rep_pass");
        const name=document.getElementById("name");

    const val_email = s_email.value.trim();
    const val_pass = s_pass.value.trim();
    const val_rep_pass = s_rep_pass.value.trim();
  
        
    if (!val_email || !val_pass || !val_rep_pass) {
      alert("All fields required!");
      return;
    }

    if (val_pass !== val_rep_pass) {
      alert("Passwords do not match!");
      return;
    }

    if (users.some(u => u.email === val_email)) {
      alert("Email already registered!");
      window.location.href = "login_signup/Log-in.html";
      return;
    }
// let meds=["Levipil 500 mg 1-0-1","Shellcal 0-0-1","CERTIcan 0.25mg post dinner"]
    users.push({ name:name, email: val_email, pass: val_pass,appointments:[],tests:[],prescribtion:[] });
    localStorage.setItem("users", JSON.stringify(users));

    alert("Sign up successful!");
   window.location.href = "/login_signup/Log-in.html";

    console.log("sign up done");
});
}

// LOGIN
const loginForm = document.getElementById("form");
const loginbutton = document.getElementById("sub");
const loginerror = document.getElementById("error");

if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const user = loginForm.email.value.trim();
    const pass = loginForm.pass.value.trim();

    const user_check = users.find(u => u.email === user && u.pass === pass);

    if (user_check) {
      alert("Login Successful!");
      localStorage.setItem("currentUser", user);
      window.location.href = "/dashboard/dashboard.html";
    } else {
      loginerror.style.opacity = 1;
    }
  });
}
