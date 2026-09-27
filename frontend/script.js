let question = document.querySelector("#txt_value");
let display = document.querySelector("#cat-box");
let chatbot = document.querySelector("#chatbot");
let signup = document.querySelector("#SignUp");
let login = document.querySelector("#login")

if (chatbot) {
    chatbot.addEventListener("submit", async function (e) {
        e.preventDefault();

        const token = localStorage.getItem("token");

        if (!token) {
            window.location.href = "login.html";
            return;
        }


        const response = await fetch("http://127.0.0.1:8000/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ user_input: question.value })
        });


        if (response.status === 401) {
            alert("Session expired. Please log in again.");
            localStorage.removeItem("token"); // Clear the dead token
            window.location.href = "login.html";
            return;
        }
        const data = await response.json();

        if (response.ok) {
            const message = document.createElement("h3");
            message.textContent = data.answer;
            display.appendChild(message);
        }

        //  catch {
        //     window.location.href = "login.html";
        // }
    });
}

if (signup) {
    signup.addEventListener("submit", async function (e) {
        e.preventDefault();
        let email = document.querySelector("#signup_email").value;
        let pass = document.querySelector("#signup_pass").value;

        const response = await fetch("http://127.0.0.1:8000/api/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username: email, password: pass })
        });


        if (!response.ok) {
            window.location.href = "signup.html";
            return;
        }

        window.location.href = "login.html";
    });
}

if (login) {
    login.addEventListener("submit", async function (e) {
        e.preventDefault();
        let email = document.querySelector("#login_email").value;
        let pass = document.querySelector("#login_pass").value;

        const response = await fetch("http://127.0.0.1:8000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: email, password: pass })
        });

        if (response.status === 401) {
            alert("invalid Credientials")
            window.location.href = "signup.html";
            return;
        }
        else if (response.status === 400) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || "Invalid input check your credentials."}`);
            throw new Error("Bad Request");
        }
        else if (response.ok) {
            const data = await response.json();
            localStorage.setItem("token", data.access_token);
            window.location.href = "index.html";
        }
    });
}

let fileInput = document.querySelector("#pdf-upload");
let uploadBtn = document.querySelector("#upload-btn");

if (fileInput && uploadBtn) {
    uploadBtn.addEventListener("click", async function () {
        const file = fileInput.files && fileInput.files[0];

        if (!file) {

            return;
        }

        const token = localStorage.getItem("token");
        if (!token) {
            window.location.href = "login.html";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/upload", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                body: formData
            });
            if (response.status === 401) {
                alert(" Please log in again.");

                window.location.href = "login.html";
                return;
            }
            else if (response.ok) {
                alert("documents uploaded and processing in the background")
            }
        } catch {
            window.location.href = "login.html";
        }
    });
}