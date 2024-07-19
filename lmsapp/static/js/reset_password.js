function sendResetOTP() {
    const email = document.getElementById('resetEmailInput');
    let mail = email.value.toLowerCase();

    $.ajax({
        type: "POST",
        url: "/reset/verify/",
        data: {"mail": mail},
        success: function(response) {
            if (response.message == "not_exists") {
                email.value = "";
                alert("User does not exist");
            } else {
                const otpField = document.getElementById('otpField');
                let otp_val = Math.floor(Math.random() * 10000);

                emailjs.init("{{ EMAILJS_USER_ID }}");

                var params = {
                    to_email: mail,
                    from_name: "Your Company",
                    message: "Reset your password with OTP: " + otp_val,
                    to_name: mail.match(/(.*)@/)[1],
                };

                emailjs.send("{{ EMAILJS_SERVICE_ID }}", "{{ EMAILJS_TEMPLATE_ID }}", params)
                    .then(function(response) {
                        alert("OTP sent to your email");
                        document.getElementById("sendResetOTPButton").style.display = "none";
                        otpField.style.display = "block";
                        email.readOnly = true;
                        const otpInput = document.getElementById('resetOtpInput');
                        const verifyOtpButton = document.getElementById('verifyResetOtpButton');
                        verifyOtpButton.addEventListener('click', () => {
                            if (otpInput.value == otp_val) {
                                otpField.style.display = "none";
                                document.getElementById("newPasswordDiv").style.display = "block";
                                $.ajax({
                                    type: "POST",
                                    url: "/reset/clear/",
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

function validateNewPassword() {
    const pass1 = document.getElementById("newPasswordInput");
    const pass2 = document.getElementById("confirmNewPasswordInput");
    if (pass1.value === pass2.value) {
        document.getElementById("resetSubmitButton").type = "submit";
    } else {
        pass1.value = pass2.value = "";
        alert("Passwords do not match");
    }
}
