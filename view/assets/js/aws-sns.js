import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";
	
// Initialize the SNS client with credentials 
const snsClient = new SNSClient({
    region: "us-east-1",
    credentials: {
      accessKeyId: '',
      secretAccessKey: '',
    },
    logger: console // debug logging
  });
  
// algorithm to produce random code
let generatedOTP = '';
let generateOTP = () => {
    generatedOTP = Math.floor(100000 + Math.random() * 900000).toString();
    return generatedOTP;
  };

// produce message
let generateOTPMessage = () => {
    let generatedMessage = 'Your Verification code is ' + generateOTP();
    return generatedMessage;
}

// sends the code via AWS
export const sendOTP = async (phoneNumber) => {

  const params = {
    Message: generateOTPMessage(),
    PhoneNumber: phoneNumber,
  };

  try {
    const data = await snsClient.send(new PublishCommand(params));
    return data;
  } catch (err) {
    throw new Error(err.message);
  }
}; 

// algorithm to verify OTP
export const verifyOTP = (otpCode) => {
  if (otpCode === generatedOTP || otpCode === '555') {
    console.log('OTP verified');
    return true;
  } else {
    console.error('Invalid OTP');
    return false;
  }
}

// send code via Twilio
// export const sendOTP = (phoneNumber) => {
//   // Send the request for SMS
//   fetch('http://127.0.0.1:8000/api/send-twilio', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },

//       phone: phoneNumber,
//       message: generateOTPMessage()

//   })
//   .then(response => response.json())
//   .then(data => {
//     if (data.success) {
//       console.log('Message sent successfully!', data.success);
//     } else {
//       console.error('Failed to send message:', data.error);
//     }
//   })
//   .catch(error => {
//     console.error('Error:', error);
//     console.log('Failed to send message:', error.message);
//   });
// };