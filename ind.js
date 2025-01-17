const nodemailer = require('nodemailer');

async function sendOrderEmail(customerEmail, orderDetails) {
    // Email settings
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'tejakumar2121@gmail.com',
            pass: 'ifmwbxgycvsaqwbv'
        }
    });

    // Email body
    let mailOptions = {
        from: 'tejakumar2121@gmail.com',
        to: customerEmail,
        subject: 'Your Order Details',
        text: `Thank you for your order. Here are your details:\n\n${orderDetails}`
    };

    // Send the email
    try {
        let info = await transporter.sendMail(mailOptions);
        console.log('Email sent: ' + info.response);
    } catch (error) {
        console.error('Error sending email: ' + error);
    }
}

// Example usage
let orderDetails = `
Product: Apples
Quantity: 2 kg
Price: $4
`;

sendOrderEmail('tejakumar3131@gmail.com', orderDetails);
