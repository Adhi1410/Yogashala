
 var sent_otp ;
 function sendEmail() {

      Email.send({
        Host: "smtp.gmail.com",
        Username: "sandeep.kumar.k.3339@gmail.com",
        Password: "Innova3592@",
        To:document.getElementById("email").value,
        From: "sandeep.kumar.k.3339@gmail.com",
        Subject: "Yogashaala OTP",
       Body: generateOTP(),
      })
        .then(function (message) {
          alert("mail sent successfully")
        });
    }

function generateOTP() {
    var digits = '0123456789';
    var OTP = '';
    for (let i = 0; i < 6; i++ ) {
        OTP += digits[Math.floor(Math.random() * 10)];
    }
    sent_otp = OTP;
    return OTP;
}
function check(){
    if (document.getElementById("eotp").value == 942411)
    {
          alert("OTP matched ");
    }
    else
    {
          alert("OTP mismatched ");
    }
}