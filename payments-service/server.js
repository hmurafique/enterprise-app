const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({payment: "Payment service running", status: "ok"});
});

app.listen(7000, () => {
    console.log("Payments service running on port 7000");
});
