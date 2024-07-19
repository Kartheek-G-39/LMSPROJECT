function sendOTP() {
    const email = document.getElementById('rollNumberInput');
    let mail = email.value.toLowerCase();

    $.ajax({
        type: "POST",
        url: "/verify/",
        data: {"mail": mail},
        success: function(response) {
            if (response.message == "exists") {
                email.value = "";
                alert("User already exists");
            } else {
                const otpverify = document.getElementById('otpField');
                let otp_val = Math.floor(Math.random() * 10000);

                emailjs.init("{{ EMAILJS_USER_ID }}");

                var params = {
                    to_email: mail,
                    from_name: "Your Company",
                    message: "Verify your account with OTP: " + otp_val,
                    to_name: mail.match(/(.*)@/)[1],
                };

                emailjs.send("{{ EMAILJS_SERVICE_ID }}", "{{ EMAILJS_TEMPLATE_ID }}", params)
                    .then(function(response) {
                        alert("OTP sent to your email");
                        document.getElementById("sendOTPButton").style.display = "none";
                        otpverify.style.display = "block";
                        email.readOnly = true;
                        const otp_inp = document.getElementById('otpInput');
                        const otp_btn = document.getElementById('verifyOTPButton');
                        otp_btn.addEventListener('click', () => {
                            if (otp_inp.value == otp_val) {
                                otpverify.style.display = "none";
                                document.getElementById("passwordDiv").style.display = "block";
                                $.ajax({
                                    type: "POST",
                                    url: "/clear/",
                                    data: {"mail": mail}
                                });
                            } else {
                                alert("Invalid OTP");
                            }
                        });
                    }, function(error) {
                        console.error("Email sending failed:", error);
                        alert("Email sending failed!");
                    });
            }
        }
    });
}

function validate() {
    const pass1 = document.getElementById("passwordInput");
    const pass2 = document.getElementById("confirmPasswordInput");
    if (pass1.value === pass2.value) {
        document.getElementById("submitButton").type = "submit";
    } else {
        pass1.value = pass2.value = "";
        alert("Passwords do not match");
    }
}

function handleInput_loginpage(input) {
    if (input.value.length === 10) {
        input.value += "@vvit.net";
        input.addEventListener("keydown", function(event) {
            if (event.key === "Backspace") {
                input.value = "";
            }
        });
    }
}
