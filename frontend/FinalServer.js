const express = require('express');
const app = express();
const bodyParser = require('body-parser');

const axios = require('axios');
const path = require("path");
const {get, request} = require("axios");
const res = require("express/lib/response");
const {response} = require("express");

app.use(bodyParser.urlencoded());

const port = 8080

app.set("views", path.resolve(__dirname, "views"))
app.set("view engine", "ejs");

app.get('/', (request, response) => response.render("pages/login", {
    message: 'Welcome to EJS HW 3'
}))

app.post('/process_login', async function (req, res) {
    var usr = req.body.username;
    var pwd = req.body.password;
    const url ='http://127.0.0.1:5000/login';
    axios.get(url)




})



// start the express application on port 8080
    app.listen(port, () => console.log('Application started listening'))