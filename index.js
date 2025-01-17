const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');
const app = express();

app.use(bodyParser.json());

// Function to send the order email
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

app.post('/submit-order', (req, res) => {
    const { name, email, phone, vegetable, fruit, meat, quantity } = req.body;
    const orderDetails = `
    Name: ${name}
    Email: ${email}
    Phone: ${phone}
    Vegetable: ${vegetable}
    Fruit: ${fruit}
    Meat: ${meat}
    Quantity: ${quantity}
    `;

    sendOrderEmail(email, orderDetails)
        .then(() => res.json({ message: 'Order received and email sent.' }))
        .catch(error => res.status(500).json({ error: 'Error sending email.' }));
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
