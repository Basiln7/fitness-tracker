// LOGIN.HTML
async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch("/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData
  });

  const data = await res.json();
if (res.status === 200 && data.access_token) {
  localStorage.setItem("token", data.access_token);
  window.location.href = "/workout";
} else {
  alert(data.detail || "Login failed");
}
}

function goToSignup() {
  window.location.href = "/signup";
}

// SIGNUP.HTML
function handleSignup(event) {
  event.preventDefault(); // prevent page reload

  const name = document.getElementById("signup-username").value;
  const password = document.getElementById("signup-password").value;

  // Optional: collect other fields (not used in backend yet)
  const fullName = document.getElementById("full-name").value;
  const phone = document.getElementById("phone").value;
  const gender = document.getElementById("gender").value;

  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, password })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message || "Signup successful");
    if (data.message) {
      window.location.href = "/"; // redirect to login
    }
  })
  .catch(err => {
    console.error("Signup error:", err);
    alert("Signup failed");
  });
}